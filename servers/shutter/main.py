# -*- coding: utf-8 -*-

"""main.py:

"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231009"

# std libs
from typing import Annotated
from json import JSONDecodeError
from contextlib import asynccontextmanager
# third party libs
from fastapi import Depends, FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
# external package
from serial_helper import SerialManager, SerialMocker
# this package
from .shutter import ShutterController, ShutterState, ShutterAction, ShutterActionResult
from .config import config, UserAccessLevel
from .auth import try_authenticate, create_access_token, validate_access_token, Token, TokenData, AccessLevelException
from .ws import WebSocketConnectionManager


class ShutterChannelOperation(BaseModel):
    action: ShutterAction


class ShutterStateReport(BaseModel):
    shutter_name: str
    state: ShutterState


class ShutterChannelList(BaseModel):
    shutter_list: list[str]


# create ShutterController that all threads shares according to config.
serial_config = config.hardware.serial
ser_mgr = SerialManager(
    serial_config.port, baudrate=serial_config.baudrate, timeout=serial_config.timeout)

# ----- TEMPORARY FOR TESTING
IS_TESTING = True
if IS_TESTING:
    # mut borrow ser_mgr, replace Serial with Mocked Serial
    response_map = {
        b"SHT1:OFF\n": b"OK, SHT1OFF\n",
        b"SHT1:ON\n": b"OK, SHT1ON\n",
        b"SHT2:OFF\n": b"OK, SHT2OFF\n",
        b"SHT2:ON\n": b"OK, SHT2ON\n",
    }
    ser_mgr.ser = SerialMocker(
        serial_config.port, baudrate=serial_config.baudrate, timeout=serial_config.timeout,
        response_map=response_map)
# ===== END TEMPORARY FOR TESTING

sc = ShutterController(ser_mgr, shutter_names=config.hardware.shutter_names)
ws_mgr = WebSocketConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start ShutterController and corresponding threads
    sc.start()
    yield
    # Clean up resources, gracefully shut down ShutterController
    sc.stop()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get_shutter_list() -> ShutterChannelList:
    return ShutterChannelList(shutter_list=sc.shutter_names)


@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    authenticate_result, user = try_authenticate(
        config.auth.users, form_data.username, form_data.password)
    if authenticate_result is False:
        # don't tell the user if it is the username or the password that is wrong.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # authentication successful, create token
    access_token = create_access_token(user=user)
    return Token(**{"access_token": access_token, "token_type": "bearer"})


@app.get("/{shutter_name}")
async def get_shutter_state(shutter_name: str,
                            token_data: Annotated[TokenData, Depends(validate_access_token)]) -> ShutterStateReport:
    if shutter_name not in sc.shutter_names:
        raise HTTPException(
            status_code=404, detail="No such shutter: {}".format(shutter_name))
    return ShutterStateReport(
        shutter_name=shutter_name,
        state=sc.shutter_states[shutter_name]
    )


@app.post("/{shutter_name}")
async def set_shutter_state(shutter_name: str,
                            operation: ShutterChannelOperation,
                            token_data: Annotated[TokenData, Depends(validate_access_token)]) -> ShutterStateReport:
    # check user access_level before performing operation
    if token_data.access_level is UserAccessLevel.readonly:
        raise HTTPException(
            status_code=403, detail="User with access level 'readonly' is not allowed to operate on this device."
        )
    # perform action
    op_result = sc.shutter_action(shutter_name, operation.action)
    if op_result is ShutterActionResult.OK:
        pass
    elif op_result is ShutterActionResult.SHUTTER_NOT_FOUND:
        raise HTTPException(
            status_code=404, detail="No such shutter: {}".format(shutter_name))
    elif op_result is ShutterActionResult.INVALID_ACTION:
        raise HTTPException(
            status_code=404, detail="No such action: {}".format(operation.action))
    else:
        raise HTTPException(
            status_code=500, detail="Action failed: {}".format(op_result.value))
    return ShutterStateReport(
        shutter_name=shutter_name,
        state=sc.shutter_states[shutter_name]
    )


@app.websocket("/{shutter_name}/ws")
async def ws_endpoint(shutter_name: str,
                      websocket: WebSocket):
    try:
        await ws_mgr.connect(websocket)
        while True:
            # receive a command, validate the command and execute the command.
            data = await websocket.receive_json()
            op = ShutterChannelOperation(**data)
            # check user priviledge
            if ws_mgr.active_connections.get(websocket).access_level is UserAccessLevel.readonly:
                raise AccessLevelException
            op_result = sc.shutter_action(shutter_name, op.action)
            # tell operating client result of operation.
            await websocket.send_json({"result": op_result.value})
            # because the shutter is a shared resource of all clients, broadcast the newest state to all clients.
            await ws_mgr.broadcast(jsonable_encoder(ShutterStateReport(
                shutter_name=shutter_name,
                state=sc.shutter_states[shutter_name]
            )))
    except WebSocketDisconnect:
        # user disconnected from client side.
        pass
    except JSONDecodeError:
        # user sent non-json message, probably wrong client, disconnect right away.
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    except ValidationError:
        # user input lack required field or malformed, report error to user and disconnect right away.
        await websocket.send_json({"error": "Invalid Operation"})
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    except AccessLevelException:
        # user input is legal and the user is good, but the user does not have the permission to perform the operation.
        await websocket.send_json({"error": "Insufficient Access Level"})
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)  
    finally:
        # clear websocket stored in manager as well as its auth info.
        ws_mgr.disconnect(websocket)

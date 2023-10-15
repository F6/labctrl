# -*- coding: utf-8 -*-

"""auth.py:
This module provide functions for password verification, token generation and token validation.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231009"

# std libs
from datetime import datetime, timedelta
from typing import Annotated
# third-party libs
from fastapi import Depends, HTTPException, status, WebSocketException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, UUID4
# own package
from .config import config, UserConfig, UserAccessLevel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    # Subject (required): we will use user id as sub to avoid username collision.
    sub: UUID4
    # Expires (required): integer timestamp, measured in the number of seconds since January 1 1970 UTC
    exp: datetime
    # Custom contents
    username: str
    access_level: UserAccessLevel


class AccessLevelException(Exception):
    pass


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def try_authenticate(users: list[UserConfig], username: str, password: str) -> tuple[bool, UserConfig | None]:
    """
    Search user with given username in a given users list, then verify the password of the user.
    """
    for user in users:
        if username == user.username:
            if pwd_context.verify(password, user.hashed_password):
                return (True, user)
            else:
                # user found, but incorrect password
                return (False, user)
    # no such user
    return (False, None)


def create_access_token(user: UserConfig, expires_delta: timedelta | None = None) -> str:
    """
    Creates encoded JSON Web Token from given data and expire delta.
    NOTE: This function uses current server time to calculate the expiration time, make sure the server time is correct!
    """
    to_encode = dict()
    to_encode["sub"] = user.id
    to_encode["username"] = user.username
    to_encode["access_level"] = user.access_level
    # jwt.encode only takes json encodable objects so convert before that.
    to_encode = jsonable_encoder(to_encode)
    jwt_config = config.auth.jwt
    if expires_delta is None:
        expire = datetime.utcnow() + timedelta(minutes=jwt_config.expire_seconds)
    else:
        expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, key=jwt_config.secret, algorithm=jwt_config.algorithm)
    return encoded_jwt


def validate_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    """
    Validates a given JWT in HTTP header and returns the data encoded in the token.
    If validation is unsuccessful, raises HTTP 401 Unauthorized.
    This function depends on OAuth2 Password Bearer scheme so if you need to add authentication to an app path, simply 
    add this function in the Depends() as follows:

        fn(..., token_data: Annotated[TokenData, Depends(validate_access_token)])

    NOTE: This function uses current server system time to validate expiration time, so make sure the system clock is
    accurate.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    jwt_config = config.auth.jwt
    try:
        payload = jwt.decode(token, jwt_config.secret,
                             algorithms=[jwt_config.algorithm])
        return TokenData(**payload)
    except JWTError:
        raise credentials_exception


def validate_token_ws(token: str | None) -> TokenData:
    """
    Validates a given JWT and returns the data encoded in the token.
    If validation is unsuccessful, raises WebSocket 1008 Policy Violation.
    This function also accepts a None input, because it is common to use dict.get("token") to retrive token str from a 
    dict, and if "token" is not in the dict then it returns None and should fail to validate.

    NOTE: this function is only for WebSocket authentication.
    """
    ws_credentials_exception = WebSocketException(
        code=status.WS_1008_POLICY_VIOLATION, reason="Invalid Token")
    jwt_config = config.auth.jwt
    if token is None:
        raise ws_credentials_exception
    try:
        payload = jwt.decode(token, jwt_config.secret,
                             algorithms=[jwt_config.algorithm])
        return TokenData(**payload)
    except JWTError:
        raise ws_credentials_exception



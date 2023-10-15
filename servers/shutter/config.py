# -*- coding: utf-8 -*-

"""config.py:
This module defines the data model of config file for this project.
It also provides methods to load config from config file, or dump config to a file.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231009"

# std libs
import os
import json

from enum import Enum

# third party libs
from pydantic import BaseModel, UUID4

# meta params and defaults
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')


class UserAccessLevel(str, Enum):
    readonly = "readonly"
    standard = "standard"
    advanced = "advanced"


class UserConfig(BaseModel):
    id: UUID4
    username: str
    hashed_password: str
    access_level: UserAccessLevel


class JWTConfig(BaseModel):
    secret: str
    algorithm: str
    expire_seconds: int


class AuthConfig(BaseModel):
    users: list[UserConfig]
    jwt: JWTConfig


class SerialConfig(BaseModel):
    port: str
    timeout: float
    baudrate: int


class HardwareConfig(BaseModel):
    serial: SerialConfig
    shutter_names: list[str]


class ApplicationConfig(BaseModel):
    auth: AuthConfig
    hardware: HardwareConfig


def load_config_from_file(config_path: str = CONFIG_PATH):
    with open(config_path, 'r') as f:
        r = json.load(f)
    return ApplicationConfig(**r)


def dump_config_to_file(config: ApplicationConfig, config_path: str = CONFIG_PATH):
    with open(config_path, 'w+') as f:
        f.write(config.model_dump_json(indent=4))


config = load_config_from_file()

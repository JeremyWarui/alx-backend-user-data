#!/usr/bin/env python3
"""session auth class"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User


class SessionAuth(Auth):
    """session authorisation class"""
    pass

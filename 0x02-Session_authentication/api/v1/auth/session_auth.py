#!/usr/bin/env python3
"""session auth class"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """session authorisation class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

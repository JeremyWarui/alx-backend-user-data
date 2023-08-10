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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on the cookie value"""
        session_cookie = self.session_cookie(request)
        try:
            _id = self.user_id_for_session_id(session_cookie)
            return User.get(_id)
        except Exception:
            return None

    def destroy_session(self, request=None):
        """deletes user session or logout"""
        try:
            session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_id)
            del self.user_id_by_session_id[session_id]
            return True
        except Exception:
            return False

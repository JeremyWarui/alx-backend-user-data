#!/usr/bin/env python3
"""basic auth class"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User


class BasicAuth(Auth):
    """basic authorisation class"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns Base64 of the Authorization header
        for basic authentication"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        basic = authorization_header.split(" ")
        return basic[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns decoded value of Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base_encode = base64_authorization_header.encode("utf-8")
            base_decode = b64decode(base_encode)
            decoded_val = base_decode.decode("utf-8")
            return decoded_val
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns user email and password from Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        personal_data = decoded_base64_authorization_header.split(":", 1)
        return personal_data[0], personal_data[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the user instance based on his/her email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for
        a request"""
        try:
            header = self.authorization_header(request=request)
            base64_header = self.extract_base64_authorization_header(header)
            decoded_val = self.decode_base64_authorization_header(
                base64_header)
            personal_data = self.extract_user_credentials(decoded_val)
            user = self.user_object_from_credentials(personal_data[0],
                                                     personal_data[1])
            return user
        except Exception:
            return None

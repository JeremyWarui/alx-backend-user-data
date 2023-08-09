#!/usr/bin/env python3
"""basic auth class"""
from api.v1.auth.auth import Auth


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

#!/usr/bin/env python3
"""basic auth class"""
from api.v1.auth.auth import Auth
from base64 import b64decode


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

#!/usr/bin/env python3
"""Auth class, requires auth"""

from typing import List, TypeVar
from flask import request


class Auth():
    """ manages the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """requires authentication
        Returns True or False"""
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        if path[-1] != "/":
            path += "/"
        if excluded_paths[-1] != "/":
            excluded_paths += "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Checks the authorisation header for authorisation
        Returns None, or request header"""
        if request is None:
            return None
        if not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """checks current user/session
        Returns the request headers or None"""
        return None

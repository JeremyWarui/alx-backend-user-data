#!/usr/bin/env python3
"""Auth class, requires auth"""

from typing import List, TypeVar
from flask import request


class Auth():
    """ manages the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """requires authentication
        Returns True or False"""
        return False

    def authorization_header(self, request=None) -> str:
        """Checks the authorisation header for authorisation
        Returns None, or request header"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """checks current user/session
        Returns the request headers or None"""
        return None

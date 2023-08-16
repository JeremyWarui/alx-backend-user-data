#!/usr/bin/env python3
"""authentication model"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> str:
    """Returns hashed password in bytes"""
    return hashpw(password.encode("utf-8"), gensalt())

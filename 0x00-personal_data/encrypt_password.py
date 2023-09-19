#!/usr/bin/env python3
"""encrypt password and decrypt password"""
import bcrypt


def hash_password(password: str) -> bytes:
    password = password.encode('utf8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    password = password.encode('utf8')
    return bcrypt.checkpw(password, hashed_password)

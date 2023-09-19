#!/usr/bin/python3
"""encrypt password and decrypt password"""
import bcrypt


def hash_password(password):
    password = password.encode()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


def is_valid(hashed_password, password):
    password = password.encode()
    return bcrypt.checkpw(password, hashed_password)

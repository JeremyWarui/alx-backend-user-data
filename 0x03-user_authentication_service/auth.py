#!/usr/bin/env python3
"""
authentication model.
Register user, create a session, check validation, destroy a session
generate a uuid
"""

from typing import Union
from uuid import uuid4
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> str:
    """Returns hashed password in bytes"""
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """generate uuids"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user. Takes in email and password
        Checks if email was used before and if not
        hash the password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            passwd = _hash_password(password)
            user = self._db.add_user(email, passwd)
            return user
        else:
            raise ValueError("User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """checks the user by email, if found
            check password with bcrypt checkpw.
            if found, returns True otherwise False"""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode("utf-8"),
                           user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """creates a session id using uuid generator and
        assign to user's session id property
        and returns the sessionID"""
        try:
            found_user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(found_user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """get the specific user using a given session ID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroys the session of specific user"""
        try:
            self._db.update_user(user_id=user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """checks if email exists, generate uuid and update the user's
        reset_token property and return the token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound as exc:
            raise ValueError from exc
        r_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=r_token)
        return r_token

    def update_password(self, reset_token: str, password: str) -> None:
        """update_password: takes reset token and password
        Returns: None
        Uses reset_token to find the user and update their password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound as exc:
            raise ValueError from exc
        passwd = _hash_password(password=password)
        self._db.update_user(user.id, hashed_password=passwd, reset_token=None)

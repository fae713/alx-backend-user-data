#!/usr/bin/env python3
"""
Hash Password
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


def _generate_uuid() -> str:
    """
    Generates a user unique ID.
    """
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """
    A method that takes in a password string arguments
    and returns bytes.
    """
    pw_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pw_bytes, salt)

    return hashed_password


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)

            new_user = self._db.add_user(
                email=email, hashed_password=hashed_password)

            return new_user
        else:
            raise ValueError(f"User {email} already exists.")

    def valid_login(self, email: str, password: str) -> bool:
        """
        This method validates login credentials.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        if bcrypt.checkpw(password.encode('utf-8'),
                          user.hashed_password):
            return True
        else:
            return False

    def create_session(self, email: str) -> str:
        """
        This method creates a new session with a user email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        # Generate a new UUID for the session ID
        session_id = str(uuid4())

        self._db.update_user(user_id=user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        This method gets a user from their session ID.
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

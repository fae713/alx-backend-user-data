#!/usr/bin/env python3
"""
Session Authentication.
"""

from flask import request
from .auth import Auth
from typing import List
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    A class that creates a session suthentication.
    """
    user_id_by_session_id = {}

    def __init__(self) -> None:
        super().__init__()
        pass

    def create_session(self, user_id: str = None) -> str:
        """
        A method that creates a Session ID for a user_id.
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This method returns a User ID based on a Session ID.
        """
        if session_id is None:
            return None

        if not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """
        A method that returns a User instance via cookie.
        """
        if request is None:
            return None

        session_id_cookie = self.session_cookie(request)

        if session_id_cookie is None:
            return None

        user_id = self.user_id_for_session_id(session_id_cookie)

        if user_id is None:
            return None

        user = User.get(user_id)

        return user

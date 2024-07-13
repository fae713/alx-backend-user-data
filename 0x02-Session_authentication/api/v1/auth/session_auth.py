#!/usr/bin/env python3
"""
Empty session
"""

from flask import request
from .auth import Auth
from typing import List
import uuid


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

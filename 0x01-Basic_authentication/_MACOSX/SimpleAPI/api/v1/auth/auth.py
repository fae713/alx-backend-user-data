#!/usr/bin/env python3
"""
Auth class task
"""

from flask import request
from typing import List, TypeVar


User = TypeVar('User')


class Auth:
    """
    A class to manage the API authentication.
    """

    def __init__(self) -> None:
        """
        the class init.
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        A method that takes care of the required auth.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        The method that extracts the authorization header from request.
        """
        return None

    def current_user(self, request=None) -> User: 
        """
        The method that gets the current user from the request.
        """
        return None

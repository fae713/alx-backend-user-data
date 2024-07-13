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
        if path is None:
            return True

        if not excluded_paths:
            return True

        normalized_path = path.rstrip('/')
        for excl_path in excluded_paths:
            norm_excl_path = excl_path.rstrip('/')

            if norm_excl_path.endswith('*'):
                prefix_match = norm_excl_path[:-1] == normalized_path[
                    :len(norm_excl_path[:-1])]
                if prefix_match:
                    return False
            elif normalized_path.startswith(norm_excl_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        The method that extracts the authorization header from request.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> User:
        """
        The method that gets the current user from the request.
        """
        return None

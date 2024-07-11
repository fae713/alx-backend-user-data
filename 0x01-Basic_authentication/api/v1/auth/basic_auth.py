#!/usr/bin/env python3
"""
Basic Auth
"""

from flask import request
from typing import List, TypeVar
from .auth import Auth


class BasicAuth(Auth):
    """
    A basic auth class.
    """
    def __init__(self) -> None:
        super().__init__()
        pass

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        This class extracts the base64 auth part from the
        authorization hearder.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ", 1)[1]

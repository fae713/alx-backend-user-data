#!/usr/bin/env python3
"""
Basic Auth
"""

import base64
from flask import request
from typing import List, TypeVar, Tuple
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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decode the Base64 part of the Authorization header.
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extract the user credentials from the decoded
        Base64 Authorization header.
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

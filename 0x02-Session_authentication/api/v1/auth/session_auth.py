#!/usr/bin/env python3
"""
Empty session
"""

from flask import request
from .auth import Auth


class SessionAuth(Auth):
    """
    A class that creates a session suthentication.
    """
    pass

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
    pass

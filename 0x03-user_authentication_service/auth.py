#!/usr/bin/env python3
"""
Hash Password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    A method that takes in a password string arguments
    and returns bytes.
    """
    pw_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pw_bytes, salt)

    return hashed_password

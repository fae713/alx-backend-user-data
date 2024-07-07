#!/usr/bin/env python3
"""
A module for encrypting passwords using bcrypt.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using a random salt with a specified number of rounds.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        bytes: The hashed password.

    Raises:
        TypeError: If the input password is not a string.
        ValueError: If the password is empty.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")
    if not password:
        raise ValueError("Password cannot be empty.")

    return bcrypt.hashpw(
        password.encode('utf-8'), bcrypt.gensalt())


def is_valid_password(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a hashed password matches the given plaintext password.

    Args:
        hashed_password (bytes): The hashed password to compare against.
        password (str): The plaintext password to validate.

    Returns:
        bool: True if the password matches the hash, False otherwise.

    Raises:
        TypeError: If the hashed_password is not bytes
                   or password is not a string.

        ValueError: If the password is empty.
    """
    if not isinstance(hashed_password, bytes):
        raise TypeError("hashed_password must be bytes.")
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")
    if not password:
        raise ValueError("Password cannot be empty.")

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

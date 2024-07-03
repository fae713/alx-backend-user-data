#!/usr/bin/env python3
"""
Regex-ing
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    A function called that returns the log message obfuscated.

    Args:
        fields (list): List of field names to obfuscate.
        redaction (str): String to replace the fields with.
        message (str): Log message to obfuscate.
        separator (str): Character separating fields in the message.

    Returns:
        str: Obfuscated log message.
    """
    pattern = f'({"|".join(fields)}){separator}[^{separator}]*'

    return re.sub(pattern, f'{redaction}{separator}', message)

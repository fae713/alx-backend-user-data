#!/usr/bin/env python3
"""
Regex-ing
"""
import logging
import re

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields_to_redact = fields

    def format(self, record: logging.LogRecord) -> str:
        org_msg = super().format(record)
        filtered_msg = self.filter_datum(
            self.fields_to_redact, self.REDACTION, org_msg, self.SEPARATOR)
        return filtered_msg

    @staticmethod
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

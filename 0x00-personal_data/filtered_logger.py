#!/usr/bin/env python3
"""
Filtered logger module.
"""

import os
import re
import logging
import mysql.connector
from typing import List

# Load environment variables at the start
db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'
    .format('|'.join(map(re.escape, x)), y),

    'replace': lambda x: r'\g<field>={}'.format(x),
}

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction:
                 str, message: str, separator: str) -> str:
    """
    A function that returns unclear log messages.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a LogRecord."""
        msg = super().format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


# Setup logger
logger = logging.getLogger("user_data")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
logger.setLevel(logging.INFO)
logger.propagate = False
logger.addHandler(stream_handler)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connector to a database."""
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main():
    """Logs the information about user records in a table."""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                record = map(lambda x: '{}={}'
                             .format(x[0], x[1]), zip(columns, row))
                msg = '{};'.format('; '.join(list(record)))
                args = ("user_data", logging.INFO, None, None, msg, None, None)
                log_record = logging.LogRecord(*args)
                logger.handle(log_record)
    except Exception as e:
        logger.error(f"Database operation failed: {e}")


if __name__ == "__main__":
    main()

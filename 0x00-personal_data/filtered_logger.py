#!/usr/bin/env python3
"""
filtered logger file for personal data
1. class RedactingFormatter
2. filter_datum function returning log message
3. get_logger function returning logging.Logger
4. get_db function that connects to MySQL database
"""
import re
from typing import List
import logging
from os import getenv
import mysql.connector
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """instantiate the Redacting formatter function"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """filter the from incoming logs"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """function that returns the log message obfudcated"""
    for arg in fields:
        message = re.sub("{}=.*?{}".format(arg, separator),
                         "{}={}{}".format(arg, redaction, separator),
                         message)
    return message


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a mysql connector to the database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connection.MySQLConnection(
            user=username,
            password=password,
            host=host,
            database=database
            )
    return conn


def main():
    """takes no arguments and returns nothing.
    It obtains a database connection using get_db and
    retrieve all rows in the users table and display
    each row under a filtered format"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = []
    for i in cursor.description:
        fields.append(i[0])
    log = get_logger()
    for row in cursor:
        str_row = "".join(f"{f}={str(r)}; " for r, f in zip(row, fields))
        log.info(str_row.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()

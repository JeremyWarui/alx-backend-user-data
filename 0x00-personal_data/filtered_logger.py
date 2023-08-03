#!/usr/bin/env python3
"""
filtered logger file for personal data
"""
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
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

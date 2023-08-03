#!/usr/bin/env python3
"""
filtered logger file for personal data
"""
import re
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


def filter_datum(fields, redaction, message, separator):
    """function that returns the log message obfudcated"""
    for arg in fields:
        message = re.sub(r'{}=.+?{}'.format(arg, separator),
                         '{}={}{}'.format(arg, redaction, separator),
                         message)
    return message

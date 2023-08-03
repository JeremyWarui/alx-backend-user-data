#!/usr/bin/env python3
"""
filtered logger file for personal data
"""
import re


def filter_datum(fields, redaction, message, separator):
    """function that returns the log message obfudcated"""
    for arg in fields:
        message = re.sub(r'{}=.+?{}'.format(arg, separator),
                         '{}={}{}'.format(arg, redaction, separator),
                         message)
    return message

#!/usr/bin/env python3
""" Module for the definition of filter_datum function
"""

import logging
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Function that return the log message obfuscated
    Parameters:
        fields: list of strings representing all fields
        redaction: string representing by what the field will be obfuscated
        message: log message to be in the log line
        separator: character separating all fields
    """
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message

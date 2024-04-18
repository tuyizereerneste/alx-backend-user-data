#!/usr/bin/env python3
""" Module for Authentication
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Initialization of Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Function that handle routes
        that require authentication
        Parameters:
            path: str, allowed for athentication
            excluded_paths: List[str], not allowed for authentication
        Return:
            True or False
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Function that handles authorization header
        Parameter:
            request: None
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """ Function that retrieves current user
        Parameters:
            request
        """
        return None

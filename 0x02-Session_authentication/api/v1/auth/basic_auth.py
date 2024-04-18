#!/usr/bin/env python3
""" Module for basic_auth
"""

import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Initialization of BasicAuth class
    """
    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str) -> str:
        """ Function that extracts base64 authorization
        header
        Parameters:
            authorization_header: str
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        else:
            head = authorization_header.split(' ')[-1]
            return head

    def decode_base64_authorization_header(
                                            self,
                                            base64_authorization_header:
                                            str) -> str:
        """ Function that decodes a header into utf-8
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_data = base64_authorization_header.encode('utf-8')
            decoded_data = base64.b64decode(decoded_data)
            return decoded_data.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Function that Returns user email and password
        from Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Function that return a User instance
        based on email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Function that returns a User instance
        based on a received request
        """
        Auth_header = self.authorization_header(request)
        if Auth_header is not None:
            path_token = self.extract_base64_authorization_header(Auth_header)
            if path_token is not None:
                decoded_dat = self.decode_base64_authorization_header(path_token)
                if decoded_dat is not None:
                    email, pwd = self.extract_user_credentials(decoded_dat)
                    if email is not None:
                        return self.user_object_from_credentials(email, pwd)
        return

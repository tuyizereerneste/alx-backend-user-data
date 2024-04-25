#!/usr/bin/env python3
"""
Hash password function module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union, TypeVar

U = TypeVar(User)


def _generate_uuid() -> str:
    """
    Method that generates a uuid
    """
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """
    Method that hashes the password
    Parameters:
    password(str): user password
    Return:
        hashed password
    """
    pwd_encode = password.encode('utf-8')
    pwd = bcrypt.hashpw(pwd_encode, bcrypt.gensalt())
    return pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Method that register a new user
        Parameters:
            email(str): new user's email
            password(str): new user's password
        Return:
            new user object or raise valueError if user already exists
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            usr = self._db.add_user(email, hashed_pwd)
            return usr
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Method that validates user login
        Parameters:
            email(str): user email
            password(str): user password
        Return:
            True or False
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        user_pwd = user.hashed_password
        pwd = password.encode("utf-8")
        return bcrypt.checkpw(pwd, user_pwd)

    def create_session(self, email: str) -> Union[None, str]:
        """
        Method that create a session_id for an existing user
        and update the user's session_id attribute
        Parameter:
            email (str): user's email address
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """
        Method that taked session id and returns user
        Parameter:
            session_id(str): user session id
        Return:
            user or None if session doesn't exist
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """ Method that destroys user session id
        Parameters:
            user_id(int): user's id
        Return:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Method that generate a UUID and update the user’s
        reset_token database field
        Parameter:
            email(str): user's email
        Return:
            new reset token or value Error
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Method that updates user's password based on token
        Parameters:
            reset_token(str): generated reset token
            password(str): new user password
        Return:
            None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed_pwd = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_pwd,
                             reset_token=None)

#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Method that save a user to the database
        Parameters:
            emait(str): user email
            hashed_password(str): user password
        Return:
            User
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Method the find a user whose attribute is matching the argument
        Parameters:
            attributes
        Return:
            user or error
        """
        all_users = self._session.query(User)
        for k, v in kwargs.items():
            if k not in User.__dict__:
                raise InvalidRequestError
            for u in all_users:
                if getattr(u, k) == v:
                    return u
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Method to update the user attributes
        Parameters:
            user_id(int): user's id to update
            attributes to update
        Return:
            None
        """
        try:
            u = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for k, v in kwargs.items():
            if hasattr(u, k):
                setattr(u, k, v)
            else:
                raise ValueError
        self._session.commit()

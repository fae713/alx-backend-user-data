#!/usr/bin/env python3
"""
DB module
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import InvalidRequestError
from user import User
from user import Base


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

        logging.getLogger(
            'sqlalchemy.engine').setLevel(logging.WARNING)

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
        This adds a new user to the DB.
        """
        new_user = User(email=email, hashed_password=hashed_password)

        try:
            self._session.add(new_user)

            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        This method finds a user with kwargs in the DB.
        """
        try:
            result = self._session.query(User).filter_by(**kwargs).one_or_none()

            if result is None:
                raise NoResultFound(f"No user found matching {kwargs}")
            elif result is not None:
                return result
        except NoResultFound as e:
            raise NoResultFound(f"No user found matching {kwargs}") from e
    
    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes.
        """
        user = self.find_user_by(id=user_id)

        if user is None:
            raise ValueError(f"No user found with ID {user_id}")

        # Update attributes
        for attr_name, attr_value in kwargs.items():
            if hasattr(User, attr_name):
                setattr(user, attr_name, attr_value)
            else:
                raise ValueError(
                    f"Invalid '{attr_name}'.")

        self._session.commit()

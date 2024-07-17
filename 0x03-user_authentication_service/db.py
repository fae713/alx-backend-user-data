#!/usr/bin/env python3
"""
DB module
"""
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
            result = self._session.query(
                User).filter_by(**kwargs).one_or_none()

            if result is None:
                raise NoResultFound(f"No user found matching {kwargs}")
            elif result is not None:
                return result
        except MultipleResultsFound:
            raise NoResultFound(f"Multiple users found matching {kwargs}")
        except InvalidRequestError as e:
            raise InvalidRequestError(f"Invalid request: {str(e)}")

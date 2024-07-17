#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine, tuple_
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
        Finds a user based on a set of filters.
        """
        fields = []
        values = []

        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(key)
                values.append(value)
            else:
                raise InvalidRequestError(f"Invalid field: {key}")

        query = self._session.query(User)
        for field, value in zip(fields, values):
            query = query.filter(getattr(User, field) == value)

        result = query.first()

        if result is None:
            raise NoResultFound("No user found matching the provided filters.")
        return result

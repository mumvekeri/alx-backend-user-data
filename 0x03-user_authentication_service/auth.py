#!/usr/bin/env python3
"""
Definition of _hash_password function
"""
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import (
    TypeVar,
    Union
)

from db import DB
from user import User

U = TypeVar(User)


def _hash_password(password: str) -> bytes:
    """
    Hashes a password string and returns it in bytes form
    Args:
        password (str): The password in string format
    Returns:
        bytes: The hashed password
    """
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate a UUID and return its string representation
    Returns:
        str: The string representation of the UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initialize Auth instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user and return a user object
        Args:
            email (str): New user's email address
            password (str): New user's password
        Returns:
            User: The newly created user object
        Raises:
            ValueError: If a user with the given email already exists
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials and return True if they are correct
        or False if they are not
        Args:
            email (str): User's email address
            password (str): User's password
        Returns:
            bool: True if credentials are correct, else False
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        passwd = password.encode("utf-8")
        return bcrypt.checkpw(passwd, user_password)

    def create_session(self, email: str) -> Union[None, str]:
        """
        Create a session_id for an existing user and update the user's
        session_id attribute
        Args:
            email (str): User's email address
        Returns:
            Union[None, str]: The session ID if created, else None
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
        Takes a session_id and returns the corresponding user, if one exists,
        else returns None
        Args:
            session_id (str): Session ID for user
        Returns:
            Union[None, U]: The user object if found, else None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Take a user_id and destroy that user's session and update their
        session_id attribute to None
        Args:
            user_id (int): User's ID
        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset_token UUID for a user identified by the given email
        Args:
            email (str): User's email address
        Returns:
            str: The newly generated reset_token for the relevant user
        Raises:
            ValueError: If no user with the given email is found
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password
        Args:
            reset_token (str): Reset token issued to reset the password
            password (str): User's new password
        Returns:
            None
        Raises:
            ValueError: If no user with the given reset token is found
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)

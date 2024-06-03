#!/usr/bin/env 
""" Auth class
"""
from flask import request


class Auth:
    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """
        Check if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (list): List of paths that are excluded from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request.

        Args:
            request (flask.Request): The Flask request object.

        Returns:
            str: The authorization header.
        """
        return None

    def current_user(self, request=None):
        """
        Get the current user from the request.

        Args:
            request (flask.Request): The Flask request object.

        Returns:
            TypeVar('User'): The current user.
        """
        return None

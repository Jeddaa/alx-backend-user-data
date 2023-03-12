#!/usr/bin/env python3
""" Module to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    ''' class to manage the API authentication.'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' function to require authentication'''
        # if path in excluded_paths:
        return False


    def authorization_header(self, request=None) -> str:
        ''' function to request authorization'''
        return request


    def current_user(self, request=None) -> TypeVar('User'):
        ''' function to request current user'''
        return request

#!/usr/bin/env python3
""" Module to manage the API authentication
"""
import fnmatch
from flask import request
from typing import List, TypeVar


class Auth:
    ''' class to manage the API authentication.'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' function to require authentication'''
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        else:
            path = path.rstrip('/')
            for excluded_path in excluded_paths:
                excluded_path = excluded_path.rstrip('/')
                if fnmatch.fnmatch(path, excluded_path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        ''' function to request authorization'''
        if request is None:
            return None
        elif request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        ''' function to request current user'''
        return None

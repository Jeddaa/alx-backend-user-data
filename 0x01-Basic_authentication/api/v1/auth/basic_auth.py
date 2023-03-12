#!/usr/bin/env python3
""" Module to manage the API authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import List, TypeVar


import base64


class BasicAuth(Auth):
    """ Basic authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''extract base64 authorization header'''
        if authorization_header is None:
            return None
        elif type(authorization_header) is not str:
            return None
        elif authorization_header.split(' ')[0] != 'Basic':
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        '''Decode base64 authorization header'''
        if base64_authorization_header is None:
            return None
        elif type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(base64_authorization_header
                                    ).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        '''extract_user_credentials'''
        if decoded_base64_authorization_header is None:
            return None, None
        elif type(decoded_base64_authorization_header) is not str:
            return None, None
        elif ':' not in decoded_base64_authorization_header:
            return None, None
        # return decoded_base64_authorization_header.split(':')[0]
        # decoded_base64_authorization_header.split(':')[1]
        user_info = decoded_base64_authorization_header.partition(":")
        email = user_info[0]
        password = user_info[2]

        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''user object from credentials'''
        if user_email is None or type(user_email) is not str:
            return None
        elif user_pwd is None or type(user_pwd) is not str:
            return None
        user = User().search({"email": user_email})
        if not user or user == []:
            return None
        for use in user:
            if use.is_valid_password(user_pwd):
                return use
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request:
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        enc_b64_header = self.extract_base64_authorization_header(auth_header)
        if enc_b64_header is None:
            return None
        de_b64_header = self.decode_base64_authorization_header(enc_b64_header)
        if de_b64_header is None:
            return None
        user_cred = self.extract_user_credentials(de_b64_header)
        if user_cred is None:
            return None
        user = self.user_object_from_credentials(user_cred[0], user_cred[1])
        return user

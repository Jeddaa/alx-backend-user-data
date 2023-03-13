#!/usr/bin/env python3
'''Sesssion authentication module'''
from api.v1.auth.auth import Auth
import uuid

from models.user import User


class SessionAuth(Auth):
    '''A session
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a session ID'''
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        newSessionId = uuid.uuid4()
        self.user_id_by_session_id[str(newSessionId)] = user_id
        return str(newSessionId)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''returns a user_id based on session_id'''
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''return the userId for the current session'''
        # cookie = request.cookies.get('_my_session_id')
        cookie = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        '''destroy the session'''
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        cookie = self.user_id_by_session_id.get(session_cookie)
        if cookie is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True

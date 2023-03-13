#!/usr/bin/env python3
'''Sesssion authentication module'''
from api.v1.auth.session_auth import SessionAuth
import uuid
import os
from datetime import (
    datetime,
    timedelta
)

from models.user import User


class SessionExpAuth(SessionAuth):
    '''Sesssion authentication module'''
    def __init__(self, session_duration=0):
        '''Constructor'''
        self.session_duration = int(os.getenv('SESSION_DURATION'))

    def create_session(self, user_id=None):
        '''create a session'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a user ID based on a session ID
        Args:
            session_id (str): session ID
        Return:
            user id or None if session_id is None or not a string
        """
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if "created_at" not in user_details.keys():
            return None
        if self.session_duration <= 0:
            return user_details.get("user_id")
        created_at = user_details.get("created_at")
        allowed_window = created_at + timedelta(seconds=self.session_duration)
        if allowed_window < datetime.now():
            return None
        return user_details.get("user_id")

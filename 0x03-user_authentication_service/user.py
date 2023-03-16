#!/usr/bin/env python3
'''a user module'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    '''model named user'''
    __tablename__ = 'user'
    id = Column(Integer,  primary_key=True)
    email = Column(String(250),  nullable=False)
    hashed_password = Column(String(250),  nullable=False)
    session_id = Column(String(250), nullable=True)
    rest_token = Column(String(250), nullable=True)

import mysql.connector

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, autoincrement=False, primary_key=True)
    is_bot = Column(Boolean, nullable=False)
    username = Column(String(250), nullable=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=True)


class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, autoincrement=False, primary_key=True)
    type = Column(String(250), nullable=False)
    title = Column(String(250), nullable=False)


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, autoincrement=False, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    type = Column(String(250), nullable=False)
    chat = relationship(Chat)
    user = relationship(User)


class ScheduleType(Base):
    __tablename__ = 'schedule_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(250), nullable=False)


class Command(Base):
    __tablename__ = 'command'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    schedule_type_id = Column(Integer, ForeignKey('schedule_type.id'), nullable=False)
    name = Column(String(250), nullable=False)
    command_id = Column(Integer, ForeignKey('command.id'), nullable=False)
    command_arguments = Column(String(250), nullable=False)
    content = Column(String(250), nullable=False)
    chat = relationship(Chat)
    user = relationship(User)
    command = relationship(Command)




engine = create_engine('mysql+mysqlconnector://user:pass@host/bot')
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
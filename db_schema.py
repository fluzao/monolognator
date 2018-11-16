import mysql.connector

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, BigInteger, DATETIME, TIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import logging
logger = logging.getLogger(__name__)


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

    def __init__(self, id, is_bot, username, first_name, last_name):
        self.id = id
        self.is_bot = is_bot
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class Chat(Base):
    __tablename__ = 'chat'
    id = Column(BigInteger, autoincrement=False, primary_key=True)
    type = Column(String(250), nullable=False)
    title = Column(String(250), nullable=True)

    def __init__(self, id, type, title):
        self.id = id
        self.type = type
        self.title = title


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, autoincrement=False, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey('chat.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    type = Column(String(250), nullable=False)
    content = Column(String(250), nullable=False)
    chat = relationship(Chat)
    user = relationship(User)

    def __init__(self, id, date, type, content, chat, user):
        self.id = id
        self.date = date
        self.type = type
        self.content = content
        self.chat = chat
        self.user = user


class ScheduleType(Base):
    __tablename__ = 'schedule_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(250), nullable=False)

    def __int__(self, type):
        self.type = type


class Command(Base):
    __tablename__ = 'command'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    def __init__(self, name):
        self.name = name


class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey('chat.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(250), nullable=False)
    schedule_type_id = Column(Integer, ForeignKey('schedule_type.id'), nullable=False)
    command_id = Column(Integer, ForeignKey('command.id'), nullable=False)
    command_arguments = Column(String(250), nullable=False)
    content = Column(String(250), nullable=True)
    when = Column(DATETIME, nullable=True)
    time = Column(TIME, nullable=True)
    interval = Column(Integer, nullable=True)
    start_date = Column(DATETIME, nullable=True)
    end_date = Column(DATETIME, nullable=True)
    chat = relationship(Chat)
    user = relationship(User)
    command = relationship(Command)
    schedule_type = relationship(ScheduleType)

    def __init__(self, chat, user, name, schedule_type,
                 command, command_arguments, content,
                 when=None, time=None, interval=None,
                 start_date=None, end_date=None):
        self.chat = chat
        self.user = user
        self.name = name
        self.schedule_type = schedule_type
        self.command = command
        self.command_arguments = command_arguments
        self.content = content
        self.when = when
        self.time = time
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date





def main():

    engine = create_engine('mysql+mysqlconnector://root:root@localhost/bot',
                           encoding='utf8',
                           echo=True,
                           echo_pool=True)
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    commands = ['chuva', 'reminder']
    for c in commands:
        command = Command(name=c)
        session.add(command)
    session.commit()

    schedule_type = ['run_once', 'run_repeating', 'run_daily']
    for st in schedule_type:
        schedule_type = ScheduleType(type=st)
        session.add(schedule_type)
    session.commit()


if __name__ == "__main__":
    main()

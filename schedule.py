from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc
from db_schema import User, Chat, Message, Schedule, ScheduleType, Command
import os
from telegram.ext import Updater
import logging
from weather import chuva
logger = logging.getLogger(__name__)


engine = create_engine('mysql+mysqlconnector://root:root@172.17.0.2/bot',
                       encoding='utf8',
                       echo=False,
                       echo_pool=False)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base = declarative_base()

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


'''        self.id = id
        self.chat = chat
        self.user = user
        self.name = name
        self.schedule_type = schedule_type
        self.interval = interval
        self.command = command
        self.command_arguments = command_arguments
        self.content = content'''


def add_schedule(chat_id, user_id, name, schedule_type, interval, command, command_arguments, content):
    try:
        session = DBSession()
    except exc.DatabaseError as e:
        logger.error('Failed to get DB Session')
        pass
    try:
        # user = get_or_create(session, User, id=user_id)
        # chat = get_or_create(session, Chat, id=chat_id)
        user = session.query(User).filter(User.id == user_id).first()
        chat = session.query(Chat).filter(Chat.id == chat_id).first()
        schedule = Schedule(chat, user, name, schedule_type, interval, command, command_arguments, content)
        session.add(schedule)
        session.commit()
    except (exc.SQLAlchemyError, exc.DBAPIError, exc.OperationalError, exc.DatabaseError) as e:
        logger.error('Log message failed, rolling back')
        session.rollback()
    finally:
        session.close()


def add_schedule_command(bot, update, job_queue, args):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    name, schedule_type, interval, command, command_arguments, content = args.split(',')
    add_schedule(chat_id, user_id, name, ScheduleType(type=schedule_type), interval, Command(name=command), command_arguments, content)
    job_queue.run_once(chuva, int(interval))
    print(args)




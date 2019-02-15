from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc
from db_schema import User, Chat, Message
import logging
logger = logging.getLogger(__name__)


engine = create_engine('mysql+mysqlconnector://bot:bot@localhost/bot',
                       encoding='utf8',
                       echo=True,
                       echo_pool=True)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base = declarative_base()

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def log_message(id, chat_id, user_id, is_bot, username, first_name, last_name, date, type, content, chat_title):
    try:
        session = DBSession()
    except exc.DatabaseError as e:
        logger.error('Failed to get DB Session')
        pass
    try:
        user = get_or_create(session, User, id=user_id, is_bot=is_bot,
                             username=username, first_name=first_name,
                             last_name=last_name)
        chat = get_or_create(session, Chat, id=chat_id, type=type, title=chat_title)
        message = Message(id, date, type, content, chat, user)
        session.add(message)
        session.commit()
    except (exc.SQLAlchemyError, exc.DBAPIError, exc.OperationalError, exc.DatabaseError) as e:
        logger.error('Log message failed, rolling back')
        session.rollback()
    finally:
        session.close()


def get_messages(bot, update):
    user = None
    # user = update.message.from_user.id
    chat = update.message.chat_id
    try:
        session = DBSession()
    except exc.DatabaseError as e:
        logger.error('Failed to get DB Session')
        pass
    try:
        if user:
            for msg in session.query(Message).filter(Message.user_id == user, Message.chat_id == chat):
                print(msg.content)
        else:
            for msg in session.query(Message).filter(Message.chat_id == chat):
                print(msg.content)
    except (exc.SQLAlchemyError, exc.DBAPIError, exc.OperationalError, exc.DatabaseError) as e:
        logger.error('Log message failed, rolling back')
        session.rollback()
    finally:
        session.close()



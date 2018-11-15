from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc
from db_schema import User, Chat, Message
import logging
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



#log_message(session,
#            11111, 22222, 33333, 0, 'bruno', 'bruno', 'savioli', '2018-11-14 01:00:53', 'lalala', 'content', 'test chat')



#
# # Insert a Person in the person table
# new_person = Person(name='new person')
# session.add(new_person)
# session.commit()
#
# # Insert an Address in the address table
# new_address = Address(post_code='00000', person=new_person)
# session.add(new_address)
# session.commit()


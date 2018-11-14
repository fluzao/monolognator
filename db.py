from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import User, Chat, Message

engine = create_engine('mysql+mysqlconnector://user:pass@host/bot')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

def log_message(id, chat_id, user_id, username, first_name, last_name, date, type, chat)

# Insert a Person in the person table
new_person = Person(name='new person')
session.add(new_person)
session.commit()

# Insert an Address in the address table
new_address = Address(post_code='00000', person=new_person)
session.add(new_address)
session.commit()


'''
    id = Column(Integer, autoincrement=False, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    type = Column(String(250), nullable=False)
    chat = relationship(Chat)
    user = relationship(User)'''
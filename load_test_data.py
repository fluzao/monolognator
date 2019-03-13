
from db import log_message, create_session, get_or_create
from db_schema import Message, Chat, User
from math import ceil
from datetime import datetime


def load_test_data(file):
    import json
    with open(file, 'r') as f:
        history = json.load(f)
    msgs = history['chats']['list'][0]['messages']
    return msgs


chat_id = -1001105653255
is_bot = False
username = None
chat_title = "Bolsão do Bolorêncio"
chat_type = 'supergroup'
msgs = load_test_data('./result.json')
objects = list()
session = create_session()
count = 0
for m in msgs:
    if m.get('type') != 'message' or m.get('media_type') is not None or m.get('photo') is not None or m.get('from') is None:
        continue
    if isinstance(m.get('text'), list):
        text = ''.join([t if isinstance(t, str) else t['text'] for t in m.get('text')])
    else:
        text = m.get('text')
    date = m.get('date')
    mid = m.get('id')
    user_id = m.get('from_id')
    username = None
    if ' ' in m.get('from'):
        # print(m.get('from'))
        first = m.get('from').split(' ')[0]
        last = ' '.join(m.get('from').split(' ')[1:])
    else:
        first = m.get('from')
        last = None
    reply_to = m.get('reply_to_message_id')
    # _user = get_or_create(session, User, id=user_id, is_bot=False, username=username, first_name=first, last_name=last)
    # _chat = get_or_create(session, Chat, id=chat_id, type=chat_type, title=chat_title)
    # messaxge = Message(mid, date, text, reply_to, _chat, _user)
    message = Message(mid, chat_id, user_id, date, text, reply_to, is_bot, username, first, last)
    # session.add(message)
    objects.append(message)

# runs = ceil(len(objects) / 50000)
# start = 0
# end = 50000
# print(datetime.now())
# for r in range(0, runs):
#     session.add_all(objects[start:end])
#     print(f'Commiting {start}:{end}')
#
#
#     start = end
#     end += 50000
print(datetime.now())
session.add_all(objects)
print(datetime.now())
session.commit()
print(datetime.now())




    # log_message(mid, chat_id, chat_type, user_id, is_bot, username, first, last, date, text, reply_to, chat_title)

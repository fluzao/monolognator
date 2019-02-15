
from db import log_message


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
msgs = load_test_data('/tmp/result.json')
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

    log_message(mid, chat_id, chat_type, user_id, is_bot, username, first, last, date, text, reply_to, chat_title)

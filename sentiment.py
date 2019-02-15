import re
from nltk.tokenize import WordPunctTokenizer
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from db import get_messages, get_user_id





def clean_messages(msg):
    link_removed = re.sub('https?://[A-Za-z0-9./]+', '', msg)
    number_removed = re.sub('[0-9]+', ' ', link_removed)
    lower_case_msg = number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_msg)
    clean_msg = ' '.join(words).strip()
    return clean_msg


def get_sentiment_score(msg):
    client = language.LanguageServiceClient()
    document = types.Document(content=msg,
                              type=enums.Document.Type.PLAIN_TEXT,
                              language='pt')
    sentiment_score = client.analyze_sentiment(document=document).document_sentiment.score
    return sentiment_score


def analyze_msgs(chat, user):
    score = 0
    msgs = get_messages(chat, user=user)
    total_msg = len(msgs)
    for msg in msgs:
        print(msg)
        # msg = msg.encode('utf-8')
        cleaned_msg = clean_messages(msg)
        sentiment_score = get_sentiment_score(cleaned_msg)
        score += sentiment_score
        print('Msg: {}'.format(cleaned_msg))
        print('Score: {}\n'.format(sentiment_score))
    final_score = round((score / float(total_msg)), 2)
    return final_score, total_msg


def sentiment(bot, update):
    chat = update.message.chat_id
    chat = -1001105653255
    if update.message.text == '/sentiment':
        user = update.message.from_user.id
        name = update.message.from_user.first_name
    else:
        name = update.message.text.split('/sentiment ')[1]
        user = get_user_id(name)
    update.message.reply_text(f'Analysing last 7 days of data for {name}, please wait...')
    score, msgs = analyze_msgs(chat, user)
    if score <= -0.25:
        status = 'NEGATIVE | ❌'
    elif score <= 0.25:
        status = 'NEUTRAL | 🔶'
    else:
        status = 'POSITIVE | ✅'

    bot.send_message(chat_id=chat, text=f'{msgs} messages in the last 7 days\nAverage score for {name}: {score}.\nStatus = {status}')


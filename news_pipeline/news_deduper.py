# -*- coding: utf-8 -*-

import datetime
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client

from cloudAMQP_client import CloudAMQPClient

import yaml

stream = open("../config.yml", "r")
load = yaml.load(stream)
config = load['default']['common']

DEDUPE_NEWS_TASK_QUEUE_URL = config['cloudAMQP']['DEDUPE_NEWS_TASK_QUEUE_URL']
DEDUPE_NEWS_TASK_QUEUE_NAME = config['cloudAMQP']['DEDUPE_NEWS_TASK_QUEUE_NAME']
SLEEP_TIME_IN_SECONDS = config['cloudAMQP']['DEDUPE_SLEEP_TIME_IN_SECONDS']

NEWS_TABLE_NAME = config['mongodb']['NEWS_TABLE_NAME']

# TODO: change the threshold after research
SAME_NEWS_SIMILARITY_THRESHOLD = 0.8

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance (msg, dict) :
        return

    task = msg
    text = str(task['text']).encode('utf-8')

    if text is None:
        return

    # Get all recent news
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    # $lt: less than
    # $gte: greater or equal
    recent_news_list = list(db[NEWS_TABLE_NAME].find({'publishedAt': {'$gte': published_at_day_begin, '$lt': published_at_day_end}}))

    if recent_news_list is not None and len(recent_news_list) > 0:
        documents = [str(news['text']) for news in recent_news_list]
        documents.insert(0, text)
        # Calculate similarity matrix
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        print pairwise_sim.A

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                # Duplicated news. Ignore.
                print "Duplicated news. Ignore."
                return

    task['publishedAt'] = parser.parse(task['publishedAt'])

    # Classify news
    title = task['title']
    if title is not None:
        topic = news_topic_modeling_service_client.classify(title)
        task['class'] = topic

    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print "deduper excepetion"
                print e
                pass

        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

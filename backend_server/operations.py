import json
import os
import pickle
import random
import redis
import sys
from bson.json_util import dumps
from datetime import datetime

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_recommendation_service_client
from cloudAMQP_client import CloudAMQPClient

import yaml

stream = open("../config.yml", "r")
load = yaml.load(stream)

config = load['default']['redis-server']
REDIS_HOST = config['host']
REDIS_PORT = config['port']
USER_NEWS_TIME_OUT_IN_SECONDS = config['USER_NEWS_TIME_OUT_IN_SECONDS']

config = load['default']['common']
MONGO_DB_HOST = config['mongodb']['MONGO_DB_HOST']
MONGO_DB_PORT = config['mongodb']['MONGO_DB_PORT']
DB_NAME = config['mongodb']['DB_NAME']
NEWS_TABLE_NAME = config['mongodb']['NEWS_TABLE_NAME']
CLICK_LOGS_TABLE_NAME = config['mongodb']['CLICK_LOGS_TABLE_NAME']
LOG_CLICKS_TASK_QUEUE_URL = config['cloudAMQP']['LOG_CLICKS_TASK_QUEUE_URL']
LOG_CLICKS_TASK_QUEUE_NAME = config['cloudAMQP']['LOG_CLICKS_TASK_QUEUE_NAME']

config = load['default']
NEWS_LIMIT = config['backend_server']['NEWS_LIMIT']
NEWS_LIST_BATCH_SIZE = config['backend_server']['NEWS_LIST_BATCH_SIZE']

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    db = mongodb_client.get_db()
    user_profile = db['user_preference_model'].find_one({"userId": user_id})
    interests = []
    if 'interest' in user_profile:
        # Get interest for the user
        interests = user_profile['interest']

    # The final list of news to be returned.
    sliced_news = []

    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))

        # If begin_index is out of range, this will return empty list;
        # If end_index is out of range (begin_index is within the range), this
        # will return all remaining news ids.
        sliced_news_digests = news_digests[begin_index:end_index]
        print sliced_news_digests
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        # sort by publishedAt
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))

        # Get preference for the user
        preference = news_recommendation_service_client.getPreferenceForUser(user_id)
        for news in total_news:
            news['level'] = 0
            if preference is not None and len(preference) > 0:
                level = 17
                for item in preference:
                    if news['class'] == item:
                        news['level'] = level
                    level = level-1

        # sort by preference
        for news in total_news:
            for interest in interests:
                if news['class'] == interest:
                    news['level'] = 18

        total_news.sort(key=lambda x:x['level'], reverse=True)

        total_news_digests = map(lambda x:x['digest'], total_news)

        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]

    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    db = mongodb_client.get_db()
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': datetime.utcnow()}
    db[CLICK_LOGS_TABLE_NAME].insert(message)
    # Send log task to machine learning service for prediction
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    cloudAMQP_client.sendMessage(message)

# TODO: initial preference by user + guess you like
# 'interest' means topic chosen by user 'preference' means guess you like
def getPreferenceForUser(userId):
    db = mongodb_client.get_db()
    user_profile = db['user_preference_model'].find_one({"userId": userId})
    if user_profile is not None and 'interest' in user_profile:
        interest = user_profile['interest']
        return json.loads(dumps(interest))
    else:
        return json.loads(dumps({"status": "null"}))

def changePreferenceForUser(userId, message):
    db = mongodb_client.get_db()
    user_profile = db['user_preference_model'].find_one({"userId": userId})
    if user_profile is None:
        print "new profile"
        db['user_preference_model'].insert({
            'userId': userId,
            'interest': message
        })
    else:
        print "change interest!"
        db['user_preference_model'].update_one({
            'userId': userId
        },{
            '$set': {
                'interest': message
            }
        }, upsert=False)
    user_profile = db['user_preference_model'].find_one({"userId": userId})
    return json.loads(dumps(user_profile))



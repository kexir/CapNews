# _*_ coding: utf-8 _*_

import os
import sys
import redis
import hashlib
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient
import yaml

stream = open("../config.yml", "r")
load = yaml.load(stream)

config = load['default']['redis-server']
REDIS_HOST = config['host']
REDIS_PORT = config['port']
NEWS_TIME_OUT_IN_SECOND = config['NEWS_TIME_OUT_IN_SECOND']

config = load['default']['common']
SCRAPE_NEWS_TASK_QUEUE_URL = config['cloudAMQP']['SCRAPE_NEWS_TASK_QUEUE_URL']
SCRAPE_NEWS_TASK_QUEUE_NAME = config['cloudAMQP']['SCRAPE_NEWS_TASK_QUEUE_NAME']
SLEEP_IN_SECOND = config['cloudAMQP']['MONITOR_SLEEP_IN_SECOND']

NEWS_SOURCE = config['news_api_client']['DEFAULT_SOURCES']

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCE)

    num_of_new_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_new_news = num_of_new_news + 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                # 2017-04-07T16:09:35Z formate: YYYY-MM-DDTHH:MM:SS in UTC
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            redis_client.set(news_digest, news)
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECOND)

            cloudAMQP_client.sendMessage(news)

    print "Fetched %d new news" % num_of_new_news
    cloudAMQP_client.sleep(SLEEP_IN_SECOND)


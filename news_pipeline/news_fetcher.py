# -*- coding: utf-8 -*-

import os
import sys
from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import scraper.cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

import yaml

stream = open("../config.yml", "r")
load = yaml.load(stream)
config = load['default']['common']

DEDUPE_NEWS_TASK_QUEUE_URL = config['cloudAMQP']['DEDUPE_NEWS_TASK_QUEUE_URL']
DEDUPE_NEWS_TASK_QUEUE_NAME = config['cloudAMQP']['DEDUPE_NEWS_TASK_QUEUE_NAME']

SCRAPE_NEWS_TASK_QUEUE_URL = config['cloudAMQP']['SCRAPE_NEWS_TASK_QUEUE_URL']
SCRAPE_NEWS_TASK_QUEUE_NAME = config['cloudAMQP']['SCRAPE_NEWS_TASK_QUEUE_NAME']


SLEEP_IN_SECOND = config['cloudAMQP']['FETCHER_SLEEP_IN_SECOND']

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrap_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'msg is broken'
        return
    task = msg

    # text = None
    # We support CNN only now
    # if task['source'] == 'cnn':
    #     print 'Scrapping CNN news'
    #     text = scraper.cnn_news_scraper.extract_news(task['url'])
    # else:
    #     print "news source [%s] is not supported!" % task['source']
    # task['text'] = text


    article = Article(task['url'])
    article.download()
    article.parse()

    print article.text

    task['text'] = article.text

    dedupe_news_queue_client.sendMessage(task)

while True:
    # Fetch message from queue
    if scrap_news_queue_client is not None:
        msg = scrap_news_queue_client.getMessage()
        if msg is not None:
            # Handle message
            try:
                handle_message(msg)
            except Exception as e:
                print "fetcher has exception"
                print e
                pass
        scrap_news_queue_client.sleep(SLEEP_IN_SECOND)

# -*- coding: utf-8 -*-
import requests
import os
import sys
import random

from lxml import html

GET_CNN_NEWS_XPATH = '''//p[@class="zn-body__paragraph"]//text() | //div[@class="zn-body__paragraph"]//text()'''

# load user agent
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')

USER_AGENTS = []


with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])

random.shuffle(USER_AGENTS)

def getHeaders():
    ua = random.choice(USER_AGENTS)
    headers = {
        'Connection' : "close",
        "User-Agent" : ua
    }
    return headers

def extract_news(new_url):
    # Fetch html
    session_requests = requests.session()
    # using session to pretend to be a human instead of machine
    response = session_requests.get(new_url, headers=getHeaders())
    news = {}

    try:
        # Parse html
        tree = html.fromstring(response.content)
        # Extract information
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
    except Exception as e:
        print e
        return {}
    return news


   
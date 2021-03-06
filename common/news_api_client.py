import requests
from json import loads

import yaml

stream = open("../config.yml", "r")
load = yaml.load(stream)
config = load['default']['common']

NEWS_API_ENDPOINT = config['news_api_client']['NEWS_API_ENDPOINT']
NEWS_API_KEY = config['news_api_client']['NEWS_API_KEY']
ARTICLES_API = config['news_api_client']['ARTICLES_API']
SORT_BY_TOP = config['news_api_client']['SORT_BY_TOP']
DEFAULT_SOURCES = config['news_api_client']['DEFAULT_SOURCES']

def buildUrl(end_point=NEWS_API_ENDPOINT, api_name = ARTICLES_API) :
    return end_point + api_name

def getNewsFromSource(sources = DEFAULT_SOURCES, sortBy = SORT_BY_TOP):
    articles = []
    for source in sources:
        payload = {'apiKey' : NEWS_API_KEY,
                   'source' : source,
                   'sortBy' : sortBy}
        response = requests.get(buildUrl(), params=payload)
        res_json = loads(response.content)
        # print res_json

        # Extract info from response
        if (res_json is not None and
                    res_json['status'] == 'ok' and
                    res_json['source'] is not None):
            # populate news
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])
    return articles
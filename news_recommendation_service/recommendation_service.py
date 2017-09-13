import operator
import os
import pyjsonrpc
import sys
import logging
import click_log_processor
from datetime import datetime

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

import yaml

stream = open("../config.yml", "r")
load = yaml.load(stream)
config = load['default']['news_recommendation_server']
SERVER_HOST = config['host']
SERVER_PORT = config['port']

config = load['default']['common']
PREFERENCE_MODEL_TABLE_NAME = config['mongodb']['PREFERENCE_MODEL_TABLE_NAME']

config = load['default']['news_topic_modeling_server']
NUM_OF_CLASSES = config['N_CLASSES']

# Ref: https://www.python.org/dev/peps/pep-0485/#proposed-implementation
# Ref: http://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ Get user's preference in an ordered class list """
    @pyjsonrpc.rpcmethod
    def getPreferenceForUser(self, user_id):
        logger.info('calling news_recommendation_server getPreferenceForUser')
        db = mongodb_client.get_db()
        model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':user_id})
        if model is None:
            return []

        sorted_tuples = sorted(model['preference'].items(), key=operator.itemgetter(1), reverse=True)
        sorted_list = [x[0] for x in sorted_tuples]
        sorted_value_list = [x[1] for x in sorted_tuples]

        # If the first preference is same as the last one, the preference makes
        # no sense.
        if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
            return []

        return sorted_list


# create logger with 'spam_application'
logger = logging.getLogger('news_recommendation_server')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('news_recommendation_server.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('creating an instance of news_recommendation_server')

# Threading HTTP Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()

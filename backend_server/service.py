import json
import pyjsonrpc
import os
import sys
import logging
import operations

sys.path.append(os.path.join(os.path.dirname(__file__),'..','common'))

import yaml

stream = open("../config.yml", "r")
load = yaml.load(stream)
config = load['default']['backend_server']
SERVER_HOST = config['host']
SERVER_PORT = config['port']

class RequestHandler (pyjsonrpc.HttpRequestHandler) :
    """Test method"""
    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser (self, user_id, page_num):
        logger.info('calling backend_server getNewsSummariesForUser')
        return operations.getNewsSummariesForUser(user_id, page_num)

    """ Log user news clicks """
    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id):
        logger.info('calling backend_server logNewsClickForUser')
        return operations.logNewsClickForUser(user_id, news_id)

    @pyjsonrpc.rpcmethod
    def getPreference(self, userId):
        logger.info('calling backend_server getPreference')
        return operations.getPreferenceForUser(userId)

    @pyjsonrpc.rpcmethod
    def updateUserInterest(self, userId, interest):
        logger.info('calling backend_server changePreference')
        return operations.changePreferenceForUser(userId, interest)


# create logger with 'spam_application'
logger = logging.getLogger('backend_server')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('backend_server.log')
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

logger.info('creating an instance of backend_server')

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST,SERVER_PORT ),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server on %s:%d" % (SERVER_HOST,SERVER_PORT)

http_server.serve_forever()

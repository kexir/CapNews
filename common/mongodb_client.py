from pymongo import MongoClient

import yaml

stream = open("../config.yml", "r")
load = yaml.load(stream)

config = load['default']['common']
MONGO_DB_HOST = config['mongodb']['MONGO_DB_HOST']
MONGO_DB_PORT = config['mongodb']['MONGO_DB_PORT']
DB_NAME = config['mongodb']['DB_NAME']

client = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))

# if has variable db else use DB_NAME
# only one client is connected to mongo db
def get_db(db=DB_NAME):
   db = client[db]
   return db

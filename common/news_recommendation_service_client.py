import pyjsonrpc
import yaml

stream = open("../config.yml", "r")
load = yaml.load(stream)
config = load['default']['news_recommendation_server']

URL = config['URL']

# URL = "http://localhost:5050/"

client = pyjsonrpc.HttpClient(url=URL)

def getPreferenceForUser(userId):
    preference = client.call('getPreferenceForUser', userId)
    print "Preference list: %s" % str(preference)
    return preference

def updatePreferenceForUser(userId, news_id):
    preference = client.call('updatePreferenceForUser', userId, news_id)
    print "update preference: %s" % str(preference)
    return preference
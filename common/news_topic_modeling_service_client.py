import pyjsonrpc
import yaml

stream = open("../config.yml", "r")
load = yaml.load(stream)
config = load['default']['news_topic_modeling_server']

URL = config['URL']

# URL = "http://localhost:6060/"

client = pyjsonrpc.HttpClient(url=URL)

def classify(text):
    topic = client.call('classify', text)
    print "Topic: %s" % str(topic)
    return topic

import pika
import json
import yaml

stream = open("../config.yml", "r")
load = yaml.load(stream)
config = load['default']['common']
socket_timeout = config['cloudAMQP']['socket_timeout']

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = socket_timeout
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue=queue_name, passive=True)
        self.queue_len = self.queue.method.message_count

    def sendMessage(self, message) :
        self.channel.basic_publish(exchange='', routing_key= self.queue_name,
                                   body=json.dumps(message))
        print "[X] Sent message to %s: %s" %(self.queue_name, message)
        return

    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame is not None:
            print "[O] Received message from %s: %s" %(self.queue_name,body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            print "No message returned from %s" %self.queue_name
            return None

    #if use sleep in python, no heart_bit, service down
    def sleep(self, seconds):
        self.connection.sleep(seconds)

    def getQueueLength(self):
        return self.queue_len

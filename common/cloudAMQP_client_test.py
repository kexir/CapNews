from cloudAMQP_client import CloudAMQPClient
from repeatedTimer import RepeatedTimer

CLOUDAMQP_URL = "amqp://xlheeaod:VAnc_mOaSE4zq1YqlOaAwdpuyGQrIkn-@clam.rmq.cloudamqp.com/xlheeaod"

TEST_QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)
    sentMsg = {'test': 'demo'}
    client.sendMessage(sentMsg)
    # client.sleep(2)
    receivedMsg = client.getMessage()
    # print receivedMsg
    assert sentMsg==receivedMsg
    len = client.getQueueLength()
    print len
    print 'test_basic passed'

def test_logging():
    print "starting..."
    RepeatedTimer(10, hello) # it auto-starts, no need of rt.start()

def hello():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)
    sentMsg = {'backend_server': 'online'}
    client.sendMessage(sentMsg)
    client.sleep(10)

if __name__ == "__main__":
    # test_basic()
    test_logging()



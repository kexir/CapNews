import click_log_processor
import os
import sys

from datetime import datetime
from sets import Set

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
NEWS_TABLE_NAME = "news"

NUM_OF_CLASSES = 17

# Start MongoDB before running following tests.
def test_basic():
    db = mongodb_client.get_db()
    db[PREFERENCE_MODEL_TABLE_NAME].delete_many({"userId": "qlyu044@gmail.com"})

    msg = {"userId": "qlyu044@gmail.com",
           "newsId": "XHe0M1b3RlpbpU2ttpJgQw==\n",
           "timestamp": str(datetime.utcnow())}

    click_log_processor.handle_message(msg)

    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':'qlyu044@gmail.com'})
    assert model is not None
    assert len(model['preference']) == NUM_OF_CLASSES

    print 'test_basic passed!'


if __name__ == "__main__":
    test_basic()

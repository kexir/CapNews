import tensorflow as tf
import numpy as np
import time
from collections import deque
from six import next
from tensorflow.core.framework import summary_pb2
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'trainer'))

import readers
import news_model

np.random.seed(42)

u_num = 6040 # number of users
i_num = 3952 # number of news
batch_size = 1000
dims = 5 # dimension of data

place_device = "/cpu:0"

def clip(x):
    return np.clip(x, 1.0, 5.0)

def get_data():
    # Prepare training and testing data
    df = readers.read_file('../trainer/ml-1m/ratings.dat')
    rows = len(df)
    df = df.iloc[np.random.permutation(rows)].reset_index(drop=True)
    split_index = int(rows * 0.9)
    train_df = df[0:split_index]
    test_df = df[split_index:].reset_index(drop=True)
    return train_df, test_df

def generate_model(df_train, df_test):
    iter_test = readers.OneEpochIterator([df_test["userId"],df_test["newsId"],df_test["rate"]],batch_size=-1)
    user_batch = tf.placeholder(tf.int32, shape=[None], name="userId")
    item_batch = tf.placeholder(tf.int32, shape=[None], name="newsId")
    rate_batch = tf.placeholder(tf.float32, shape=[None])

    infer,regularizer = news_model.model(user_batch, item_batch, user_num=u_num, item_num=i_num, dim=dims, device=place_device)

    _,train_op= news_model.loss(infer, regularizer, rate_batch, learning_rate=0.1, reg=0.05, device=place_device)

    init_op = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init_op)
        saver = tf.train.Saver()
        check_point = tf.train.get_checkpoint_state('../trainer/model/')
        saver.restore(sess, check_point.model_checkpoint_path)

        test_err2 = np.array([])
        for users, items, rates in iter_test:
            pred_batch = sess.run(infer, feed_dict={user_batch:users, item_batch: items})
            pred_batch = clip(pred_batch)
            test_err2 = np.append(test_err2, np.power(pred_batch-rates,2))
        test_err = np.sqrt(np.mean(test_err2))
        print test_err


train_df, test_df = get_data()
generate_model(train_df, test_df)
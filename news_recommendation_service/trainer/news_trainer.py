import numpy as np
import tensorflow as tf
import time
from collections import deque
from six import next
from tensorflow.core.framework import summary_pb2
import readers
import news_model

np.random.seed(42)

u_num = 6040 # number of users
i_num = 3952 # number of news

batch_size = 1000
dims = 5 # dimension of data
max_epochs = 50

place_device = "/cpu:0"

MODEL_OUTPUT_DIR = './save'

def clip(x):
    return np.clip(x, 1.0, 5.0)

def make_scalar_summary(name, val):
    return summary_pb2.Summary(value=[summary_pb2.Summary.Value(tag=name, simple_value=val)])

def get_data():
    # Prepare training and testing data
    df = readers.read_file('ml-1m/ratings.dat')
    rows = len(df)
    df = df.iloc[np.random.permutation(rows)].reset_index(drop=True)
    split_index = int(rows * 0.9)
    train_df = df[0:split_index]
    test_df = df[split_index:].reset_index(drop=True)
    return train_df, test_df

def generate_model(df_train, df_test):
    sample_per_batch = len(df_train) // batch_size
    iter_train = readers.ShuffleIterator([df_train["userId"],df_train["newsId"],
                                          df_train["rate"]],batch_size=batch_size)
    iter_test = readers.OneEpochIterator([df_test["userId"],df_test["newsId"],df_test["rate"]],batch_size=-1)

    user_batch = tf.placeholder(tf.int32, shape=[None], name="userId")
    item_batch = tf.placeholder(tf.int32, shape=[None], name="newsId")
    rate_batch = tf.placeholder(tf.float32, shape=[None])

    infer,regularizer = news_model.model(user_batch, item_batch, user_num=u_num, item_num=i_num, dim=dims, device=place_device)

    global_step = tf.contrib.framework.get_or_create_global_step()
    _,train_op= news_model.loss(infer, regularizer, rate_batch, learning_rate=0.01, reg=0.05, device=place_device)

    init_op = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init_op)
        saver = tf.train.Saver()
        # summary_writer = tf.summary.FileWriter(logdir="/save", graph=sess.graph)
        print("{} {} {} {}".format("epoch", "train_error", "val_error", "elapsed_time"))
        errors = deque(maxlen=sample_per_batch)
        start = time.time()
        for i in range(max_epochs*sample_per_batch):
            users, items, rates = next(iter_train)
            _, pred_batch = sess.run([train_op, infer], feed_dict={user_batch: users, item_batch: items, rate_batch: rates})
            pred_batch = clip(pred_batch)
            errors.append(np.power(pred_batch-rates,2))
            if i % sample_per_batch == 0:
                train_err = np.sqrt(np.mean(errors))
                test_err2 = np.array([])
                for users, items, rates in iter_test:
                    pred_batch = sess.run(infer, feed_dict={user_batch:users, item_batch: items})
                    pred_batch = clip(pred_batch)
                    test_err2 = np.append(test_err2, np.power(pred_batch-rates,2))
                end = time.time()
                test_err = np.sqrt(np.mean(test_err2))
                print("{:3d} {:f} {:f} {:f}(s)".format(i // sample_per_batch, train_err, test_err,
                                                       end - start))
                # train_err_summary = make_scalar_summary("training_error", train_err)
                # test_err_summary = make_scalar_summary("test_error", test_err)
                # summary_writer.add_summary(train_err_summary, i)
                # summary_writer.add_summary(test_err_summary, i)
                start = end

        saver.save(sess, './model/model')



if __name__ == '__main__':
    df_train, df_test = get_data()
    # print (df_train['userId'].head())
    # print (df_test['userId'].head())
    #
    # print (df_train['rate'].head())
    # print (df_test['rate'].head())
    generate_model(df_train,df_test)

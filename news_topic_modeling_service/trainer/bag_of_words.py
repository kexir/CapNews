import tensorflow as tf
import pandas as pd
from sklearn import metrics
import numpy as np

N_CLASSES = 17
EMBEDDING_SIZE = 40
DATA_SET_FILE = '../labeled_news.csv'
MAX_DOCUMENT_LENGTH = 100

def bag_of_words(n_classes, n_words):
    def bag_of_words_model(features, target):
        target = tf.one_hot(target,n_classes,1,0)
        features = tf.contrib.layers.bow_encoder(
            features, vocab_size=n_words, embed_dim=EMBEDDING_SIZE
        )
        logits = tf.contrib.layers.fully_connected(features,N_CLASSES,activation_fn=None)
        loss = tf.contrib.losses.softmax_cross_entropy(logits, target)
        train_op = tf.contrib.layers.optimize_loss(
            loss,tf.contrib.framework.get_global_step(),optimizer='Adam', learning_rate=0.01)
        return ({
            'class': tf.argmax(logits,1),
            'prob': tf.nn.softmax(logits)
        }, loss, train_op)
    return bag_of_words_model

def main(unused_argv):
    # Prepare training and testing data
    df = pd.read_csv(DATA_SET_FILE, header=None)
    train_df = df[0:400]
    test_df = df.drop(train_df.index)

    # x - news title, y - class
    x_train = train_df[1]
    y_train = train_df[0]
    x_test = test_df[1]
    y_test = test_df[0]

    # Process vocabulary
    vocab_processor = tf.contrib.learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    x_test = np.array(list(vocab_processor.transform(x_test)))

    n_words = len(vocab_processor.vocabulary_)
    print('Total words: %d' % n_words)
    # Build model
    classifier = tf.contrib.learn.Estimator(model_fn=bag_of_words(N_CLASSES, n_words))

    # Train and predict
    classifier.fit(x_train, y_train, steps=10000)

    # Evaluate model
    y_predicted = [
        p['class'] for p in classifier.predict(x_test, as_iterable=True)
        ]

    score = metrics.accuracy_score(y_test, y_predicted)
    print('Accuracy: {0:f}'.format(score))

if __name__ == '__main__':
    # Accuracy: 0.510345
    tf.app.run(main=main)
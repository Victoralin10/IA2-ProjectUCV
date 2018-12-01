#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import tensorflow as tf
import csv
import argparse
import matplotlib.pyplot as plt
import os
import random
import copy


def load_data_set(f_csv):
    if not os.path.exists(f_csv):
        return print('Csv Data-Set not found.')

    features, labels = [], []
    with open(f_csv) as f:
        csv_in = csv.reader(f)
        csv_in.next()
        for row in csv_in:
            labels.append(row[1])
            features.append(row[2:])
    return features, labels


def make_model(tr_features, tr_labels, ts_features, ts_labels, training_epochs, learning_rate, model_dir):
    n_hidden_units_one = 280
    n_hidden_units_two = 300

    n_dim = tr_features.shape[1]
    n_classes = tr_labels.shape[1]
    sd = 1 / np.sqrt(n_dim)

    graph = tf.Graph()
    with graph.as_default():
        x = tf.placeholder(tf.float32, [None, n_dim], name='x')
        y = tf.placeholder(tf.float32, [None, n_classes], name='y')

        w_1 = tf.Variable(tf.random_normal([n_dim, n_hidden_units_one], mean=0, stddev=sd))
        b_1 = tf.Variable(tf.random_normal([n_hidden_units_one], mean=0, stddev=sd))
        h_1 = tf.nn.tanh(tf.matmul(x, w_1) + b_1)

        w_2 = tf.Variable(tf.random_normal([n_hidden_units_one, n_hidden_units_two], mean=0, stddev=sd))
        b_2 = tf.Variable(tf.random_normal([n_hidden_units_two], mean=0, stddev=sd))
        h_2 = tf.nn.sigmoid(tf.matmul(h_1, w_2) + b_2)

        w = tf.Variable(tf.random_normal([n_hidden_units_two, n_classes], mean=0, stddev=sd))
        b = tf.Variable(tf.random_normal([n_classes], mean=0, stddev=sd))
        y_ = tf.nn.softmax(tf.matmul(h_2, w) + b)

        init = tf.global_variables_initializer()

        cost_function = -tf.reduce_sum(y * tf.log(y_))
        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)

        correct_prediction = tf.equal(tf.argmax(y_, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        cost_history = np.empty(shape=[1], dtype=float)
        with tf.Session(graph=graph) as sess:
            sess.run(init)
            for epoch in range(training_epochs):
                _, cost = sess.run([optimizer, cost_function], feed_dict={x: tr_features, y: tr_labels})
                cost_history = np.append(cost_history, cost)
                print('\r', int(epoch*100.0/training_epochs), '% completed', end='')
            print('\rTraining completed.')

            # print(sess.run(b))
            # y_pred = sess.run(tf.argmax(y_, 1), feed_dict={x: ts_features})
            # y_true = sess.run(tf.argmax(ts_labels, 1))
            print("Train accuracy: ", round(sess.run(accuracy, feed_dict={x: tr_features, y: tr_labels}), 3))
            print("Test accuracy: ", round(sess.run(accuracy, feed_dict={x: ts_features, y: ts_labels}), 3))

            inputs = {"x": x, "y": y}
            output = {"y_": y_}
            tf.saved_model.simple_save(sess, model_dir, inputs, output)

    # fig = plt.figure(figsize=(10, 8))
    plt.plot(cost_history)
    plt.axis([0, training_epochs, 0, np.max(cost_history)])
    plt.savefig('training.png')


def one_hot_labels(labels):
    n_labels = len(labels)
    unique_labels = np.unique(labels)
    index = {}
    for i, lbl in enumerate(unique_labels):
        index[lbl] = i
        print(lbl, 'encoded as', i)
    labels = [index[x] for x in labels]
    n_unique_labels = len(unique_labels)
    one_hot_encode = np.zeros((n_labels, n_unique_labels))
    one_hot_encode[np.arange(n_labels), labels] = 1
    return one_hot_encode


def load_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', '-e', type=int, default=1000, help='Number of iterations')
    parser.add_argument('--learning_rate', '-lr', type=float, default=1e-6, help='Learning rate')
    parser.add_argument('--model_dir', '-md', type=str, help='Folder to save model', default='./model')
    parser.add_argument('dataset', type=str, help='Csv file with dataset')
    parser.add_argument('test', type=str, help='CSv file with tests')
    return parser.parse_args()


def main():
    args = load_args()
    print('Loading dataset...')
 
    tr_features, tr_labels = load_data_set(args.dataset)
    tr_labels = one_hot_labels(tr_labels)
    tr_features = np.array(tr_features, dtype=np.float32)

    ts_features, ts_labels = load_data_set(args.test)
    ts_labels = one_hot_labels(ts_labels)
    ts_features = np.array(ts_features, dtype=np.float32)

    print('Running training...')
    make_model(tr_features, tr_labels, ts_features, ts_labels, args.epochs, args.learning_rate, args.model_dir)


if __name__ == "__main__":
    main()

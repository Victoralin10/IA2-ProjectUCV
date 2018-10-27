#!/usr/bin/env python

import numpy as np
import tensorflow as tf
import csv
import argparse
import matplotlib.pyplot as plt
import os
import random


def load_data_set(f_csv):
    if not os.path.exists(f_csv):
        print('Csv Data-Set not found.')
        return

    rows = []
    with open(f_csv) as f:
        csv_in = csv.reader(f)
        csv_in.__next__()
        for row in csv_in:
            rows.append([row[1]] + row[3:])

    def order(a):
        return a[0]

    rows = sorted(rows, key=order)
    rows.append(['end'])

    prev = '-1'
    n_rows, tmp = [], []

    def handle_group(group):
        cp_group = group.copy()
        while len(group) < 2000:
            group.extend(cp_group.copy())
        n_rows.extend(group)

    for row in rows:
        if row[0] == prev:
            tmp.append(row)
        else:
            if len(tmp) > 0:
                handle_group(tmp)
            tmp = [row]
        prev = row[0]

    random.shuffle(n_rows)
    features, labels = [], []
    for row in n_rows:
        labels.append(row[0])
        features.append(row[1:])
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
    return parser.parse_args()


def main():
    args = load_args()
    print('Loading dataset...')
    data_features, data_tags = load_data_set(args.dataset)
    # data_features, data_tags = balance_data(data_features, data_tags)

    data_tags = one_hot_labels(data_tags)
    data_features = np.array(data_features, dtype=np.float32)

    total_cnt = len(data_features)
    training_cnt = int(total_cnt*0.7)

    tr_features, tr_labels = data_features[0:training_cnt], data_tags[0:training_cnt]
    ts_features, ts_labels = data_features[training_cnt:], data_tags[training_cnt:]
    print('Running training...')
    make_model(tr_features, tr_labels, ts_features, ts_labels, args.epochs, args.learning_rate, args.model_dir)


if __name__ == "__main__":
    main()

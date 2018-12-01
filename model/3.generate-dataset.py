#!/usr/bin/env python

import argparse
import os
import csv
import random
import pandas
import numpy as np
import util


def load_samples(file_in):
    f_in = open(file_in)
    csv_in = csv.reader(f_in)
    headers = csv_in.next()

    samples = []
    for row in csv_in:
        sample = {}
        for i in range(len(headers)):
            sample[headers[i]] = row[i]
        samples.append(sample)

    f_in.close()
    return samples, headers


def run_abs(samples, headers, file_out):
    with open(file_out, 'w') as f1:
        csv_out = csv.writer(f1)
        header = ['id', 'same-person']
        header.extend(headers[3:])
        csv_out.writerow(header)

        for i in range(len(samples)):
            for j in range(i+1, len(samples)):
                s1 = samples[i]
                s2 = samples[j]

                row = [s1['id']+'-'+s2['id'], s1['person']==s2['person']]
                for f in headers[3:]:
                    row.append(abs(float(s1[f]) - float(s2[f])))
                csv_out.writerow(row)


def run(file_in, prop, training_out, test_out):
    if not os.path.exists(file_in):
        raise Exception('Csv file with features not found.')

    if prop < 0 or prop > 1:
        prop = 0.7

    util.normalize_train(file_in, 'norm' + file_in)
    samples, headers = load_samples('norm' + file_in)
    random.shuffle(samples)

    n = int(len(samples)*prop)
    samples1 = samples[0:n]
    samples2 = samples[n:]
    run_abs(samples1, headers, training_out)
    run_abs(samples2, headers, test_out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, default='features.csv', help='Csv file with features.')
    parser.add_argument('--split', '-s', type=float, default=0.7, help='Spli. Default 0.7 (70%).')
    parser.add_argument('--output_training', '-o1', type=str, default='training.csv', help='Csv file with samples to training.')
    parser.add_argument('--output_test', '-o2', type=str, default='test.csv', help='Csv file with samples to test.')

    args = parser.parse_args()
    run(args.input, args.split, args.output_training, args.output_test)


if __name__ == "__main__":
    main()

#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import argparse
import os
import librosa
import boto3
import json
import pandas
import json
import csv
import random
import copy


features_names = []
for tp, length in [('mfccs', 40), ('chroma', 12), ('mel', 128), ('contrast', 7), ('tonnetz', 6)]:
    features_names.extend([tp + str(x) for x in range(length)])


zmean = json.load(open('z.json'))


def extract_feature(file_name):
    audio, sample_rate = librosa.load(file_name)
    stft = np.abs(librosa.stft(audio))

    mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(audio, sr=sample_rate).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(audio), sr=sample_rate).T, axis=0)
    return mfccs, chroma, mel, contrast, tonnetz


def features_dict(file_name):
    feats = []
    for feat in extract_feature(file_name):
        feats.extend(feat)
    ans = {}
    for i in range(len(features_names)):
        ans[features_names[i]] = feats[i]
    return ans


def balance_data(f_csv):
    if not os.path.exists(f_csv):
        return print('Csv Data-Set not found.')

    rows = []
    with open(f_csv) as f:
        csv_in = csv.reader(f)
        headers = csv_in.next()
        for row in csv_in:
            rows.append(row[1:])

    def order(a):
        return a[0]

    rows = sorted(rows, key=order)
    rows.append(['end'])

    prev = '-1'
    n_rows, tmp = [], []
    groups = []

    def handle_group(group, mx_len):
        cp_group = copy.copy(group)
        while len(group) < mx_len:
            group.extend(copy.copy(cp_group))
        n_rows.extend(group)

    for row in rows:
        if row[0] == prev:
            tmp.append(row)
        else:
            if len(tmp) > 0:
                groups.append(tmp)
            tmp = [row]
        prev = row[0]

    mx_len = max(len(groups[0]), len(groups[1]))
    handle_group(groups[0], mx_len)
    handle_group(groups[1], mx_len)

    random.shuffle(n_rows)
    with open('bal-' + f_csv, 'w') as f:
        csv_out = csv.writer(f)
        csv_out.writerow(headers)
        ind = 0
        for row in n_rows:
            csv_out.writerow([ind] + row)
            ind += 1


def normalize_train(file, fout=None):
    df = pandas.read_csv(file, index_col=0)

    z = {}
    for feature in features_names:
        z[feature] = {
            'mean': df[feature].mean(),
            'stdev': df[feature].std()
        }
        df[feature] = (df[feature] - z[feature]['mean'])/z[feature]['stdev']
    
    json.dump(z, open('z.json', 'w'), ensure_ascii=False, indent=2)

    if fout is None:
        fout = 'norm-' + file
    df.to_csv(fout)


def normalize_test(file, fout=None):
    df = pandas.read_csv(file, index_col=0)
    z = json.load(open('z.json'))

    for feature in features_names:
        df[feature] = (df[feature] - z[feature]['mean'])/z[feature]['stdev']
    
    if fout is None:
        fout = 'norm-' + file
    df.to_csv(fout)

def main():
    normalize_train('training.csv')
    normalize_test('test.csv')

if __name__ == "__main__":
    main()

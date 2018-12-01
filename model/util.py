#!/usr/bin/env python

import numpy as np
import argparse
import os
import librosa
import boto3
import json
import pandas
import json


features_names = []
for tp, length in [('mfccs', 40), ('chroma', 12), ('mel', 128), ('contrast', 7), ('tonnetz', 6)]:
    features_names.extend([tp + str(x) for x in range(length)])


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


def normalize_train(file):
    df = pandas.read_csv(file, index_col=0)

    z = {}
    for feature in features_names:
        z[feature] = {
            'mean': df[feature].mean(),
            'stdev': df[feature].std()
        }
        df[feature] = (df[feature] - z[feature]['mean'])/z[feature]['stdev']
    
    json.dump(z, open('z.json', 'w'), ensure_ascii=False, indent=2)
    df.to_csv('norm-' + file)


def normalize_test(file):
    df = pandas.read_csv(file, index_col=0)
    z = json.load(open('z.json'))

    for feature in features_names:
        df[feature] = (df[feature] - z[feature]['mean'])/z[feature]['stdev']
    
    df.to_csv('norm-' + file)


def main():
    normalize_train('training.csv')
    normalize_test('test.csv')

if __name__ == "__main__":
    main()

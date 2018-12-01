#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import argparse
import os
import librosa
import boto3
import json


def extract_feature(file_name):
    audio, sample_rate = librosa.load(file_name)
    stft = np.abs(librosa.stft(audio))

    mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(audio, sr=sample_rate).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(audio), sr=sample_rate).T, axis=0)
    return mfccs, chroma, mel, contrast, tonnetz


def get_features(audio_file):
    features = extract_feature(audio_file)
    ans = []
    for feat in features:
        ans.extend(feat)
    return ans


def check(audio1, audio2):
    if not os.path.exists(audio1):
        return print("Audio1 file does not exist.")
    if not os.path.exists(audio2):
        return print("Audio2 fiel does not exist.")

    features1 = get_features(audio1)
    features2 = get_features(audio2)
    query_features = []
    for i in range(len(features1)):
        query_features.append(abs(features1[i] - features2[i]))
    feat_names = []
    for tp, length in [('mfcss', 40), ('chroma', 12), ('mel', 128), ('contrast', 7), ('tonnetz', 6)]:
        feat_names.extend([tp + str(x) for x in range(length)])
    
    record = {}
    for i in range(len(query_features)):
        record[feat_names[i]] = str(query_features[i])
    record['id'] = '1'

    client = boto3.client('machinelearning')
    response = client.predict(MLModelId="ml-Wqrg1MNDzTW", Record=record, PredictEndpoint="https://realtime.machinelearning.us-east-1.amazonaws.com")
    ans = response['Prediction']['predictedLabel']
    prob = response['Prediction']['predictedScores'][ans]
    prob = round(prob*100, 2)

    # print(json.dumps(response, indent=2))
    if ans == "1":
        print("Same person with %{0} probabilities.".format(prob))
    else:
        print("Diferent person with %{0} probabilities.".format(100 - prob))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('audio1', type=str, help='Audio file 1')
    parser.add_argument('audio2', type=str, help='Audio file 2')
    args = parser.parse_args()
    check(args.audio1, args.audio2)


if __name__ == "__main__":
    main()

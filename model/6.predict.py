#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import argparse
import os
import librosa
import boto3
import json
import util


def check(audio1, audio2):
    if not os.path.exists(audio1):
        return print("Audio1 file does not exist.")
    if not os.path.exists(audio2):
        return print("Audio2 fiel does not exist.")

    features1 = util.features_dict(audio1)
    features1 = util.normalize_feature(features1)

    features2 = util.features_dict(audio2)
    features2 = util.normalize_feature(features2)

    record = {}
    for feat in util.features_names:
        record[feat] = str(abs(features1[feat] - features2[feat]))
    record['id'] = '1'

    client = boto3.client('machinelearning')
    response = client.predict(MLModelId="ml-wp93CRI1IxD", Record=record, PredictEndpoint="https://realtime.machinelearning.us-east-1.amazonaws.com")
    ans = response['Prediction']['predictedLabel']
    prob = response['Prediction']['predictedScores'][ans]
    prob = round(prob*100, 2)

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

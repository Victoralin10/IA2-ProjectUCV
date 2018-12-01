#!/usr/bin/env python

from __future__ import print_function
import argparse
import librosa
import os
import numpy as np
import pandas as pd


def get_list_files(source_folder):
    if not os.path.isdir(source_folder):
        raise Exception('Source folder not found')

    ans = []
    for fname in os.listdir(source_folder):
        name, ext = fname.split('.')
        if ext != 'wav':
            continue

        person, city, nid = name.split('_')
        ans.append({
            'file': os.path.join(source_folder, fname),
            'person': person,
            'city': city,
            'nro': nid
        })
    return ans


def extract_feature(file_name):
    audio, sample_rate = librosa.load(file_name)
    stft = np.abs(librosa.stft(audio))

    mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(audio, sr=sample_rate).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(audio), sr=sample_rate).T, axis=0)
    return mfccs, chroma, mel, contrast, tonnetz


def run(source_folder, dest_file):
    # Headers
    headers = ['person', 'city', 'nro']
    for tp, length in [('mfcss', 40), ('chroma', 12), ('mel', 128), ('contrast', 7), ('tonnetz', 6)]:
        headers.extend([tp + str(x) for x in range(length)])

    # Listing files
    files = get_list_files(source_folder)
    data = []

    cnt = 1
    for faud in files:
        try:
            features = extract_feature(faud['file'])
            n_row = [faud['person'], faud['city'], faud['nro']]
            for feat in features:
                n_row.extend(feat)

            data.append(n_row)
            print("{0} of {1}".format(cnt, len(files)), end='\r')
            cnt += 1
        except Exception as ex:
            print(faud['file'], str(ex))
    print("")
    data_frame = pd.DataFrame(data, columns=headers)
    data_frame.to_csv(dest_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', '-o', type=str, help='Csv with features', default='features.csv')
    parser.add_argument('source', type=str, help='Folder with wav records.')
    args = parser.parse_args()
    run(args.source, args.out)


if __name__ == "__main__":
    main()

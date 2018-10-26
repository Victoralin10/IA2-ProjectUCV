#!/usr/bin/env python

import argparse
import librosa
import os


def run(source_folder, dest_folder):
    if not os.path.exists(source_folder) or not os.path.isdir(source_folder):
        return print("Source folder not found.")
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    
    for fname in os.listdir(source_folder):
        fpath = os.path.join(source_folder, fname)
        fdest = os.path.join(dest_folder, fname.lower())

        if fpath.endswith('.wav'):
            os.rename(fpath, fdest)
        else:
            fdest = fdest.replace(fname.split('.')[-1], 'wav')
            y, sr = librosa.load(fpath)
            librosa.output.write_wav(fdest, y, sr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help='Folder with original data.')
    parser.add_argument('dest', type=str, help='Folder where wav files will be saved.')

    args = parser.parse_args()
    run(args.source, args.dest)


if __name__ == "__main__":
    main()

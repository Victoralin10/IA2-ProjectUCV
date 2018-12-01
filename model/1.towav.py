#!/usr/bin/env python

import argparse
import soundfile
import os


def run(source_folder, dest_folder):
    if not os.path.exists(source_folder) or not os.path.isdir(source_folder):
        print("Source folder not found.")
        return
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)

    next_id = 1
    id_map = {}

    for fname in os.listdir(source_folder):
        fpath = os.path.join(source_folder, fname)

        aux = fname.split('.')[0].split('_')
        person_name, city = aux[0], aux[1]
        city = city.strip()
        if person_name not in id_map:
            id_map[person_name] = 'person' + str(next_id)
            next_id += 1
        fname = id_map[person_name] + '_' +  city + '.wav'
        fdest = os.path.join(dest_folder, fname.lower())

        if os.path.exists(fdest):
            continue

        if fpath.endswith('.wav'):
            with open(fpath, 'rb') as f1:
                with open(fdest, 'wb') as f2:
                    f2.write(f1.read())
        else:
            try:
                fdest = fdest.replace(fname.split('.')[-1], 'wav')
                y, sr = soundfile.read(fpath)
                soundfile.write(fdest, y, sr)
            except Exception as e:
                print("Error: ", fpath)
                print(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help='Folder with original data.')
    parser.add_argument('dest', type=str, help='Folder where wav files will be saved.')

    args = parser.parse_args()
    run(args.source, args.dest)


if __name__ == "__main__":
    main()

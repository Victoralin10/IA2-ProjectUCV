#!/usr/bin/env python

import argparse
import os
import csv


def load_samples(file_in):
    f_in = open(file_in)
    csv_in = csv.reader(f_in)
    headers = csv_in.__next__()

    samples = []
    for row in csv_in:
        sample = {}
        for i in range(len(headers)):
            sample[headers[i]] = row[i]
        samples.append(sample)

    f_in.close()
    return samples, headers


def run_join(samples, headers, file_out):
    with open(file_out, 'w') as f1:
        csv_out = csv.writer(f1)
        header = ['id', 'same-person']
        header.extend(['1_' + x for x in headers[4:]])
        header.extend(['2_' + x for x in headers[4:]])
        csv_out.writerow(header)

        for i in range(len(samples)):
            for j in range(i+1, len(samples)):
                s1 = samples[i]
                s2 = samples[j]

                row = [s1['id']+'-'+s2['id'], s1['person']==s2['person']]
                for f in headers[4:]:
                    row.append(float(s1[f]))
                for f in headers[4:]:
                    row.append(float(s2[f]))
                csv_out.writerow(row)


def run_abs(samples, headers, file_out):
    with open(file_out, 'w') as f1:
        csv_out = csv.writer(f1)
        header = ['id', 'same-person']
        header.extend(headers[4:])
        csv_out.writerow(header)

        for i in range(len(samples)):
            for j in range(i+1, len(samples)):
                s1 = samples[i]
                s2 = samples[j]

                row = [s1['id']+'-'+s2['id'], s1['person']==s2['person']]
                for f in headers[4:]:
                    row.append(abs(float(s1[f]) - float(s2[f])))
                csv_out.writerow(row)


def run(file_in, file_out, merge):
    if not os.path.exists(file_in):
        raise Exception('Csv file with features not found.')

    samples, headers = load_samples(file_in)
    if merge:
        run_abs(samples, headers, file_out)
    else:
        run_join(samples, headers, file_out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, default='features.csv', help='Csv file with features.')
    parser.add_argument('--output', '-o', type=str, default='dataset.csv', help='Csv file with dataset.')
    parser.add_argument('--merge', '-m', default=False, help='Indicate if the features will be merged.', action='store_true')
    args = parser.parse_args()
    run(args.input, args.output, args.merge)


if __name__ == "__main__":
    main()

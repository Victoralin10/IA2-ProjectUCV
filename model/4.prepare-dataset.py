#!/usr/bin/env python

import util


def main():
    util.balance_data('training.csv')
    util.balance_data('test.csv')

    util.normalize_train('bal-training.csv', 'norm-training.csv')
    util.normalize_test('bal-test.csv', 'norm-test.csv')


if __name__ == "__main__":
    main()


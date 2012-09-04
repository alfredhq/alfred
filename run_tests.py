#!/usr/bin/env python
import os
import nose


TESTS_DIR = os.path.join(os.path.dirname(__file__), 'tests')
if os.environ.get('TRAVIS'):
    CONFIG = os.path.join(TESTS_DIR, 'travis.yml')
else:
    CONFIG = os.path.join(TESTS_DIR, 'config.yml')


def main():
    os.environ.setdefault('ALFRED_TEST_CONFIG', CONFIG)
    nose.run()


if __name__ == '__main__':
    main()

#Alfred

[![Build Status](https://secure.travis-ci.org/alfredhq/alfred.png?branch=develop)](http://travis-ci.org/alfredhq/alfred)

##Instructions

Due to some database specific features, you need to run postgresql locally.

1. Clone this repo
2. In your virtualenv `pip install -r requirements/development.txt`
3. `alfred shell` launches shell
4. `alfred runserver` launches server on 5000 port.

## Tests

To launch tests you must create database named `alfred_test`. Then, execute `nosetests`.

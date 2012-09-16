#Alfred

[![Build Status](https://secure.travis-ci.org/alfredhq/alfred.png?branch=develop)](http://travis-ci.org/alfredhq/alfred)

##Instructions

1. Clone this repo
2. In your virtualenv `pip install -r requirements.txt`
3. `alfred shell` launches shell
4. `alfred runserver` launches server on 5000 port.


Example config file placed in example dir. You can pass path to config file
with `--config` parameter, or set it to `ALFRED_CONFIG` env variable.

To launch tests execute `nosetests`

#!/bin/sh

set -e
cd /io

eval "$(pyenv init -)"
pyenv local 3.5.2

python setup.py clean

rm -rf dist build tick.egg-info

#!/bin/sh

set -e

yum update -y

cd /io

eval "$(pyenv init -)" 
export TICK_CMAKE=cmake28

#rm -rf dist build tick.egg-info

for PYBIN in "3.4.5" "3.5.2"; do
	pyenv local $PYBIN
	python -V
	python setup.py cpplint build pytest bdist_wheel
done

for whl in dist/*.whl; do
	auditwheel repair "$whl" -w /io/dist/wheelhouse
done

#!/bin/sh
pip install -U tox==2.3.0 coveralls==1.1
coverage erase
tox
coverage combine
coverage report -m
coverage html

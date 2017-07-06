#!/bin/sh
pip install -U tox coveralls
coverage erase
tox
coverage combine
coverage report -m
coverage html

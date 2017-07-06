# -*- coding: utf-8 -*-
# Copyright (c) 2016 by Alberto Vara <a.vara.1986@gmail.com>
from __future__ import absolute_import

import codecs
import os

from setuptools import setup, find_packages

version = __import__('avython').__version__
author = __import__('avython').__author__
author_email = __import__('avython').__email__

if os.path.exists('README.rst'):
    long_description = codecs.open('README.rst', 'r', 'utf-8').read()
else:
    long_description = 'See https://github.com/avara1986/avython'

setup(
    name="avython",
    version=version,
    author=author,
    author_email=author_email,
    description="Common resources to extend python code",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
    platforms=["any"],
    keywords="avython",
    url='https://github.com/avara1986/avython.git',
    test_suite='nose.collector',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gitautotag = avython.gitautotag:GitAutotag'
        ]
    },
    scripts=['avython/gitautotag/gitautotag.py'],
    install_requires=[
        'awscli',
        'pathlib'
    ],
    include_package_data=True,
    zip_safe=False,
)

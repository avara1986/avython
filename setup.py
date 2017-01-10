# -*- coding: utf-8 -*-
# Copyright (c) 2016 by Alberto Vara <a.vara.1986@gmail.com>


import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="avython",
    version="0.0.1",
    author="Alberto Vara",
    author_email="a.vara.1986@gmail.com",
    description="Common resources to extend python code",
    long_description=(read('README.rst') + '\n\n' + read('CHANGES.rst')),
    classifiers=[
        'Development Status :: 0.2 - Beta',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        'License :: MIT',
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    license="MIT",
    platforms=["any"],
    keywords="avython",
    url='https://github.com/avara1986/python-utils.git',
    test_suite='nose.collector',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
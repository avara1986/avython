# -*- coding: utf-8 -*-
# Copyright (c) 2016 by Alberto Vara <a.vara.1986@gmail.com>
from __future__ import absolute_import
import os
import sys
import site
from setuptools import setup, find_packages
from distutils.command.install import install


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


def binaries_directory():
    """Return the installation directory, or None"""
    if '--user' in sys.argv:
        paths = (site.getusersitepackages(),)
    else:
        py_version = '%s.%s' % (sys.version_info[0], sys.version_info[1])
        paths = (s % (py_version) for s in (
            sys.prefix + '/lib/python%s/dist-packages/',
            sys.prefix + '/lib/python%s/site-packages/',
            sys.prefix + '/local/lib/python%s/dist-packages/',
            sys.prefix + '/local/lib/python%s/site-packages/',
            '/Library/Python/%s/site-packages/',
        ))

    for path in paths:
        if os.path.exists(path):
            return path
    print('no installation path found', sys.stderr)
    return None


def add_script_as_command(command, *args):
    path = binaries_directory()
    command_to_write = command + "=" + os.path.join(path, "avython", *args)
    alias_line = "alias " + command_to_write
    command_line = command_to_write
    bashrc_path = os.path.expanduser('~/.bashrc')
    with open(bashrc_path, 'r+') as file:
        bashrc_text = file.read()
        if alias_line not in bashrc_text:
            file.write('\n{}\n'.format(alias_line))
        if command_line not in bashrc_text:
            file.write('\n{}\n'.format(command_line))


class post_install(install):

    def run(self):
        install.run(self)

        add_script_as_command("autotag", "gitautotag", "main.py")


setup(
    name="avython",
    version="0.0.1",
    author="Alberto Vara",
    author_email="a.vara.1986@gmail.com",
    description="Common resources to extend python code",
    long_description=(read('README.rst') + '\n\n' + read('CHANGES.rst')),
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
    include_package_data=True,
    zip_safe=False,
    cmdclass={'install': post_install},
)

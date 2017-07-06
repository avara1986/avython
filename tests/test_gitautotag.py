# encoding: utf-8
from __future__ import absolute_import
from copy import copy
import unittest
import os
import subprocess

from avython.gitautotag import GitAutotag


class GitAutotagTest(unittest.TestCase):

    def test_init(self):
        git = GitAutotag(arguments=['-v fake', '-f'])
        self.assertTrue(git.increase_or_create(), "fake0.0.0")

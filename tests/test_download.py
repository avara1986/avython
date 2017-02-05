# encoding: utf-8
from __future__ import absolute_import
from copy import copy
import unittest
import os
import subprocess

from avython.download import Download


class DownloadTest(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(__file__)
        self.host_dir = os.path.join(self.base_dir, "runtests")
        self.tmp_dir = os.path.join(self.base_dir, "tmp")
        self.file = "example.html"
        self.file_zip = "example.zip"

        self.options = {
            'method': "wget",

            'host_path': self.host_dir,
            'host_tmp_path': self.tmp_dir,

            'remote_path': "https://s3-eu-west-1.amazonaws.com/cosas-varias/",
            'remote_file': "example.zip",

            'unzip': True,
            'move_to_tmp': True,
            "noinput": True,
        }

    def test_wget_tmp_folder_unzip_move(self):
        down = Download(**self.options)

        down.get()

        self.host_file = os.path.join(self.host_dir, self.file)
        self.tmp_file = os.path.join(self.tmp_dir, self.file_zip)

        self.assertTrue(self.check_file(self.host_file))
        self.assertTrue(self.check_file(self.tmp_file))
        os.remove(self.host_file)
        os.remove(self.tmp_file)
        self.assertFalse(self.check_file(self.host_file))
        self.assertFalse(self.check_file(self.tmp_file))

    def test_wget_tmp_folder_move(self):
        options = copy(self.options)
        options['unzip'] = False

        down = Download(**options)

        down.get()

        self.host_file = os.path.join(self.host_dir, self.file_zip)
        self.tmp_file = os.path.join(self.tmp_dir, self.file_zip)

        self.assertTrue(self.check_file(self.host_file))
        self.assertTrue(self.check_file(self.tmp_file))
        os.remove(self.host_file)
        os.remove(self.tmp_file)
        self.assertFalse(self.check_file(self.host_file))
        self.assertFalse(self.check_file(self.tmp_file))

    def test_wget_min_fields(self):
        options = {
            'remote_path': "https://s3-eu-west-1.amazonaws.com/cosas-varias/",
            'remote_file': "example.zip",

            'unzip': True,
            'move_to_tmp': True,
            "noinput": True,
        }

        down = Download(**options)

        down.get()
        self.assertTrue(self.check_file(self.file))
        os.remove(self.file)
        self.assertFalse(self.check_file(self.file))

    def check_file(self, file):
        return os.path.isfile(file)

    def check_dir(self, dir):
        return os.path.isdir(dir)

    def remove_file(self, file):
        process = subprocess.Popen(
            "rm -r {} ".format(file),
            shell=True
        )
        process.wait()


if __name__ == '__main__':
    unittest.main()

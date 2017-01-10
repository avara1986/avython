#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from importlib import import_module
import datetime
from distutils.dir_util import mkpath
import shutil
from pathlib import Path
import logging
import os
import subprocess

from avython.console import show_error, check_continue

logging.basicConfig(filename='log.log', level=logging.DEBUG)
log = logging.getLogger('avython')


class Download(object):
    def __init__(self, * args, **kwargs):
        self.unzip = kwargs.get('unzip', True)
        self.move_to_tmp = kwargs.get('tmp', True)
        self.noinput = kwargs.get('noinput', True)
        self.force_download = kwargs.get('force_download', True)

        self.host_path = kwargs.get('host_path', os.path.join(str(Path().resolve()), ""))
        self.host_file = kwargs.get('host_file', "")

        self.host_tmp_path = kwargs.get('host_tmp_path', "/tmp/")
        self.host_tmp_file = kwargs.get('remote_file', "")

        self.remote_path = kwargs.get('remote_path', "")
        self.remote_file = kwargs.get('remote_file', "")

        method_module = 'avython.download.{}'.format(kwargs.get('method', "wget"))
        method = import_module(method_module)
        self._method = method.Driver()

    @property
    def host_path(self):
        self.check_emtpy(self.__host_path, "No host path")
        return self.__host_path

    @host_path.setter
    def host_path(self, value):
        self.__host_path = value

    @property
    def host_file(self):
        self.check_emtpy(self.__host_file, "No host file")
        return self.__host_file

    @host_file.setter
    def host_file(self, value):
        self.__host_file = value

    def get_host_tmp_path(self):
        self.check_emtpy(self.host_tmp_path, "No host path")
        return self.host_tmp_path

    def get_host_tmp_file(self):
        return self.host_tmp_file

    def get_remote_path(self):
        self.check_emtpy(self.remote_path, "No remote path")
        return self.remote_path

    def get_remote_file(self):
        return self.remote_file

    def check_emtpy(self, variable_to_check, error_msg):
        if not variable_to_check and not self.noinput:
            check_continue(error_msg)
        return True

    def check_directory_exist_and_create(self, folder):
        folder = (folder)
        if not os.path.isdir(folder):
            if not self.noinput:
                check_continue("The directory {} not exist".format(folder))
                mkpath(folder)
            else:
                mkpath(folder)

    def get(self):
        local_route = os.path.join(self.host_path, self.host_file)
        log.debug("Local route {}".format(local_route))
        local_tmp_route = os.path.join(self.get_host_tmp_path(), self.get_host_tmp_file())
        log.debug("TMP route {}".format(local_tmp_route))
        remote_route = self.get_remote_path() + self.get_remote_file()

        download_path = None

        tmp_unzip_folder = None

        result = False

        if local_tmp_route and self.move_to_tmp:
            if not os.path.isfile(local_tmp_route) or self.force_download:
                result = self._method.download(remote_route, local_tmp_route)
            else:
                result = True
            download_path = self.get_host_tmp_path()

        elif local_route and not self.move_to_tmp:
            if not os.path.isfile(local_route) or self.force_download:
                result = self._method.download(remote_route, local_route)
            else:
                result = True

            download_path = self.host_path

        if not result:
            show_error("Not exist:\n-{}\n-".format(local_route, local_tmp_route))

        if self.unzip:
            tmp_unzip_folder = os.path.join(self.get_host_tmp_path(), datetime.datetime.now().strftime('%s'), "")
            self.check_directory_exist_and_create(tmp_unzip_folder)
            zip_folder = os.path.join(self.get_host_tmp_path(), self.get_host_tmp_file())
            log.debug("unzip file {} to {}".format(zip_folder, tmp_unzip_folder))
            print("unzip {}".format(zip_folder, self.get_host_tmp_file()))

            process = subprocess.Popen(
                "unzip {} -d {}".format(os.path.join(self.get_host_tmp_path(), self.get_host_tmp_file()), tmp_unzip_folder),
                shell=True
            )
            process.wait()
            download_path = os.path.join(tmp_unzip_folder)

        """
        At this point. we have our final folder in th
        """

        if self.unzip or self.move_to_tmp:
            log.debug("copy file {} to {}".format(download_path, self.host_path))
            process = subprocess.Popen("cp -R {}/* {}".format(download_path, self.host_path), shell=True)
            process.wait()
            if self.unzip:
                log.debug("remove file {}".format(download_path))
                shutil.rmtree(download_path, ignore_errors=False, onerror=None)

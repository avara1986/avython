# -*- encoding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import logging
import os
import subprocess

logging.basicConfig(filename='log.log', level=logging.DEBUG)
log = logging.getLogger('avython')


class AbstractDriver(object):
    __metaclass__ = ABCMeta

    command_to_get = None

    @abstractmethod
    def download(self, remote_dir, local_dir):
        pass


class BaseDriver(AbstractDriver):

    def download(self, remote_dir, local_dir):
        log.info("Start download {}...".format(remote_dir))
        process = subprocess.Popen(
            self.command_to_get.format(remote_dir, local_dir),
            shell=True,
            stdout=subprocess.PIPE
        )
        process.wait()
        log.info("Finish download {} to ".format(remote_dir, local_dir))
        return os.path.isfile(local_dir) or os.path.isdir(local_dir)

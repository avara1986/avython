#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import subprocess
import argparse
import logging
import sys

logging.basicConfig(filename='log.log', level=logging.DEBUG)
log = logging.getLogger('avython')


class GitAutotag(object):
    __revision_list = ["mayor", "minor", "patch"]  # other conf: ["pro", "pre", "dev"]
    __list_tags = False

    def __init__(self, *args, **kwargs):
        arguments = kwargs.get("arguments", False)
        if not arguments:
            arguments = sys.argv[1:]

        parser = argparse.ArgumentParser(description='Autotag a git project ')
        parser.add_argument("-v", "--version", help="Version pattern to search")
        parser.add_argument("-d", "--directory", help="Set the directory to search changes")
        parser.add_argument("-r", "--revision", choices=self.__revision_list,
                            help="Revision of release. Choices: {}".format(str(self.__revision_list)))
        parser.add_argument("-f", "--force", action='store_true', help="Create new release, no matters if not exist new changes")

        parser.add_argument("-p", "--push", action='store_true', help="Push the new tag to git")

        self.args = parser.parse_args(arguments)
        self.parse_commandline()
        print(self.increase_or_create())

    def parse_commandline(self):

        self.version = self.args.version if self.args.version else "v"

        self.version_pattern = self.version + "*"

        self.directory = self.args.directory if self.args.directory else "./"

        self.revision = self.args.revision if self.args.revision else self.__revision_list[2]

        self.force = self.args.force

        self.__push = self.args.push

    def run(self, *args):
        log.debug("Run: git {}".format(str(args)))
        process = subprocess.Popen(('git', ) + args, stdout=subprocess.PIPE)
        result, err = process.communicate()
        if not err:
            return result
        return False

    def parse_result(self, result):
        if result and len(result) > 1:
            return result.decode('utf-8').split('\n')[:-1]
        return []

    def run_parse(self, *args):
        return self.parse_result(self.run(*args))

    def list_tags(self, cached=True):
        if not self.__list_tags or cached is False:
            self.__list_tags = self.run_parse('for-each-ref', 'refs/tags/' + self.version_pattern,  '--sort=taggerdate', "--format=%(tag)")
            #self.__list_tags = self.run_parse('tag', '-l', self.version_pattern, '--sort=creatordate')
        return self.__list_tags

    def last_tag(self):
        return self.list_tags()[-1] if self.list_tags() else False

    def exist_changes(self):
        if self.last_tag():
            return self.run_parse('log', '--oneline', '{}..HEAD'.format(self.last_tag()), '--', self.directory)
        log.debug("GitAutotag.exist_changes: Not exist tags")

    def parse_version_to_list(self):
        if self.last_tag():
            return self.last_tag().replace(self.version, "").split(".")
        return []

    def create_first_version(self):
        return ["0" for _ in range(len(self.__revision_list))]

    def parse_version_to_str(self, version_list):
        return self.version + ".".join(version_list)

    def increase_version_number(self):
        if self.exist_changes() or self.force is True:
            version = self.parse_version_to_list()
            index_of_revision = self.__revision_list.index(self.revision)
            try:
                element_to_increase = int(version[index_of_revision])
            except IndexError:
                pass
            else:
                element_to_increase += 1
                version[index_of_revision] = str(element_to_increase)
                if index_of_revision < len(version) - 1:
                    for indx, val in enumerate(version):
                        if index_of_revision < indx:
                            version[indx] = "0"
                return self.parse_version_to_str(version)
        return False

    def increase_or_create(self):
        version = self.increase_version_number()
        if not version and len(self.list_tags()) == 0:
            version = self.parse_version_to_str(self.create_first_version())
        if version and version not in self.list_tags():
            if self.__push:
                self.push(version)
            return version
        return False

    def push(self, version):
        self.run('tag', '-a', '{}'.format(version), '-m', 'Version {}'.format(version))
        self.run('push', '--tags')


if __name__ == '__main__':
    git = GitAutotag(sys.argv[1:])

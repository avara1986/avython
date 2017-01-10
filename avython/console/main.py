# -*- coding: utf-8 -*-
from __future__ import print_function
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def warning_color(message):
    return bcolors.WARNING + message + bcolors.ENDC


def error_color(message):
    return bcolors.FAIL + message + bcolors.ENDC


def exit_with_error():
    sys.exit(1)


def show_error(message):
    print(error_color(message))
    exit_with_error()


def show_warning(message):
    print(warning_color(message))


def check_continue(message):
    continue_download = raw(show_warning(message + "\nDo you really want to continue ([y]/n)?"))
    print(continue_download)
    if continue_download.lower() != "y":
        exit_with_error()

def raw(*args, **kwargs):
    if sys.version_info[0] < 3:
        input_text = str(raw_input("> "))
    else:
        input_text = input("> ")
    return input_text

from __future__ import absolute_import, print_function

import sys

import colorama
from colorama import Fore, Style

from vedo.logger import Level, DEFAULT_LEVEL, Destination

colorama.init()

LEVEL_COLORS = {
    Level.debug: Fore.MAGENTA,
    Level.info: Fore.BLUE,
    Level.warning: Fore.YELLOW,
    Level.error: Fore.RED,
    Level.fatal: Fore.RED
}

STRING_COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA,
                 Fore.CYAN, Fore.WHITE]

DEFAULT_STDERROR_LEVEL = Level.warning


def should_color(stderr=False):
    if stderr:
        return sys.stderr.isatty()

    return sys.stdout.isatty()


def get_level_color(level):
    if level not in LEVEL_COLORS:
        return Fore.RESET

    return LEVEL_COLORS[level]


def get_string_color(string):
    return STRING_COLORS[hash(string) % len(STRING_COLORS)]


def snake_case_to_camel_case(snake_case):
    camel_case = []
    capitalize_next = True

    for letter in snake_case:
        if letter == '_':
            capitalize_next = True
        elif capitalize_next:
            camel_case.append(letter.upper())
            capitalize_next = False
        else:
            camel_case.append(letter.lower())

    return ''.join(camel_case)


class ConsoleDestination(Destination):
    def __init__(self, level=DEFAULT_LEVEL,
                 stderr_level=DEFAULT_STDERROR_LEVEL,
                 colorize=False):
        super(ConsoleDestination, self).__init__(level)

        self._stderr_level = stderr_level
        self._colorize = colorize

    @property
    def stderr_level(self):
        return self._stderr_level

    @property
    def colorize(self):
        return self._colorize

    def log(self, name, message):
        level = snake_case_to_camel_case(message.level.name)
        using_stderr = message.level.value >= self.stderr_level.value

        if self.colorize and should_color(using_stderr):
            level = get_level_color(message.level) + level + Style.RESET_ALL
            name = get_string_color(name) + name + Style.RESET_ALL

        if using_stderr:
            print_file = sys.stderr
        else:
            print_file = sys.stdout

        print('[{0}] [{1}] {2}'.format(level, name, str(message)),
              file=print_file)

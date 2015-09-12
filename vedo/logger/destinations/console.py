from __future__ import absolute_import

import sys

import colorama
from colorama import Fore, Style

from vedo.logger import Level, DEFAULT_LEVEL, Destination

colorama.init(strip=not sys.stdout.isatty())

LEVEL_COLORS = {
    Level.debug: Fore.MAGENTA,
    Level.info: Fore.BLUE,
    Level.warning: Fore.YELLOW,
    Level.error: Fore.RED,
    Level.fatal: Fore.RED
}


def get_level_color(level):
    if level not in LEVEL_COLORS:
        return Fore.RESET

    return LEVEL_COLORS[level]


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
    def __init__(self, level=DEFAULT_LEVEL, colorize=False):
        super(ConsoleDestination, self).__init__(level)

        self._colorize = colorize

    @property
    def colorize(self):
        return self._colorize

    def log(self, message):
        level = snake_case_to_camel_case(message.level.name)

        if self.colorize:
            level = get_level_color(message.level) + level + Style.RESET_ALL

        print('[{0}] {1}'.format(level, str(message)))

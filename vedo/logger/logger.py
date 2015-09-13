from __future__ import absolute_import

from enum import Enum
from vedo.event_emitter import EventEmitter


class Level(Enum):
    debug = 0
    info = 1
    warning = 2
    error = 3
    fatal = 4


DEFAULT_LEVEL = Level.info


class Message(object):
    def __init__(self, level, format, *args, **kwargs):
        self._level = level
        self._format = format
        self._args = list(args)
        self._kwargs = kwargs

    @property
    def level(self):
        return self._level

    @property
    def format(self):
        return self._format

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    def __str__(self):
        return self.format.format(*self.args, **self.kwargs)


class Destination(object):
    def __init__(self, level=DEFAULT_LEVEL):
        self._level = level

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    def should_log(self, name, message):
        return message.level.value >= self.level.value

    def log(self, name, message):
        raise NotImplementedError('{0}.log'.format(self.__class__.__name__))


class Logger(EventEmitter):
    def __init__(self, name, *destinations):
        super(Logger, self).__init__()

        self._name = name
        self._destinations = destinations

    @property
    def name(self):
        return self._name

    def log_message(self, message):
        for destination in self._destinations:
            if destination.should_log(self.name, message):
                destination.log(self.name, message)

        self.emit(message.level.name, {'name': self.name, 'message': message})

    def log(self, level, format, *args, **kwargs):
        return self.log_message(Message(level, format, *args, **kwargs))

    def copy(self, name):
        return Logger(name, self._destinations)

    def __getattr__(self, name):
        if name in Level.__members__.keys():
            level = Level.__members__[name]

            def log_level(message, *args, **kwargs):
                return self.log(level, message, *args, **kwargs)

            log_level.__name__ = name

            return log_level
        else:
            raise AttributeError('\'{0}\' object has no attribute \'{1}\''
                                 .format(self.__class__.__name__, name))

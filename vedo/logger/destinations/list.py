from __future__ import absolute_import

from collections import namedtuple

from vedo.logger import DEFAULT_LEVEL, Message, Destination


NamedMessage = namedtuple('NamedMessage', ['name', 'message'])


class ListDestination(Destination):
    def __init__(self, level=DEFAULT_LEVEL):
        super(ArrayDestination, self).__init__(level)

        self._messages = []

    @property
    def messages(self):
        return [message for message in self._messages]

    def log(self, name, message):
        self._messages.append(NamedMessage(name, message))

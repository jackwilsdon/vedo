from __future__ import absolute_import

from collections import namedtuple

from vedo.logger import Destination


NamedMessage = namedtuple('NamedMessage', ['name', 'message'])


class ListDestination(Destination):
    def __init__(self, *args, **kwargs):
        super(ListDestination, self).__init__(*args, **kwargs)

        self._messages = []

    @property
    def messages(self):
        return [message for message in self._messages]

    def log(self, name, message):
        self._messages.append(NamedMessage(name, message))

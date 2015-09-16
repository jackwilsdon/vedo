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

    @property
    def latest_message(self):
        if len(self.messages) == 0:
            return None

        return self.messages[-1]

    def log(self, name, message):
        self._messages.append(NamedMessage(name, message))

    def __contains__(self, value):
        return value in self.messages

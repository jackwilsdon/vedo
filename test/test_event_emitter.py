from __future__ import absolute_import

from unittest import TestCase

from vedo.event_emitter import EventEmitter


class ResultHolder(object):
    def __init__(self, value=False):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def set(self, value):
        self._value = value

class EventEmitterTest(TestCase):
    def setUp(self):
        self.event_emitter = EventEmitter()

    def test_on(self):
        event_name = 'test event'
        result = ResultHolder()

        self.event_emitter.on(event_name, lambda event: result.set(True))
        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

    def test_monitor(self):
        event_name = 'test event'
        result = ResultHolder()

        def check_monitor(event):
            self.assertTrue(event.monitor)
            result.set(True)

        self.event_emitter.monitor(event_name, check_monitor)
        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

    def test_event_name_stringification(self):
        event_name = object()
        result = ResultHolder()

        self.event_emitter.on(str(event_name), lambda event: result.set(True))
        self.event_emitter.on(event_name, lambda event: result.set(False))

        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

from __future__ import absolute_import

from unittest import TestCase

from vedo.event_emitter import EventEmitter


class ValueHolder(object):
    def __init__(self, value=False, one_time=True):
        self._value = value
        self._one_time = one_time

        self._already_set = False

    @property
    def value(self):
        return self._value

    @property
    def one_time(self):
        return self._one_time

    @property
    def already_set(self):
        return self._already_set

    @value.setter
    def value(self, value):
        if self.one_time and not self.already_set:
            self._value = value

    def set(self, value):
        self.value = value

class EventEmitterTest(TestCase):
    def setUp(self):
        self.event_emitter = EventEmitter()

    def test_on(self):
        event_name = 'test event'
        result = ValueHolder()

        self.event_emitter.on(event_name, lambda event: result.set(True))
        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

    def test_monitor(self):
        event_name = 'test event'
        result = ValueHolder()

        def _check_monitor(event):
            self.assertTrue(event.monitor)
            result.set(True)

        self.event_emitter.monitor(event_name, _check_monitor)
        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

    def test_event_name_stringification(self):
        event_name = object()
        result = ValueHolder()

        self.event_emitter.on(str(event_name), lambda event: result.set(True))
        self.event_emitter.on(event_name, lambda event: result.set(False))

        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

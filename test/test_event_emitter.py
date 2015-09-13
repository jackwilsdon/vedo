from __future__ import absolute_import

from unittest import TestCase

from vedo.event_emitter import EventEmitter


class ValueHolder(object):
    def __init__(self, value=None, lock_on_value=False, lock_value=None):
        self._value = value
        self._lock_on_value = lock_on_value
        self._lock_value = lock_value

        self._locked = False

    @property
    def value(self):
        return self._value

    @property
    def lock_on_value(self):
        return self._lock_on_value

    @property
    def lock_value(self):
        return self._lock_value

    @property
    def locked(self):
        return self._locked

    @value.setter
    def value(self, value):
        if not self.locked:
            if self.lock_on_value and value == self.lock_value:
                self._locked = True

            self._value = value

    def set(self, value):
        self.value = value


class FalseLockValueHolder(ValueHolder):
    def __init__(self, value=False):
        super(FalseLockValueHolder, self).__init__(value, True, False)


class EventEmitterTest(TestCase):
    def setUp(self):
        self.event_emitter = EventEmitter()

    def test_on(self):
        event_name = 'test event'
        result = FalseLockValueHolder()

        self.event_emitter.on(event_name, lambda event: result.set(True))
        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

    def test_on_func_args(self):
        event_name = 'test event'
        result = FalseLockValueHolder()

        def _not_enough_args():
            result.set(False)

        def _correct_args(event):
            result.set(True)

        def _too_many_args(a, b, c):
            result.set(False)

        with self.assertRaises(TypeError):
            self.event_emitter.on(event_name, _not_enough_args)

        self.event_emitter.on(event_name, _correct_args)

        with self.assertRaises(TypeError):
            self.event_emitter.on(event_name, _too_many_args)

    def test_monitor(self):
        event_name = 'test event'
        result = FalseLockValueHolder()

        def _check_monitor(event):
            self.assertTrue(event.monitor)
            result.set(True)

        self.event_emitter.monitor(event_name, _check_monitor)
        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

    def test_event_name_stringification(self):
        event_name = object()
        result = FalseLockValueHolder()

        self.event_emitter.on(str(event_name), lambda event: result.set(True))
        self.event_emitter.on(event_name, lambda event: result.set(False))

        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

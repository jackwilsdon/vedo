from __future__ import absolute_import

from unittest import TestCase
import types

from vedo.test import ValueContainer
from vedo.event_emitter import ReadOnlyEvent, EventEmitter


class FalseLockValueContainer(ValueContainer):
    def __init__(self, value=False):
        super(FalseLockValueContainer, self).__init__(value, True, False)


class EventEmitterTest(TestCase):
    def setUp(self):
        self.event_emitter = EventEmitter()

    def test_on(self):
        event_name = 'test event'
        result = FalseLockValueContainer()

        self.event_emitter.on(event_name, lambda event: result.set(True))
        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

    def test_on_func_args(self):
        event_name = 'test event'
        result = FalseLockValueContainer()

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

        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

    def test_on_bound_func(self):
        event_name = 'test event'
        result = FalseLockValueContainer()

        def _not_enough_args(self):
            self.set(False)

        def _correct_args(self, event):
            self.set(True)

        def _too_many_args(self, a, b, c):
            self.set(False)

        bound_not_enough_args = types.MethodType(_not_enough_args, result,
                                                 FalseLockValueContainer)
        bound_correct_args = types.MethodType(_correct_args, result,
                                              FalseLockValueContainer)
        bound_too_many_args = types.MethodType(_too_many_args, result,
                                               FalseLockValueContainer)

        with self.assertRaises(TypeError):
            self.event_emitter.on(event_name, bound_not_enough_args)

        self.event_emitter.on(event_name, bound_correct_args)

        with self.assertRaises(TypeError):
            self.event_emitter.on(event_name, bound_too_many_args)

        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

    def test_monitor(self):
        event_name = 'test event'
        result = FalseLockValueContainer()

        def _check_monitor(event):
            result.set(isinstance(event, ReadOnlyEvent))

        self.event_emitter.monitor(event_name, _check_monitor)
        self.event_emitter.emit(event_name)

        self.assertTrue(result.value)

    def test_event_name_objects(self):
        event_name = object()
        result = FalseLockValueContainer()

        self.event_emitter.on(event_name, lambda event: result.set(True))

        self.event_emitter.emit(str(event_name))

        self.assertTrue(result.value)

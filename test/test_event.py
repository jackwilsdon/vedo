from __future__ import absolute_import

import unittest

from vedo.event_emitter import Event

class EventTest(unittest.TestCase):
    def test_properties_get(self):
        property_key = 'testing'
        property_value = True
        event = Event('event name', {property_key: property_value})

        self.assertEqual(event.get(property_key), property_value)

    def test_properties_get_default(self):
        property_key = 'testing'
        default_value = 'default value'
        event = Event('event name')

        self.assertEqual(event.get(property_key, default_value), default_value)

    def test_properties_get_nonexistent(self):
        property_key = 'testing'
        event = Event('event name')

        with self.assertRaises(KeyError):
            event.get(property_key)

    def test_properties_set(self):
        property_key = 'testing'
        property_value = True
        new_property_value = False
        event = Event('event name', {property_key: property_value})

        event.set(property_key, new_property_value)
        self.assertEqual(event.get(property_key), new_property_value)

    def test_properties_set_nonexistent(self):
        property_key = 'testing'
        property_value = True
        event = Event('event name')

        with self.assertRaises(KeyError):
            event.set(property_key, property_value)

    def test_cancellable_cancelled(self):
        event = Event('event name', cancellable=True)

        event.cancelled = True

        self.assertTrue(event.cancelled)

    def test_cancellable_cancel(self):
        event = Event('event name', cancellable=True)

        event.cancel()

        self.assertTrue(event.cancelled)

    def test_not_cancellable_cancelled(self):
        event = Event('event name', cancellable=False)

        with self.assertRaises(RuntimeError):
            event.cancelled = True

    def test_not_cancellable_cancel(self):
        event = Event('event name', cancellable=False)

        with self.assertRaises(RuntimeError):
            event.cancel()

    def test_cancelled(self):
        event = Event('event name', cancellable=True)

        event.cancelled = True

        self.assertTrue(event.cancelled)

    def test_cancel(self):
        event = Event('event name', cancellable=True)

        event.cancel()

        self.assertTrue(event.cancelled)

    def test_read_only_set(self):
        property_key = 'testing'
        property_value = True
        new_property_value = False
        event = Event('event name', {property_key: property_value},
                      read_only=True)

        with self.assertRaises(RuntimeError):
            event.set(property_key, new_property_value)

    def test_read_only_cancelled(self):
        event = Event('event name', read_only=True)

        with self.assertRaises(RuntimeError):
            event.cancelled = True

    def test_read_only_cancel(self):
        event = Event('event name', read_only=True)

        with self.assertRaises(RuntimeError):
            event.cancel()

    def test_monitor_set(self):
        property_key = 'testing'
        property_value = True
        new_property_value = False
        event = Event('event name', {property_key: property_value},
                      monitor=True)

        with self.assertRaises(RuntimeError):
            event.set(property_key, new_property_value)

    def test_monitor_cancelled(self):
        event = Event('event name', monitor=True)

        with self.assertRaises(RuntimeError):
            event.cancelled = True

    def test_monitor_cancel(self):
        event = Event('event name', monitor=True)

        with self.assertRaises(RuntimeError):
            event.cancel()

    def test_make_read_only(self):
        event = Event('event name')

        read_only_event = event.make_read_only()

        self.assertFalse(event.read_only)
        self.assertTrue(read_only_event.read_only)

    def test_make_monitor(self):
        event = Event('event name')

        monitor_event = event.make_monitor()

        self.assertFalse(event.monitor)
        self.assertTrue(monitor_event.monitor)

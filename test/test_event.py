from __future__ import absolute_import

from unittest import TestCase

from vedo.test import ClassTestCase
from vedo.event_emitter import Event, ReadOnlyEvent


class EventTest(ClassTestCase):
    def setUp(self):
        self.args = ['default event name']
        self.test_class = Event

    def test_name(self):
        event_name = 'event name'
        event = self.create_test_class(event_name)

        self.assertEqual(event.name, event_name)

    def test_get(self):
        property_key = 'testing'
        property_value = True
        event = self.create_test_class(properties={property_key: property_value})

        self.assertEqual(event.get(property_key), property_value)

    def test_get_nonexistent(self):
        property_key = 'testing'
        event = self.create_test_class()

        with self.assertRaises(KeyError):
            event.get(property_key)

    def test_get_default(self):
        property_key = 'testing'
        default_value = 'default value'
        event = self.create_test_class()

        self.assertEqual(event.get(property_key, default_value), default_value)

    def test_set(self):
        property_key = 'testing'
        property_value = True
        new_property_value = False
        event = self.create_test_class(properties={property_key: property_value})

        event.set(property_key, new_property_value)
        self.assertEqual(event.get(property_key), new_property_value)

    def test_set_nonexistent(self):
        property_key = 'testing'
        new_property_value = True
        event = self.create_test_class()

        with self.assertRaises(KeyError):
            event.set(property_key, new_property_value)


class ReadOnlyEventTest(EventTest):
    def setUp(self):
        self.args = ['default event name']
        self.test_class = ReadOnlyEvent

    def test_set(self):
        property_key = 'testing'
        property_value = True
        new_property_value = False
        event = self.create_test_class({property_key: property_value})

        with self.assertRaises(RuntimeError):
            event.set(property_key, new_property_value)

    def test_set_nonexistent(self):
        property_key = 'testing'
        new_property_value = True
        event = self.create_test_class()

        with self.assertRaises(RuntimeError):
            event.set(property_key, new_property_value)

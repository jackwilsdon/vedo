from __future__ import absolute_import

from unittest import TestCase

from vedo.event_emitter import Event, ReadOnlyEvent


class BaseEventTest(TestCase):
    DEFAULT_EVENT_NAME = 'default event name'

    def setUp(self):
        self.event_class = Event

    @property
    def event_class(self):
        return self._event_class

    @event_class.setter
    def event_class(self, event_class):
        self._event_class = event_class

    def create_event(self, name=DEFAULT_EVENT_NAME, *args, **kwargs):
        return self.event_class(name=name, *args, **kwargs)


class EventTest(BaseEventTest):
    def test_name(self):
        event_name = 'event name'
        event = self.create_event(event_name)

        self.assertEqual(event.name, event_name)

    def test_get(self):
        property_key = 'testing'
        property_value = True
        event = self.create_event(properties={property_key: property_value})

        self.assertEqual(event.get(property_key), property_value)

    def test_get_nonexistent(self):
        property_key = 'testing'
        event = self.create_event()

        with self.assertRaises(KeyError):
            event.get(property_key)

    def test_get_default(self):
        property_key = 'testing'
        default_value = 'default value'
        event = self.create_event()

        self.assertEqual(event.get(property_key, default_value), default_value)

    def test_set(self):
        property_key = 'testing'
        property_value = True
        new_property_value = False
        event = self.create_event(properties={property_key: property_value})

        event.set(property_key, new_property_value)
        self.assertEqual(event.get(property_key), new_property_value)

    def test_set_nonexistent(self):
        property_key = 'testing'
        new_property_value = True
        event = self.create_event()

        with self.assertRaises(KeyError):
            event.set(property_key, new_property_value)


class ReadOnlyEventTest(EventTest):
    def setUp(self):
        self.event_class = ReadOnlyEvent

    def test_set(self):
        property_key = 'testing'
        property_value = True
        new_property_value = False
        event = self.create_event({property_key: property_value})

        with self.assertRaises(RuntimeError):
            event.set(property_key, new_property_value)

    def test_set_nonexistent(self):
        property_key = 'testing'
        new_property_value = True
        event = self.create_event()

        with self.assertRaises(RuntimeError):
            event.set(property_key, new_property_value)

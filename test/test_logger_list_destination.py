from __future__ import absolute_import

from nose.tools import raises

from vedo.logger import Level, Message, Destination, Logger
from vedo.logger.destinations import ListDestination


class TestListDestination(object):
    def test_sets_level_for_level_in_constructor(self):
        list_destination = ListDestination(Level.debug)
        assert list_destination.level == Level.debug

    def test_sets_level_for_level_setter(self):
        list_destination = ListDestination(Level.debug)
        assert list_destination.level == Level.debug

        list_destination.level = Level.warning
        assert list_destination.level == Level.warning

    def test_should_log_for_same_level(self):
        message = Message(Level.debug, 'message')
        list_destination = ListDestination(Level.debug)
        assert list_destination.should_log('name', message)

    def test_should_not_log_for_lower_level(self):
        message = Message(Level.debug, 'message')
        list_destination = ListDestination(Level.warning)
        assert not list_destination.should_log('name', message)

    def test_should_log_for_higher_level(self):
        message = Message(Level.warning, 'message')
        list_destination = ListDestination(Level.debug)
        assert list_destination.should_log('name', message)

    def test_message_appended_to_messages_for_log(self):
        message = Message(Level.debug, 'message')
        list_destination = ListDestination(Level.debug)

        list_destination.log('name', message)

        assert any(message == named_message.message for named_message in
                   list_destination.messages)

    def test_latest_message_is_latest_for_log(self):
        first_message = Message(Level.debug, 'first message')
        second_message = Message(Level.debug, 'second message')
        list_destination = ListDestination(Level.debug)

        list_destination.log('name', first_message)
        list_destination.log('name', second_message)

        assert list_destination.latest_message.message == second_message

    def test_adds_message_to_messages_for_log(self):
        message = Message(Level.debug, 'message')
        list_destination = ListDestination()

        list_destination.log('name', message)

        assert list_destination.latest_message.message == message

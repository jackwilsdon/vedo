from __future__ import absolute_import

from nose.tools import raises

from vedo.logger import Level, Message, Destination, Logger
from vedo.logger.destinations import ListDestination


class TestMessage(object):
    def test_sets_level_for_level_in_constructor(self):
        message = Message(Level.debug, 'message')
        assert message.level == Level.debug

    def test_sets_format_for_format_in_constructor(self):
        message = Message(Level.debug, 'message')
        assert message.format == 'message'

    def test_sets_args_for_args_in_constructor(self):
        message = Message(Level.debug, 'message', 'first', 'second', 'third')
        assert message.args == ['first', 'second', 'third']

    def test_sets_kwargs_for_kwargs_in_constructor(self):
        message = Message(Level.debug, 'message', first='first kwarg',
                          second='second kwarg', third='third kwarg')
        assert message.kwargs == {'first': 'first kwarg',
                                  'second': 'second kwarg',
                                  'third': 'third kwarg'}

    def test_formats_message_for_args_kwargs(self):
        message = Message(Level.debug, 'this is a message created to {0} '
                          '{object}', 'test', object='message formatting')
        assert str(message) == ('this is a message created to test message '
                                'formatting')


class TestDestination(object):
    def test_sets_level_for_level_in_constructor(self):
        destination = Destination(Level.debug)
        assert destination.level == Level.debug

    def test_sets_level_for_level_setter(self):
        destination = Destination(Level.debug)
        assert destination.level == Level.debug

        destination.level = Level.warning
        assert destination.level == Level.warning

    def test_should_log_for_same_level(self):
        message = Message(Level.debug, 'message')
        destination = Destination(Level.debug)
        assert destination.should_log('name', message)

    def test_should_not_log_for_lower_level(self):
        message = Message(Level.debug, 'message')
        destination = Destination(Level.warning)
        assert not destination.should_log('name', message)

    def test_should_log_for_higher_level(self):
        message = Message(Level.warning, 'message')
        destination = Destination(Level.debug)
        assert destination.should_log('name', message)

    @raises(NotImplementedError)
    def test_raises_not_implemented_error_for_log(self):
        message = Message(Level.debug, 'message')
        destination = Destination()
        destination.log('name', message)


class TestLogger(object):
    def test_sets_name_for_name_in_constructor(self):
        logger = Logger('logger')
        assert logger.name == 'logger'

    def test_adds_destinations_for_destinations_in_constructor(self):
        destination = Destination()
        logger = Logger('logger', destination)
        assert destination in logger

    def test_logs_message_instance_for_log_message(self):
        message = Message(Level.debug, 'message')
        list_destination = ListDestination(Level.debug)
        logger = Logger('logger', list_destination)

        logger.log_message(message)

        assert list_destination.latest_message.message == message

    def test_logs_message_instance_for_log(self):
        list_destination = ListDestination(Level.debug)
        logger = Logger('logger', list_destination)

        logger.log(Level.debug, 'message', 'arg_first', second='arg_second')
        latest_message = list_destination.latest_message

        assert len(list_destination.messages) == 1
        assert latest_message.message.level == Level.debug
        assert latest_message.message.format == 'message'
        assert latest_message.message.args == ['arg_first']
        assert latest_message.message.kwargs == {'second': 'arg_second'}

    def test_copies_logger_with_new_name_for_copy(self):
        original_logger = Logger('logger')
        new_logger = original_logger.copy('new logger')

        assert original_logger.name == 'logger'
        assert new_logger.name == 'new logger'

    def test_returns_dynamic_logging_method_for_level_name(self):
        list_destination = ListDestination(Level.debug)
        logger = Logger('logger', list_destination)

        for level in list(Level):
            getattr(logger, level.name)('message', 'arg_first',
                                        second='arg_second')
            latest_message = list_destination.latest_message

            assert latest_message.message.level == level
            assert latest_message.message.format == 'message'
            assert latest_message.message.args == ['arg_first']
            assert latest_message.message.kwargs == {'second': 'arg_second'}

from __future__ import absolute_import

from unittest import TestCase

from vedo.logger import Level, DEFAULT_LEVEL, Message, Destination, Logger


class ArrayDestination(Destination):
    def __init__(self, level=DEFAULT_LEVEL):
        super(ArrayDestination, self).__init__(level)

        self._messages = []

    @property
    def messages(self):
        return [message for message in self._messages]

    def log(self, name, message):
        self._messages.append({'name': name, 'message': message})


class MessageTest(TestCase):
    def test_level(self):
        message_level = Level.debug
        message = Message(message_level, 'hello!')

        self.assertEqual(message.level, message_level)

    def test_format(self):
        message_format = 'hello!'
        message = Message(Level.debug, message_format)

        self.assertEqual(message.format, message_format)

    def test_args(self):
        message_args = ['a', 'b', 'c']
        message = Message(Level.debug, 'hello!', *message_args)

        self.assertEqual(message.args, message_args)

    def test_kwargs(self):
        message_kwargs = {'a': True}
        message = Message(Level.debug, 'hello!', **message_kwargs)

        self.assertEqual(message.kwargs, message_kwargs)

    def test_str(self):
        message_format = 'hello, {0}! how is {name}?'
        message_args = ['world']
        message_kwargs = {'name': 'Jack'}
        message_str = message_format.format(*message_args, **message_kwargs)
        message = Message(Level.debug, message_format, *message_args,
                          **message_kwargs)

        self.assertEqual(str(message), message_str)


class LoggerTest(TestCase):
    def setUp(self):
        self.array_destination = ArrayDestination(Level.debug)
        self.logger = Logger(self.__class__.__name__, self.array_destination)

    @property
    def messages(self):
        return self.array_destination.messages

    @property
    def latest_message(self):
        return self.messages[-1] if len(self.messages) > 0 else None

    def test_log_message(self):
        message = Message(Level.debug, 'hello!')
        self.logger.log_message(message)

        self.assertEqual(len(self.messages), 1)
        self.assertEqual(self.latest_message['name'], self.logger.name)
        self.assertEqual(self.latest_message['message'], message)

    def test_log(self):
        message_level = Level.debug
        message_format = 'hello!'
        self.logger.log(message_level, message_format)

        self.assertEqual(len(self.messages), 1)
        self.assertEqual(self.latest_message['name'], self.logger.name)
        self.assertEqual(self.latest_message['message'].level, message_level)
        self.assertEqual(self.latest_message['message'].format, message_format)

    def test_copy(self):
        logger_name = '{0} 2'.format(self.logger.name)
        logger_copy = self.logger.copy(logger_name)

        self.assertEqual(self.logger.name, self.__class__.__name__)
        self.assertEqual(logger_copy.name, logger_name)

    def test_generated_methods(self):
        message_level = Level.debug
        message_format = 'hello!'
        getattr(self.logger, message_level.name)(message_format)

        self.assertEqual(len(self.messages), 1)
        self.assertEqual(self.latest_message['name'], self.logger.name)
        self.assertEqual(self.latest_message['message'].level, message_level)
        self.assertEqual(self.latest_message['message'].format, message_format)

    def test_missing_attribute(self):
        with self.assertRaises(AttributeError):
            getattr(self.logger, 'invalid_attribute')

    def test_log_level(self):
        level = Level.info
        below_level = Level.debug
        above_level = Level.warning
        message_format = 'hello!'
        self.array_destination.level = level

        self.logger.log(level, message_format)

        self.assertEqual(len(self.messages), 1)
        self.assertEqual(self.latest_message['name'], self.logger.name)
        self.assertEqual(self.latest_message['message'].level, level)
        self.assertEqual(self.latest_message['message'].format, message_format)

        self.logger.log(below_level, message_format)

        self.assertEqual(len(self.messages), 1)

        self.logger.log(above_level, message_format)

        self.assertEqual(len(self.messages), 2)
        self.assertEqual(self.latest_message['name'], self.logger.name)
        self.assertEqual(self.latest_message['message'].level, above_level)
        self.assertEqual(self.latest_message['message'].format, message_format)


class DestinationTest(TestCase):
    def test_level(self):
        level = Level.debug
        destination = Destination(level)

        self.assertEqual(destination.level, level)

    def test_should_log(self):
        level = Level.info
        below_level = Level.debug
        above_level = Level.warning
        message_format = 'hello!'
        destination = Destination(level)

        self.assertTrue(destination.should_log(self.__class__.__name__,
                                               Message(level, message_format)))
        self.assertFalse(destination.should_log(self.__class__.__name__,
                                                Message(below_level,
                                                        message_format)))
        self.assertTrue(destination.should_log(self.__class__.__name__,
                                               Message(above_level,
                                                       message_format)))

    def test_log(self):
        level = Level.debug
        destination = Destination(level)
        message = Message(level, 'hello!')

        with self.assertRaises(NotImplementedError):
            destination.log('name', message)

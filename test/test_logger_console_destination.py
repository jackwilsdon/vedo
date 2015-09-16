from __future__ import absolute_import, print_function

from vedo.test import OutputRecorder

from vedo.logger import Level, Message
from vedo.logger.destinations import ConsoleDestination
from vedo.logger.destinations.console import LEVEL_COLORS


class TestConsoleDestination(object):
    def setup(self):
        self.recorder = OutputRecorder(True)

    def teardown(self):
        self.recorder.stop()

    def test_sets_level_for_level_in_constructor(self):
        console_destination = ConsoleDestination(Level.debug)
        assert console_destination.level == Level.debug

    def test_sets_stderr_level_for_stderr_level_in_constructor(self):
        console_destination = ConsoleDestination(Level.debug, Level.warning)
        assert console_destination.stderr_level == Level.warning

    def test_sets_colorize_for_colorize_in_constructor(self):
        console_destination = ConsoleDestination(Level.debug, Level.warning,
                                                 True)
        assert console_destination.colorize

    def test_sets_level_for_level_setter(self):
        console_destination = ConsoleDestination(Level.debug)
        assert console_destination.level == Level.debug

        console_destination.level = Level.warning
        assert console_destination.level == Level.warning

    def test_should_log_for_same_level(self):
        message = Message(Level.debug, 'message')
        console_destination = ConsoleDestination(Level.debug)
        assert console_destination.should_log('name', message)

    def test_should_not_log_for_lower_level(self):
        message = Message(Level.debug, 'message')
        console_destination = ConsoleDestination(Level.warning)
        assert not console_destination.should_log('name', message)

    def test_should_log_for_higher_level(self):
        message = Message(Level.warning, 'message')
        console_destination = ConsoleDestination(Level.debug)
        assert console_destination.should_log('name', message)

    def test_logs_to_stderr_for_same_stderr_level(self):
        message = Message(Level.warning, 'message')
        console_destination = ConsoleDestination(Level.debug, Level.warning)
        console_destination.log('name', message)

        assert len(self.recorder.stdout) == 0
        assert len(self.recorder.stderr) > 0

    def test_logs_to_stdout_for_lower_stderr_level(self):
        message = Message(Level.debug, 'message')
        console_destination = ConsoleDestination(Level.debug, Level.warning)
        console_destination.log('name', message)

        assert len(self.recorder.stdout) > 0
        assert len(self.recorder.stderr) == 0

    def test_logs_to_stderr_for_higher_stderr_level(self):
        message = Message(Level.warning, 'message')
        console_destination = ConsoleDestination(Level.debug, Level.info)
        console_destination.log('name', message)

        assert len(self.recorder.stdout) == 0
        assert len(self.recorder.stderr) > 0

    def test_logs_with_color_for_colorized_and_is_a_tty(self):
        message = Message(Level.debug, 'message')
        console_destination = ConsoleDestination(Level.debug, Level.info, True)

        self.recorder.isatty = True
        console_destination.log('name', message)

        assert LEVEL_COLORS[Level.debug] in self.recorder.stdout

    def test_logs_without_color_for_colorized_and_is_not_a_tty(self):
        message = Message(Level.debug, 'message')
        console_destination = ConsoleDestination(Level.debug, Level.info, True)
        console_destination.log('name', message)

        assert LEVEL_COLORS[Level.debug] not in self.recorder.stdout

    def test_logs_without_color_for_not_colorized_and_is_a_tty(self):
        message = Message(Level.debug, 'message')
        console_destination = ConsoleDestination(Level.debug, Level.info)

        self.recorder.isatty = True
        console_destination.log('name', message)

        assert LEVEL_COLORS[Level.debug] not in self.recorder.stdout

    def test_logs_without_color_for_not_colorized_and_is_not_tty(self):
        message = Message(Level.debug, 'message')
        console_destination = ConsoleDestination(Level.debug, Level.info)
        console_destination.log('name', message)

        assert LEVEL_COLORS[Level.debug] not in self.recorder.stdout

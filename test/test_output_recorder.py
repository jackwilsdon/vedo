from __future__ import absolute_import, print_function

import sys

from StringIO import StringIO

from vedo.util import OutputRecorder


class TestOutputRecorder(object):
    def teardown(self):
        if hasattr(self, 'recorder') and self.recorder.active:
            self.recorder.stop()

    def test_does_not_start_for_start_false_in_constructor(self):
        self.recorder = OutputRecorder()
        assert not self.recorder.active

    def test_starts_for_start_true_in_constructor(self):
        self.recorder = OutputRecorder(True)
        assert self.recorder.active

    def test_sets_isatty_for_isatty_in_constructor(self):
        self.recorder = OutputRecorder(False, True)
        assert self.recorder.isatty

    def test_sets_isatty_for_isatty_setter(self):
        self.recorder = OutputRecorder()
        self.recorder.isatty = True
        assert self.recorder.isatty

    def test_streams_use_isatty_value_from_recorder(self):
        self.recorder = OutputRecorder(True, True)

        assert sys.stdout.isatty()
        assert sys.stdout.isatty()

    def test_original_streams_does_nothing_for_inactive_recorder(self):
        self.recorder = OutputRecorder()

        original_stdout = sys.stdout
        original_stderr = sys.stderr

        with self.recorder.original_streams:
            assert sys.stdout == original_stdout
            assert sys.stderr == original_stderr

        assert sys.stdout == original_stdout
        assert sys.stderr == original_stderr

    def test_original_streams_swaps_streams_for_active_recorder(self):
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        self.recorder = OutputRecorder(True)

        replacement_stdout = sys.stdout
        replacement_stderr = sys.stderr

        with self.recorder.original_streams:
            assert sys.stdout == original_stdout
            assert sys.stderr == original_stderr

        assert sys.stdout == replacement_stdout
        assert sys.stderr == replacement_stderr

    def test_stdout_contains_stdout_value_for_print_in_active_recorder(self):
        self.recorder = OutputRecorder(True)

        print('text')

        assert self.recorder.stdout == 'text\n'

    def test_stderr_contains_stderr_value_for_print_in_active_recorder(self):
        self.recorder = OutputRecorder(True)

        print('text', file=sys.stderr)

        assert self.recorder.stderr == 'text\n'

    def test_start_does_nothing_for_active_recorder(self):
        self.recorder = OutputRecorder(True)

        replacement_stdout = sys.stdout
        replacement_stderr = sys.stderr

        self.recorder.start()

        assert sys.stdout == replacement_stdout
        assert sys.stderr == replacement_stderr

    def test_stop_does_nothing_for_inactive_recorder(self):
        self.recorder = OutputRecorder()

        original_stdout = sys.stdout
        original_stderr = sys.stderr

        self.recorder.stop()

        assert sys.stdout == original_stdout
        assert sys.stderr == original_stderr

    def test_start_swaps_stdout_and_stderr_streams_for_stringio(self):
        self.recorder = OutputRecorder()

        original_stdout = sys.stdout
        original_stderr = sys.stderr

        self.recorder.start()

        assert sys.stdout != original_stdout
        assert sys.stderr != original_stderr
        assert isinstance(sys.stdout, StringIO)
        assert isinstance(sys.stderr, StringIO)

    def test_stop_swaps_stdout_and_stderr_streams_for_original(self):
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        self.recorder = OutputRecorder(True)
        self.recorder.stop()

        assert sys.stdout == original_stdout
        assert sys.stderr == original_stderr

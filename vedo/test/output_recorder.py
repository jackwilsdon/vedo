import sys
from StringIO import StringIO


def get_isatty(value):
    def isatty():
        return value

    return isatty


class StreamSwapWrapper(object):
    def __init__(self, original_stdout, original_stderr, replacement_stdout,
                 replacement_stderr):
        self._original_stdout = original_stdout
        self._original_stderr = original_stderr

        self._replacement_stdout = replacement_stdout
        self._replacement_stderr = replacement_stderr

    def __enter__(self):
        sys.stdout = self._replacement_stdout
        sys.stderr = self._replacement_stderr

    def __exit__(self, type, value, traceback):
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr


class OutputRecorder(object):
    def __init__(self, start=False, isatty=False):
        self._original_stdout = None
        self._original_stderr = None

        self._replacement_stdout = None
        self._replacement_stderr = None

        self._isatty = isatty
        self._active = False

        if start:
            self.start()

    @property
    def original_streams(self):
        return StreamSwapWrapper(self._replacement_stdout,
                                 self._replacement_stderr,
                                 self._original_stdout, self._original_stderr)

    @property
    def stdout(self):
        if self._replacement_stdout is not None:
            return self._replacement_stdout.getvalue()

        return ''

    @property
    def stderr(self):
        if self._replacement_stderr is not None:
            return self._replacement_stderr.getvalue()

        return ''

    @property
    def isatty(self):
        return self._isatty

    @isatty.setter
    def isatty(self, value):
        if self.active:
            self._replacement_stdout.isatty = get_isatty(value)
            self._replacement_stderr.isatty = get_isatty(value)

        self._isatty = value

    @property
    def active(self):
        return self._active

    def start(self):
        if self.active:
            return

        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        self._replacement_stdout = StringIO()
        self._replacement_stderr = StringIO()

        if self.isatty:
            self._replacement_stdout.isatty = get_isatty(True)
            self._replacement_stderr.isatty = get_isatty(True)

        sys.stdout = self._replacement_stdout
        sys.stderr = self._replacement_stderr

        self._active = True

    def stop(self):
        if not self.active:
            return

        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

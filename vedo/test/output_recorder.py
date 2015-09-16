import sys
from StringIO import StringIO


def get_isatty(value):
    def isatty():
        return value

    return isatty


class OutputRecorder(object):
    def __init__(self, start=False, isatty=False):
        self._original_stdout = None
        self._original_stderr = None

        self._stdout_output = None
        self._stderr_output = None

        self._isatty = isatty

        if start:
            self.start()

    @property
    def stdout(self):
        if self._stdout_output is not None:
            return self._stdout_output.getvalue()

        return ''

    @property
    def stderr(self):
        if self._stdout_output is not None:
            return self._stdout_output.getvalue()

        return ''

    @property
    def isatty(self):
        return self._isatty

    def start(self):
        if (self._original_stdout is not None or
                self._original_stderr is not None):
            return

        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        self._stdout_output = StringIO()
        self._stderr_output = StringIO()

        if self.isatty:
            self._stdout_output.isatty = get_isatty(True)
            self._stderr_output.isatty = get_isatty(True)

        sys.stdout = self._stdout_output
        sys.stderr = self._stderr_output

    def stop(self):
        if self._original_stdout is None or self._original_stderr is None:
            return

        sys.stdout, self._original_stdout = self._original_stdout, None
        sys.stderr, self._original_stderr = self._original_stderr, None

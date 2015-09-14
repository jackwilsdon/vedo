import sys
from StringsIO import StringIO


class OutputRecorder(object):
    def __init__(self):
        self._original_stdout = None
        self._original_stderr = None

        self._stdout_output = None
        self._stderr_output = None

    @property
    def merge_stdout_stderr(self):
        return self._merge_stdout_stderr

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

    def start(self):
        if (self._original_stdout is not None or
                self._original_stderr is not None):
            return

        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        self._stdout_output = StringIO()
        self._stderr_output = StringIO()

        sys.stdout = self._stdout_output
        sys.stderr = self._stderr_output

    def stop(self):
        if self._original_stdout is None or self._original_stderr is None:
            return

        sys.stdout, self._original_stdout = self._original_stdout, None
        sys.stderr, self._original_stderr = self._original_stderr, None

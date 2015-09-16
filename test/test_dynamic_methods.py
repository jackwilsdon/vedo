from __future__ import absolute_import, print_function

import inspect

from vedo.test import create_pass_method, create_bound_pass_method


class TestDynamicMethods(object):
    def test_creates_method_for_name_and_argument_count(self):
        method = create_pass_method('pass_method', 3)
        argspec = inspect.getargspec(method)

        assert method.__name__ == 'pass_method'
        assert len(argspec.args) == 3

    def test_creates_bound_method_for_name_and_argument_count(self):
        method = create_bound_pass_method('bound_pass_method', 3)
        argspec = inspect.getargspec(method)

        assert method.__name__ == 'bound_pass_method'
        assert len(argspec.args) == 4
        assert hasattr(method, '__self__') and method.__self__ is not None

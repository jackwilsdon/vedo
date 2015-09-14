from __future__ import absolute_import

from unittest import TestCase


def merge_lists(base, cover):
    merged = [element for element in base]
    max_length = max(len(merged), len(cover))

    for index in range(max_length):
        if index >= len(merged):
            merged.append(cover[index])
        elif index < len(cover):
            merged[index] = cover[index]

    return merged


def merge_dicts(base, cover):
    merged = {}

    for key in base:
        merged[key] = base[key]

    for key in cover:
        merged[key] = cover[key]

    return merged


class ClassTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super(ClassTestCase, self).__init__(*args, **kwargs)

        self._args = []
        self._kwargs = {}
        self._test_class = None

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        self._args = args

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs):
        self._kwargs = kwargs

    @property
    def test_class(self):
        return self._test_class

    @test_class.setter
    def test_class(self, test_class):
        self._test_class = test_class

    def create_test_class(self, *args, **kwargs):
        merged_args = merge_lists(self.args, args)
        merged_kwargs = merge_dicts(self.kwargs, kwargs)

        if self.test_class is None:
            return None

        return self.test_class(*merged_args, **merged_kwargs)

from __future__ import absolute_import

from unittest import TestCase
from nose.tools import nottest

def merge_lists(base, cover, skip=object()):
    merged = [element for element in base]
    max_length = max(len(merged), len(cover))

    for index, cover_value in enumerate(cover):
        if cover_value == skip:
            continue
        if index >= len(merged):
            merged.append(cover[index])
        else:
            merged[index] = cover[index]

    return merged


def merge_dicts(base, cover, skip=object()):
    merged = {}

    for key in base:
        merged[key] = base[key]

    for key in cover:
        if cover[key] == skip:
            continue
        merged[key] = cover[key]

    return merged


class ClassTestCase(TestCase):
    DEFAULT = object()

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

    def create_instance(self, *args, **kwargs):
        merged_args = merge_lists(self.args, args, self.DEFAULT)
        merged_kwargs = merge_dicts(self.kwargs, kwargs, self.DEFAULT)

        if self.test_class is None:
            return None

        return self.test_class(*merged_args, **merged_kwargs)

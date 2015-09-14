from __future__ import absolute_import

from unittest import TestCase
from nose.tools import nottest


def merge_dicts(base, cover):
    merged = {}

    for key in base:
        merged[key] = base[key]

    for key in cover:
        merged[key] = cover[key]

    return merged


class ClassTestCase(TestCase):
    DEFAULT = object()

    def __init__(self, *args, **kwargs):
        super(ClassTestCase, self).__init__(*args, **kwargs)

        self._kwargs = {}
        self._test_class = None

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

    def create_instance(self, **kwargs):
        if self.test_class is None:
            return None

        merged_kwargs = merge_dicts(self.kwargs, kwargs)

        return self.test_class(**merged_kwargs)

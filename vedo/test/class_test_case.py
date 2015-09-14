from __future__ import absolute_import

from unittest import TestCase
from nose.tools import nottest

class ClassTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super(ClassTestCase, self).__init__(*args, **kwargs)

        self._test_class = None

    @property
    def test_class(self):
        return self._test_class

    @test_class.setter
    def test_class(self, test_class):
        self._test_class = test_class

    def create_instance(self, *args, **kwargs):
        return self.test_class(*args, **kwargs)

from __future__ import absolute_import

from vedo.util import ValueContainer


class TestValueContainer(object):
    def test_sets_value_for_value_in_constructor(self):
        container = ValueContainer('value')
        assert container.value == 'value'

    def test_sets_lock_trigger_for_lock_trigger_in_constructor(self):
        container = ValueContainer('value', 'trigger')
        assert container.lock_trigger == 'trigger'

    def test_sets_locked_for_locked_in_constructor(self):
        container = ValueContainer('value', 'trigger', True)
        assert container.locked

    def test_sets_value_for_value_setter(self):
        container = ValueContainer('value')
        container.value = 'new value'
        assert container.value == 'new value'

    def test_sets_value_for_set_method(self):
        container = ValueContainer('value')
        container.set('new value')
        assert container.value == 'new value'

    def test_locks_for_lock_trigger_passed_to_value_setter(self):
        container = ValueContainer('value', 'trigger')
        container.value = 'trigger'
        assert container.locked

    def test_locks_for_lock_trigger_passed_to_set_method(self):
        container = ValueContainer('value', 'trigger')
        container.set('trigger')
        assert container.locked

    def test_does_not_lock_for_lock_trigger_not_passed_to_value_setter(self):
        container = ValueContainer('value', 'trigger')
        container.value = 'new value'
        assert not container.locked

    def test_does_not_lock_for_lock_trigger_not_passed_to_set_method(self):
        container = ValueContainer('value', 'trigger')
        container.set('new value')
        assert not container.locked

    def test_value_does_not_change_for_locked_value_setter(self):
        container = ValueContainer('value', 'trigger', True)
        container.value = 'new value'
        assert container.value == 'value'

    def test_value_does_not_change_for_locked_set_method(self):
        container = ValueContainer('value', 'trigger', True)
        container.set('new value')
        assert container.value == 'value'

from __future__ import absolute_import

from nose.tools import raises

from vedo.test import (ValueContainer, create_pass_method,
                       create_bound_pass_method)

from vedo.event_emitter import Event, ReadOnlyEvent, EventEmitter


valid_unbound_function = create_pass_method(argc=1)
unbound_function_with_not_enough_args = create_pass_method(argc=0)
unbound_function_with_too_many_args = create_pass_method(argc=2)

valid_bound_function = create_bound_pass_method(argc=1)
bound_function_with_not_enough_args = create_bound_pass_method(argc=0)
bound_function_with_too_many_args = create_bound_pass_method(argc=2)


class FalseLockValueContainer(ValueContainer):
    def __init__(self, value=False):
        super(FalseLockValueContainer, self).__init__(value, True, False)


class TestEvent(object):
    def test_sets_name_for_name_in_constructor(self):
        event = Event('event name')
        assert event.name == 'event name'

    @raises(TypeError)
    def test_raises_type_error_for_non_string_name_in_constructor(self):
        Event(object())

    def test_sets_properties_for_properties_in_constructor(self):
        properties = {'key': 'value'}
        event = Event('event name', properties)
        assert event.properties == properties

    def test_returns_value_for_existing_value(self):
        event = Event('event name', {'key': 'value'})
        assert event.get('key') == 'value'

    def test_returns_default_value_for_nonexistent_key_with_default(self):
        event = Event('event name')
        assert event.get('nonexistent key', 'default value') == 'default value'

    @raises(KeyError)
    def test_raises_key_error_for_nonexistent_key(self):
        event = Event('event name')
        event.get('nonexistent key')

    def test_sets_value_for_existing_key(self):
        event = Event('event name', {'key': 'value'})
        event.set('key', 'new value')
        assert event.get('key') == 'new value'

    @raises(KeyError)
    def test_raises_key_error_for_setting_value_for_nonexistent_key(self):
        event = Event('event name')
        event.set('nonexistent key', 'value')

    def test_in_for_existing_key(self):
        event = Event('event name', {'key': 'value'})
        assert 'key' in event

    def test_not_in_for_nonexistent_key(self):
        event = Event('event name')
        assert 'nonexistent key' not in event


class TestReadOnlyEvent(object):
    def test_sets_name_for_name_in_constructor(self):
        event = ReadOnlyEvent('event name')
        assert event.name == 'event name'

    def test_sets_properties_for_properties_in_constructor(self):
        properties = {'key': 'value'}
        event = ReadOnlyEvent('event name', properties)
        assert event.properties == properties

    def test_returns_value_for_existing_value(self):
        event = ReadOnlyEvent('event name', {'key': 'value'})
        assert event.get('key') == 'value'

    def test_returns_default_value_for_nonexistent_key_with_default(self):
        event = ReadOnlyEvent('event name')
        assert event.get('nonexistent key', 'default value') == 'default value'

    @raises(KeyError)
    def test_raises_key_error_for_nonexistent_key(self):
        event = ReadOnlyEvent('event name')
        event.get('nonexistent key')

    @raises(RuntimeError)
    def test_raises_runtime_error_for_setting_value_for_existing_key(self):
        event = ReadOnlyEvent('event name', {'key': 'value'})
        event.set('key', 'new value')

    @raises(RuntimeError)
    def test_raises_key_error_for_setting_value_for_nonexistent_key(self):
        event = ReadOnlyEvent('event name')
        event.set('nonexistent key', 'value')

    def test_in_for_existing_key(self):
        event = ReadOnlyEvent('event name', {'key': 'value'})
        assert 'key' in event

    def test_not_in_for_nonexistent_key(self):
        event = ReadOnlyEvent('event name')
        assert 'nonexistent key' not in event


class TestEventEmitterOn(object):
    def setup(self):
        self.event_emitter = EventEmitter()

    def test_adds_valid_unbound_function_to_emitter(self):
        self.event_emitter.on('event', valid_unbound_function)
        assert valid_unbound_function in self.event_emitter

    @raises(TypeError)
    def test_raises_type_error_for_unbound_function_with_not_enough_args(self):
        self.event_emitter.on('event', unbound_function_with_not_enough_args)

    @raises(TypeError)
    def test_raises_type_error_for_unbound_function_with_too_many_args(self):
        self.event_emitter.on('event', unbound_function_with_too_many_args)

    def test_adds_valid_bound_function_to_emitter(self):
        self.event_emitter.on('event', valid_bound_function)
        assert valid_bound_function in self.event_emitter

    @raises(TypeError)
    def test_raises_type_error_for_bound_function_with_not_enough_args(self):
        self.event_emitter.on('event', bound_function_with_not_enough_args)

    @raises(TypeError)
    def test_raises_type_error_for_bound_function_with_too_many_args(self):
        self.event_emitter.on('event', bound_function_with_too_many_args)

    @raises(TypeError)
    def test_raises_type_error_for_invalid_type(self):
        self.event_emitter.on('event', 3.142)

    @raises(TypeError)
    def test_raises_type_error_for_non_string_event_name(self):
        self.event_emitter.on(object(), valid_unbound_function)


class TestEventEmitterOff(object):
    def setup(self):
        self.event_emitter = EventEmitter()

    def test_does_nothing_for_valid_unbound_function_not_in_emitter(self):
        self.event_emitter.off('event', valid_unbound_function)

    def test_removes_valid_unbound_function_in_emitter_from_emitter(self):
        self.event_emitter.on('event', valid_unbound_function)
        assert valid_unbound_function in self.event_emitter

        self.event_emitter.off('event', valid_unbound_function)
        assert valid_unbound_function not in self.event_emitter

    @raises(TypeError)
    def test_raises_type_error_for_unbound_function_with_not_enough_args(self):
        self.event_emitter.off('event', unbound_function_with_not_enough_args)

    @raises(TypeError)
    def test_raises_type_error_for_unbound_function_with_too_many_args(self):
        self.event_emitter.off('event', unbound_function_with_too_many_args)

    def test_does_nothing_for_valid_bound_function_not_in_emitter(self):
        self.event_emitter.off('event', valid_bound_function)

    def test_removes_valid_bound_function_in_emitter_from_emitter(self):
        self.event_emitter.on('event', valid_bound_function)
        assert valid_bound_function in self.event_emitter

        self.event_emitter.off('event', valid_bound_function)
        assert valid_bound_function not in self.event_emitter

    @raises(TypeError)
    def test_raises_type_error_for_bound_function_with_not_enough_args(self):
        self.event_emitter.off('event', bound_function_with_not_enough_args)

    @raises(TypeError)
    def test_raises_type_error_for_bound_function_with_too_many_args(self):
        self.event_emitter.off('event', bound_function_with_too_many_args)

    @raises(TypeError)
    def test_raises_type_error_for_invalid_type(self):
        self.event_emitter.off('event', 3.142)

    @raises(TypeError)
    def test_raises_type_error_for_non_string_event_name(self):
        self.event_emitter.off(object(), valid_unbound_function)


class TestEventEmitterEmit(object):
    def setup(self):
        self.event_emitter = EventEmitter()

    def test_single_listener_called_for_emit(self):
        container = FalseLockValueContainer()

        self.event_emitter.on('event', lambda event: container.set(True))
        self.event_emitter.emit('event')

        assert container.value

    def test_multiple_listeners_called_for_emit(self):
        containers = [FalseLockValueContainer(), FalseLockValueContainer()]

        self.event_emitter.on('event',
                              lambda event: containers[0].set(True))
        self.event_emitter.on('event',
                              lambda event: containers[1].set(True))

        self.event_emitter.emit('event')

        assert all(container.value for container in containers)

    def test_event_instance_is_emitted_for_emit(self):
        event = Event('event')
        container = ValueContainer()

        self.event_emitter.on('event', lambda event: container.set(event))
        self.event_emitter.emit(event)

        assert container.value == event

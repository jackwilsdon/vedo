import inspect

_DEFAULT = object()


def _validate_event_name(name):
    if not isinstance(name, str):
        raise TypeError('name must be str, not {0}'
                        .format(name.__class__.__name__))


def _validate_function(func):
    argspec = inspect.getargspec(func)
    argcount = len(argspec.args)
    bound = hasattr(func, '__self__') and func.__self__ is not None

    if bound:
        if argcount != 2:
            raise TypeError('func {0} must accept 2 arguments, not {1}'
                            .format(func.__name__, argcount))
    elif argcount != 1:
        raise TypeError('func {0} must accept 1 argument, not {1}'.format(
                        func.__name__, argcount))


class Event(object):
    def __init__(self, name, properties={}):
        _validate_event_name(name)

        self._name = name
        self._properties = properties

    @property
    def name(self):
        return self._name

    @property
    def properties(self):
        return self._properties

    def get(self, key, default=_DEFAULT):
        if key not in self and default == _DEFAULT:
            raise KeyError(key)

        return self.properties[key] if key in self else default

    def set(self, key, value):
        if key not in self:
            raise KeyError(key)

        self.properties[key] = value

    def __contains__(self, key):
        return key in self.properties


class ReadOnlyEvent(Event):
    def __init__(self, *args, **kwargs):
        super(ReadOnlyEvent, self).__init__(*args, **kwargs)

    def set(self, key, value):
        raise RuntimeError('event is read only')


class EventEmitter(object):
    def __init__(self):
        self._listeners = {}

    def emit(self, event):
        if not isinstance(event, Event):
            event = Event(event)

        if event.name in self._listeners:
            for listener in self._listeners[event.name]:
                listener(event)

        return event

    def on(self, name, func):
        _validate_event_name(name)
        _validate_function(func)

        if name not in self._listeners:
            self._listeners[name] = []

        self._listeners[name].append(func)

    def off(self, name, func):
        _validate_event_name(name)
        _validate_function(func)

        if name in self._listeners and func in self._listeners[name]:
            if len(self._listeners[name]) <= 1:
                del self._listeners[name]
            else:
                self._listeners[name].remove(func)

    def __contains__(self, value):
        for name in self._listeners:
            if value in self._listeners[name]:
                return True

        return False

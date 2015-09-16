import inspect

_DEFAULT = object()


def _validate_event_name(name):
    if not isinstance(name, str):
        raise TypeError('name must be str, not {0}'
                        .format(name.__class__.__name__))


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

        return self._properties[key] if key in self else default

    def set(self, key, value):
        if key not in self:
            raise KeyError(key)

        self._properties[key] = value

    def __contains__(self, key):
        return key in self._properties


class ReadOnlyEvent(Event):
    def __init__(self, *args, **kwargs):
        super(ReadOnlyEvent, self).__init__(*args, **kwargs)

    def set(self, key, value):
        raise RuntimeError('event is read only')


class EventEmitter(object):
    def __init__(self):
        self._listeners = {}

    def _check_func(self, func):
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

    @property
    def listeners(self):
        return self._listeners

    @property
    def events(self):
        return self.listeners.keys()

    def emit(self, event):
        if not isinstance(event, Event):
            event = Event(event)

        if event.name in self.listeners:
            for listener in self.listeners[event.name]:
                listener(event)

        return event

    def on(self, name, func):
        _validate_event_name(name)
        self._check_func(func)

        if name not in self.listeners:
            self.listeners[name] = []

        self.listeners[name].append(func)

    def off(self, name, func):
        _validate_event_name(name)
        self._check_func(func)

        if name in self.listeners and func in self.listeners[name]:
            if len(self.listeners[name]) <= 1:
                del self.listeners[name]
            else:
                self.listeners[name].remove(func)

    def __contains__(self, value):
        for name in self.listeners:
            if value in self.listeners[name]:
                return True

        return False

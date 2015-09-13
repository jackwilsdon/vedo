import inspect

_DEFAULT = object()


class Event(object):
    def __init__(self, name, properties={}, *args, **kwargs):
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

    def set(self, *args, **kwargs):
        raise RuntimeError('event is read only')


class EventEmitter(object):
    def __init__(self):
        self._monitors = {}
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

    def _emit(self, listeners, event):
        name = str(event.name)

        if name in listeners:
            for listener in listeners[name]:
                listener(event)

    def _listen(self, listeners, name, func):
        self._check_func(func)

        name = str(name)

        if name not in listeners:
            listeners[name] = []

        listeners[name].append(func)

    def emit_event(self, event):
        self._emit(self._monitors, ReadOnlyEvent(event.name, event.properties))
        self._emit(self._listeners, event)

        return event

    def emit(self, *args, **kwargs):
        return self.emit_event(Event(*args, **kwargs))

    def monitor(self, name, *funcs):
        for func in funcs:
            self._listen(self._monitors, name, func)

    def on(self, name, *funcs):
        for func in funcs:
            self._listen(self._listeners, name, func)

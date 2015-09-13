import inspect

_DEFAULT = object()


class Event(object):
    def __init__(self, name, properties={}, cancellable=False, read_only=False,
                 monitor=False):
        self._name = name
        self._properties = properties
        self._cancellable = cancellable
        self._read_only = read_only
        self._monitor = monitor

        self._cancelled = False

    @property
    def name(self):
        return self._name

    def get(self, key, default=_DEFAULT):
        if key not in self and default == _DEFAULT:
            raise KeyError(key)

        return self._properties[key] if key in self else default

    @property
    def cancellable(self):
        return self._cancellable

    @property
    def cancelled(self):
        return self._cancelled

    @property
    def read_only(self):
        return self._read_only

    @property
    def monitor(self):
        return self._monitor

    def _enforce_read_only(self):
        if self._read_only:
            raise RuntimeError('event is read only')

        if self._monitor:
            raise RuntimeError('event is monitor only')

    def set(self, key, value):
        self._enforce_read_only()

        if key not in self:
            raise KeyError(key)

        self._properties[key] = value

    @cancelled.setter
    def cancelled(self, cancelled):
        self._enforce_read_only()

        if not self.cancellable:
            raise RuntimeError('event is not cancellable')

        self._cancelled = cancelled

    def cancel(self):
        self.cancelled = True

    def make_read_only(self):
        return Event(self._name, self._properties, self._cancellable, True,
                     self._monitor)

    def make_monitor(self):
        return Event(self._name, self._properties, self._cancellable,
                     self._read_only, True)

    def __contains__(self, key):
        return key in self._properties


class EventEmitter(object):
    def __init__(self):
        self._monitors = {}
        self._listeners = {}

    def _emit(self, listeners, event):
        name = str(event.name)

        if name in listeners:
            for listener in listeners[name]:
                listener(event)

    def emit_event(self, event):
        self._emit(self._monitors, event.make_monitor())
        self._emit(self._listeners, event)

        return event

    def emit(self, name, properties={}, cancellable=False, read_only=False,
             monitor=False):
        return self.emit_event(Event(str(name), properties, cancellable,
                                     read_only, monitor))

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

    def _listen(self, listeners, name, func):
        self._check_func(func)

        name = str(name)

        if name not in listeners:
            listeners[name] = []

        listeners[name].append(func)

    def monitor(self, name, *funcs):
        for func in funcs:
            self._listen(self._monitors, name, func)

    def on(self, name, *funcs):
        for func in funcs:
            self._listen(self._listeners, name, func)

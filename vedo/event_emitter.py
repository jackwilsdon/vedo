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

        if isinstance(cancelled, bool):
            self._cancelled = cancelled

    def cancel(self):
        self.cancelled = True

    def make_read_only(self):
        return Event(self._name, self._properties, True, self._monitor)

    def make_monitor(self):
        return Event(self._name, self._properties, self._read_only, True)

    def __contains__(self, key):
        return key in self._properties


class EventEmitter(object):
    def __init__(self):
        self._monitors = {}
        self._listeners = {}

    def emit_event(self, event):
        if event.name in self._monitors:
            for monitor in self._monitors[event.name]:
                monitor(event.make_monitor())

        if event.name in self._listeners:
            for listener in self._listeners[event.name]:
                listener(event)

        return event

    def emit(self, name, properties={}, read_only=False):
        return self.emit_event(Event(name, properties, read_only))

    def _check_func(self, func):
        argspec = inspect.getargspec(func)

        if len(argspec.args) != 1:
            raise TypeError('func {0} must accept 1 argument'.format(
                            func.__name__))

    def monitor(self, name, *funcs):
        for func in funcs:
            self._check_func(func)

            if name not in self._monitors:
                self._monitors[name] = []

            self._monitors[name].append(func)

    def on(self, name, *funcs):
        for func in funcs:
            self._check_func(func)

            if name not in self._listeners:
                self._listeners[name] = []

            self._listeners[name].append(func)

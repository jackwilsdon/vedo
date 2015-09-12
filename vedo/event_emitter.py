import inspect

_DEFAULT = object()


class Event(object):
    def __init__(self, name, properties={}):
        self._name = name
        self._properties = properties

        self._cancelled = False

    @property
    def name(self):
        return self._name

    def get(self, key, default=_DEFAULT):
        if key not in self and default == _DEFAULT:
            raise KeyError(key)

        return self._properties[key] if key in self else default

    def set(self, key, value):
        if key not in self:
            raise KeyError(key)

        self._properties[key] = value

    @property
    def cancelled(self):
        return self._cancelled

    @cancelled.setter
    def cancelled(self, cancelled):
        if isinstance(cancelled, bool):
            self._cancelled = cancelled

    def cancel(self):
        self.cancelled = True

    def __contains__(self, key):
        return key in self._properties


class EventEmitter(object):
    def __init__(self):
        self._listeners = {}

    def emit(self, name, properties={}):
        self.emit_event(Event(name, properties))

    def emit_event(self, event):
        if event.name not in self._listeners:
            return

        for listener in self._listeners[event.name]:
            if not event.cancelled:
                listener(event)

    def on(self, name, *funcs):
        for func in funcs:
            argspec = inspect.getargspec(func)

            if len(argspec.args) != 1:
                raise TypeError('func {0} must accept 1 argument'.format(
                                func.__name__))

            if name not in self._listeners:
                self._listeners[name] = []

            self._listeners[name].append(func)

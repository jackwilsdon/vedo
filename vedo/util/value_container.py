class ValueContainer(object):
    DEFAULT = object()

    """A lockable container for a single value of any type.

    The value of a locked container cannot be changed.
    """

    def __init__(self, value=None, lock_trigger=DEFAULT, locked=False):
        """Configures the container with a value and lock options.

        Args:
            value: The initial value for the container.
            lock_trigger: The value to compare against when deciding
                whether or not to lock the container. If the value being
                compared against this is the same, then the container is
                locked.
            locked (bool): Whether or not the container is initially locked
                (it's value cannot be changed).
        """

        self._value = value
        self._lock_trigger = lock_trigger
        self._locked = locked

    @property
    def value(self):
        return self._value

    @property
    def lock_trigger(self):
        return self._lock_trigger

    @property
    def locked(self):
        return self._locked

    @value.setter
    def value(self, value):
        if not self.locked:
            if value == self.lock_trigger:
                self._locked = True

            self._value = value

    def set(self, value):
        self.value = value

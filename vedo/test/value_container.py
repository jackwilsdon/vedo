class ValueContainer(object):
    """A lockable container for a single value of any type.

    The value of a locked container cannot be changed.
    """

    def __init__(self, value=None, lock_on_value=False, lock_value=None,
                 locked=False):
        """Configures the container with a value and lock options.

        Args:
            value: The initial value for the container.
            lock_on_value (bool): Lock the container when the value is equal to
                `lock_value`. If the initial value is equal to `lock_value`,
                the container is not locked automatically upon creation and can
                only be locked if the value of the container changes to match
                the lock value.
            lock_value (bool): The value to compare against when deciding
                whether or not to lock the container. If the value being
                compared against this is the same, then the container is
                locked.
            locked (bool): Whether or not the container is initially locked
                (it's value cannot be changed).
        """

        self._value = value
        self._lock_on_value = lock_on_value
        self._lock_value = lock_value
        self._locked = locked

    @property
    def value(self):
        return self._value

    @property
    def lock_on_value(self):
        return self._lock_on_value

    @property
    def lock_value(self):
        return self._lock_value

    @property
    def locked(self):
        return self._locked

    @value.setter
    def value(self, value):
        if not self.locked:
            if self.lock_on_value and value == self.lock_value:
                self._locked = True

            self._value = value

    def set(self, value):
        self.value = value

from msgpackrpc import error


class Future(object):
    """
    This class is used as the result of asynchronous call.
    By using join(), the caller is able to wait for the completion.
    """

    def __init__(self, loop, timeout, callback=None):
        self._loop = loop
        self._error = None
        self._result = None
        self._timeout = timeout
        self._callback = callback
        self._error_handler = None
        self._result_handler = None

    def join(self):
        while (self._error is None and self._result is None):
            self._loop.start()

    def get(self):
        self.join()
        if self._result is not None:
            if self._result_handler is None:
                return self._result
            else:
                self._result_handler(self._result)

        if self._error_handler is not None:
            self._error_handler(self._error)
        raise error.RPCError(self._error)

    def set(self, error=None, result=None):
        self._error = error
        self._result = result

        if self._callback is not None:
            self._callback(self)

    @property
    def result(self):
        return self._result

    def set_result(self, result):
        assert result is not None
        self.set(result=result)

    @property
    def error(self):
        return self._error

    def set_error(self, error):
        assert error is not None
        self.set(error=error)

    def attach_callback(self, callback):
        self._callback = callback

    def attach_error_handler(self, handler):
        self._error_handler = handler

    def attach_result_handler(self, handler):
        self._result_handler = handler

    # better name?
    def step_timeout(self):
        if self._timeout < 1:
            return True
        else:
            self._timeout -= 1
            return False


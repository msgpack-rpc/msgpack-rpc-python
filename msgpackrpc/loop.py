from tornado import ioloop
import signal
from time import time

class Loop(object):
    """\
    An I/O loop class which wraps the Tornado's ioloop.
    """

    @staticmethod
    def instance():
        return Loop(ioloop.IOLoop.current())

    def __init__(self, loop=None):
        self._ioloop = loop or ioloop.IOLoop()
        self._ioloop.make_current()
        self._periodic_callback = None

    def start(self):
        """\
        Starts the Tornado's ioloop if it's not running.
        """

        handler = _LoopShutdownHandler(self._ioloop)
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGHUP, handler)
        self._ioloop.start()

    def stop(self):
        """\
        Stops the Tornado's ioloop if it's running.
        """

        try:
            self._ioloop.stop()
        except:
            return

    def attach_periodic_callback(self, callback, callback_time):
        if self._periodic_callback is not None:
            self.dettach_periodic_callback()

        self._periodic_callback = ioloop.PeriodicCallback(callback, callback_time, self._ioloop)
        self._periodic_callback.start()

    def dettach_periodic_callback(self):
        if self._periodic_callback is not None:
            self._periodic_callback.stop()
        self._periodic_callback = None


class _LoopShutdownHandler:
    def __init__(self, loop):
        self._ioloop = loop

    def __call__(self, *args, **argv):
        loop = self._ioloop
        deadline = time() + 3

        def stop():
            now = time()
            if now < deadline and (loop._callbacks or loop._timeouts):
                loop.add_timeout(now + 1, stop)
            else:
                loop.stop()
        stop()

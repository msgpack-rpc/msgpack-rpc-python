import msgpack

from msgpackrpc import inPy3k
from msgpackrpc import error
from msgpackrpc import Loop
from msgpackrpc import message
from msgpackrpc import session
from msgpackrpc.transport import tcp

class Server(session.Session):
    """\
    Server is usaful for MessagePack RPC Server.
    """

    def __init__(self, dispatcher, loop=None, builder=tcp, pack_encoding='utf-8', unpack_encoding=None):
        self._loop = loop or Loop()
        self._builder = builder
        self._encodings = (pack_encoding, unpack_encoding)
        self._listeners = []
        self._dispatcher = dispatcher

    def listen(self, address):
        listener = self._builder.ServerTransport(address, self._encodings)
        listener.listen(self)
        self._listeners.append(listener)

    def start(self):
        self._loop.start()

    def stop(self):
        self._loop.stop()

    def close(self):
        for listener in self._listeners:
            listener.close()

    def on_request(self, sendable, msgid, method, param):
        self.dispatch(method, param, _Responder(sendable, msgid))

    def on_notify(self, method, param):
        self.dispatch(method, param, _NullResponder())

    def dispatch(self, method, param, responder):
        try:
            if inPy3k and not isinstance(method, str):
                method = method.decode("utf-8")
            if not hasattr(self._dispatcher, method):
                raise error.NoMethodError("'{0}' method not found".format(method))
            responder.set_result(getattr(self._dispatcher, method)(*param))
        except Exception as e:
            responder.set_error(str(e))

        # TODO: Support advanced and async return


class _Responder:
    def __init__(self, sendable, msgid):
        self._sendable = sendable
        self._msgid = msgid
        self._sent = False

    def set_result(self, value, error=None, packer=msgpack.Packer()):
        if not self._sent:
            self._sendable.send_message([message.RESPONSE, self._msgid, error, value])
            self._sent = True

    def set_error(self, error, value=None):
        self.set_result(value, error)


class _NullResponder:
    def set_result(self, value, error=None):
        pass

    def set_error(self, error, value=None):
        pass

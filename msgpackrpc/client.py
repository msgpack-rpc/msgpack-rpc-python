from msgpackrpc import loop
from msgpackrpc import session
from msgpackrpc.transport import tcp

class Client(session.Session):
    """\
    Client is usaful for MessagePack RPC API.
    """

    def __init__(self, address, timeout=10, loop=loop.Loop(), builder=tcp):
        session.Session.__init__(self, address, timeout, loop, builder)

        if timeout:
            loop.attach_periodic_callback(self.step_timeout, 1000) # each 1s

    @classmethod
    def open(cls, *args):
        assert cls is Client, "should only be called on sub-classes"

        client = Client(*args)
        return Client.Context(client)

    class Context(object):
        """\
        For with statement
        """

        def __init__(self, client):
            self._client = client

        def __enter__(self):
            return self._client

        def __exit__(self, type, value, traceback):
            self._client.close()
            if type:
                return False
            return True
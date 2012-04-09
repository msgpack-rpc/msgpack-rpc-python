import threading
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import helper
import msgpackrpc
from msgpackrpc import error


class TestMessagePackRPC(unittest.TestCase):

    class TestArg:
        ''' this class must know completely how to deserialize '''
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

        def to_msgpack(self):
            return (self.a, self.b, self.c)

        def add(self, rhs):
            self.a += rhs.a
            self.b -= rhs.b
            self.c *= rhs.c
            return self

        def __eq__(self, rhs):
            return (self.a == rhs.a and self.b == rhs.b and self.c == rhs.c)

        @staticmethod
        def from_msgpack(arg):
            return TestMessagePackRPC.TestArg(arg[0], arg[1], arg[2])

    class TestServer(object):
        def hello(self):
            return "world"

        def sum(self, x, y):
            return x + y

        def nil(self):
            return None

        def add_arg(self, arg0, arg1):
            lhs = TestMessagePackRPC.TestArg.from_msgpack(arg0)
            rhs = TestMessagePackRPC.TestArg.from_msgpack(arg1)
            return lhs.add(rhs)

        def raise_error(self):
            raise Exception('error')


    def setUp(self):
        self._address = msgpackrpc.Address('localhost', helper.unused_port())

    def setup_env(self):
        def _start_server(server):
            server.start()
            server.close()

        self._server = msgpackrpc.Server(TestMessagePackRPC.TestServer())
        self._server.listen(self._address)
        self._thread = threading.Thread(target=_start_server, args=(self._server,))
        self._thread.start()

        self._client = msgpackrpc.Client(self._address, unpack_encoding='utf-8')
        return self._client;

    def tearDown(self):
        self._client.close();
        self._server.stop();
        self._thread.join();

    def test_call(self):
        client = self.setup_env();

        result1 = client.call('hello')
        result2 = client.call('sum', 1, 2)
        result3 = client.call('nil')

        self.assertEqual(result1, "world", "'hello' result is incorrect")
        self.assertEqual(result2, 3, "'sum' result is incorrect")
        self.assertIsNone(result3, "'nil' result is incorrect")

    def test_call_userdefined_arg(self):
        client = self.setup_env();

        arg = TestMessagePackRPC.TestArg(0, 1, 2)
        arg2 = TestMessagePackRPC.TestArg(23, 3, -23)

        result1 = TestMessagePackRPC.TestArg.from_msgpack(client.call('add_arg', arg, arg2))
        self.assertEqual(result1, arg.add(arg2))

        result2 = TestMessagePackRPC.TestArg.from_msgpack(client.call('add_arg', arg2, arg))
        self.assertEqual(result2, arg2.add(arg))

        result3 = TestMessagePackRPC.TestArg.from_msgpack(client.call('add_arg', result1, result2))
        self.assertEqual(result3, result1.add(result2))

    def test_call_async(self):
        client = self.setup_env();

        future1 = client.call_async('hello')
        future2 = client.call_async('sum', 1, 2)
        future3 = client.call_async('nil')
        future1.join()
        future2.join()
        future3.join()

        self.assertEqual(future1.result, "world", "'hello' result is incorrect in call_async")
        self.assertEqual(future2.result, 3, "'sum' result is incorrect in call_async")
        self.assertIsNone(future3.result, "'nil' result is incorrect in call_async")

    def test_notify(self):
        client = self.setup_env();

        result = True
        try:
            client.notify('hello')
            client.notify('sum', 1, 2)
            client.notify('nil')
        except:
            result = False

        self.assertTrue(result)

    def test_raise_error(self):
        client = self.setup_env();
        self.assertRaises(error.RPCError, lambda: client.call('raise_error'))

    def test_unknown_method(self):
        client = self.setup_env();
        self.assertRaises(error.RPCError, lambda: client.call('unknown', True))
        try:
            client.call('unknown', True)
            self.assertTrue(False)
        except error.RPCError as e:
            message = e.args[0]
            self.assertEqual(message, "'unknown' method not found", "Error message mismatched")

if __name__ == '__main__':
    unittest.main()

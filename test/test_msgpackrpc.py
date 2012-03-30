import threading
import unittest

import helper
import msgpackrpc
from msgpackrpc import inPy3k
from msgpackrpc import error


class TestMessagePackRPC(unittest.TestCase):
    class TestServer(object):
        def hello(self):
            return "world"

        def sum(self, x, y):
            return x + y

        def nil(self):
            return None

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

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
        result = client.call('hello')
        self.assertEqual(result, "world", "'hello' result is incorrect")

        result = client.call('sum', 1, 2)
        self.assertEqual(result, 3, "'sum' result is incorrect")

    def test_call_async(self):
        client = self.setup_env();

        feture1 = client.call_async('hello')
        feture2 = client.call_async('sum', 1, 2)
        feture1.join()
        feture2.join()

        self.assertEqual(feture1.result, "world", "'hello' result is incorrect in call_async")
        self.assertEqual(feture2.result, 3, "'sum' result is incorrect in call_async")

    def test_notify(self):
        client = self.setup_env();
        result = True
        try:
            client.notify('hello')
            client.notify('sum', 1, 2)
        except:
            result = False
        self.assertTrue(result)

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

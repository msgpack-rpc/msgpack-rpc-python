import threading
import unittest

import helper
import msgpackrpc


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

        import time
        time.sleep(1)

        self._client = msgpackrpc.Client(self._address)
        return self._client;

    def tearDown(self):
        self._client.close();
        self._server.stop();
        self._thread.join();

    def test_hello(self):
        client = self.setup_env();
        self.assertEqual(client.call('hello'), "world", "sum result is incorrect")

    def test_add(self):
        client = self.setup_env();
        self.assertEqual(client.call('sum', 1, 2), 3, "sum result is incorrect")


if __name__ == '__main__':
    unittest.main()

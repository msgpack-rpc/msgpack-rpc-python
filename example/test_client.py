#!/usr/bin/env python
# coding: utf-8

import msgpackrpc
import echoserver

ADDR = SERVER = THREAD = None


def setup():
    global ADDR, SERVER, THREAD
    (ADDR, SERVER, THREAD) = echoserver.serve()


def teardown():
    global SERVER, THREAD
    SERVER.stop()
    THREAD.join()


def test_client():
    global ADDR
    client = msgpackrpc.Client(ADDR, unpack_encoding = 'utf-8')

    f1 = client.call('echo', 'foo')
    f2 = client.call('echo', 'bar')
    f3 = client.call('echo', 'baz')

    assert f2 == 'bar'
    assert f1 == 'foo'
    assert f3 == 'baz'

    print "EchoHandler#echo via msgpackrpc"


if __name__ == '__main__':
    setup()
    test_client()
    teardown()


#!/usr/bin/env python
# coding: utf-8

"""Echo service.
This server using msgpackrpc.Server.
"""

import msgpackrpc

class EchoHandler(object):

    def echo(self, msg):
        return msg

def serve_background(server, daemon=False):
    def _start_server(server):
        server.start()
        server.close()

    import threading
    t = threading.Thread(target=_start_server, args = (server,))
    t.setDaemon(daemon)
    t.start()
    return t

def serve(daemon=False):
    """Serve echo server in background on localhost.
    This returns (server, port). port is number in integer.

    To stop, use ``server.shutdown()``
    """
    for port in xrange(9000, 10000):
        try:
            addr = msgpackrpc.Address('localhost', port)
            server = msgpackrpc.Server(EchoHandler())
            print server
            server.listen(addr)
            thread = serve_background(server, daemon)
            return (addr, server, thread)
        except Exception as err:
            print err
            pass

if __name__ == '__main__':
    port = serve(False)
    print "Serving on localhost:%d\n" % port[1]


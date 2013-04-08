'''
Created on Mar 25, 2013

@author: hvishwanath
'''

import socket,os
import msgpack
import signal
import tornado
from tornado.ioloop import IOLoop
from tornado import stack_context
from tornado.options import options, parse_command_line, define
from tornado.netutil import *
from tornado.ioloop import IOLoop
from tornado.util import bytes_type
from tornado import tcpserver
from tornado.iostream import IOStream


def simple_uds_server():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.remove("/tmp/socketname")
    except OSError:
        pass
    
    s.bind("/tmp/socketname")
    print "Listening..."
    s.listen(1)
    print "Accepting..."
    conn, addr = s.accept()
    
    data = conn.recv(4096)
    print ' Received : ', data
    print "Len of received data : ", len(data)
    print "Trimming the last delimiter (\n)"
    data = data.rstrip('\n')
    
    print "Trying to unpack using msgpack"
    x = msgpack.unpackb(data)
    print x
    
    print "Packing a custom object and sending to client"
    y = msgpack.packb(['String', True, 1, 3.1123]);
    
    
    conn.send(y)
    conn.close()
    


def handle_signal(sig, frame):
    IOLoop.instance().add_callback(IOLoop.instance().stop)

class UDSConnection(object):
    """UDS Connection handler"""
 
    def __init__(self, stream, address, server):
        """Initialize base params and call stream reader for next line"""
        self.stream = stream
        self.address = address
        self.server = server
        self.stream.set_close_callback(self._on_disconnect)
        self.wait()
        
    def _on_read(self, line):
        """Called when new line received from connection"""
        # Some game logic (or magic)
        print "From stream (%s), received data : %s" % (str(self.stream), line)
        print "Stripping delimiter from the data.."
        line = line.rstrip('\n')
        
        print "Trying to unpack using msgpack"
        x = msgpack.unpackb(line)
        for i in x:
            print ("%s : %s" % (i, type(i)))
        
        print "Packing a custom object and sending to client"
        y = msgpack.packb(['String', True, 1, 3.1123, False, 8383]);

        
        self.stream.write(y)
        self.wait()
 
    def wait(self):
        """Read from stream until the next signed end of line"""

        print "Will read until delimiter (\\n) "

#        chunk = self.stream._read_from_socket()
#        print "Read chunk : ", chunk
#        print "Trying to unpack using msgpack"
#        x = msgpack.unpackb(chunk)
#        print x


        #self.stream.read_bytes(3240, self._on_read)
        self.stream.read_until(b'\n', self._on_read)
 
    def _on_disconnect(self, *args, **kwargs):
        """Called on client disconnected"""
        print 'Client disconnected (stream %s, address %r)'% (id(self.stream), self.address)
        
 
    def __str__(self):
        """Build string representation, will be used for working with
        server identity (not only name) in future"""
        return "UDS Connection (stream %s, address %r)" % (id(self.stream), self.address)

class UDSServer(tcpserver.TCPServer):
    
    def handle_stream(self, stream, address):
        print "New incoming connection (stream %s, address %r)" % (id(stream), address)
        UDSConnection(stream, address, self)

def tornado_uds_server():
    
    us = bind_unix_socket("/tmp/socketname")
    tornado.process.fork_processes(0)
    server = UDSServer()
    server.add_socket(us)
    IOLoop.instance().start()    
    IOLoop.instance().close()
    
        
if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    #simple_uds_server()
    tornado_uds_server()
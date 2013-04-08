'''
Created on Apr 5, 2013

@author: hvishwanath | harish.shastry@gmail.com
'''

import msgpackrpc.transport
from tornado.netutil import bind_unix_socket
from tornado import tcpserver
from tornado.iostream import IOStream

# Create namespace equals
BaseSocket = msgpackrpc.transport.tcp.BaseSocket
ClientSocket = msgpackrpc.transport.tcp.ClientSocket
ClientTransport = msgpackrpc.transport.tcp.ClientTransport

ServerSocket = msgpackrpc.transport.tcp.ServerSocket
ServerTransport = msgpackrpc.transport.tcp.ServerTransport


class UDSServer(tcpserver.TCPServer):
    """Define a Unix domain socket server.
    Instead of binding to TCP/IP socket, bind to UDS socket and listen"""
    
    def __init__(self, io_loop=None, ssl_options=None):
        tcpserver.TCPServer.__init__(self, io_loop=io_loop, ssl_options=ssl_options)
    
    def listen(self, port, address=""):
        """Bind to a unix domain socket and add to self.
        Note that port in our case actually contains the uds file name"""
        
        # Create a Unix domain socket and bind
        socket = bind_unix_socket(port)
        
        # Add to self
        self.add_socket(socket)
        
class MessagePackServer(UDSServer):
    """The MessagePackServer inherits from UDSServer
    instead of tornado's TCP Server"""
    
    def __init__(self, transport, io_loop=None, encodings=None):
        self._transport = transport
        self._encodings = encodings
        UDSServer.__init__(self, io_loop=io_loop)

    def handle_stream(self, stream, address):
        ServerSocket(stream, self._transport, self._encodings)

#Monkey patch the MessagePackServer
msgpackrpc.transport.tcp.MessagePackServer = MessagePackServer
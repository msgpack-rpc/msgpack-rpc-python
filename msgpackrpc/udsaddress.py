'''
@author: hvishwanath | harish.shastry@gmail.com
'''

import socket
from tornado.platform.auto import set_close_exec
    
class UDSAddress(object):
    """This class abstracts Unix domain socket address.
    For compatibility with other code in the library, port is always equal to host"""

    def __init__(self, host, port=None):
        self._host = host
        
        # Passed value for port is ignored.
        # Port is also made equal to host. 
        # This is because some of the code in transport.tcp uses address._port to connect.
        # For a unix socket, there is no port. Hence if port = host, that code should work.
        self._port = host 

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port
    
    def unpack(self):
        # Return only the host
        return self._host
    
    def socket(self, family=socket.AF_UNSPEC):
        """Return a Unix domain socket"""

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        set_close_exec(sock.fileno())
        sock.setblocking(0)
        
        return sock
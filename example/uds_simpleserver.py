'''
Created on Apr 5, 2013

@author: hvishwanath
'''
import msgpackrpc
import msgpackrpc.udsaddress
from msgpackrpc.transport import euds
from msgpackrpc.transport import uds
class SumServer(object):
    def sum(self, x, y):
        return x + y

server = msgpackrpc.Server(SumServer(), builder=uds)
server.listen(msgpackrpc.udsaddress.UDSAddress('/tmp/exrpc'))
server.start()
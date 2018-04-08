'''
@author: hvishwanath | harish.shastry@gmail.com
'''

import msgpackrpc.udsaddress
from msgpackrpc.transport import uds
class SumServer(object):
    def sum(self, x, y):
        return x + y

# Use builder as uds. default builder is tcp which creates tcp sockets
server = msgpackrpc.Server(SumServer(), builder=uds)
# Use UDSAddress instead of msgpackrpc.Address
server.listen(msgpackrpc.udsaddress.UDSAddress('/tmp/exrpc'))
server.start()

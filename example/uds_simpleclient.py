'''
@author: hvishwanath | harish.shastry@gmail.com
'''

import msgpackrpc.udsaddress
from msgpackrpc.transport import uds

#Use UDSAddress instead of default Address object
client = msgpackrpc.Client(msgpackrpc.udsaddress.UDSAddress("/tmp/exrpc"), builder=uds)
result = client.call('sum', 1, 2)  # = > 
print "Sum of 1 and 2 : %d" % result
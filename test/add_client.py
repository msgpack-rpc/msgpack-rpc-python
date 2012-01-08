#!/usr/bin/env python
import socket
import msgpackrpc

for sockaddr in socket.getaddrinfo("localhost", 18800, socket.AF_UNSPEC, socket.SOCK_STREAM):
    addr = sockaddr[4]
    if len(addr) == 4 and addr[3] == 1: # ignore loopback address
        continue
    address = msgpackrpc.Address(*addr[0:2])
    print "address:(%s, %d), " % (address.host, address.port)
    client = msgpackrpc.Client(address)
    result = client.call('add', 1, 2)  # = > 3  
    print "result:", result

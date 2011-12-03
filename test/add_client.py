#!/usr/bin/env python
import socket
import msgpackrpc

for addr in socket.getaddrinfo("localhost", 18800, socket.AF_UNSPEC, socket.SOCK_STREAM):
    address = msgpackrpc.Address(*addr[4][0:2])
    print "address:(%s, %d), "  % (address.host, address.port), 
    client = msgpackrpc.Client(address)
    result = client.call('add', 1, 2)  # = > 3  
    print "result:", result

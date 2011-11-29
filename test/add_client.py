import msgpackrpc

address = msgpackrpc.Address("localhost", 18800)
#address = msgpackrpc.Address("::1", 18800)
#address = msgpackrpc.Address("127.0.0.1", 18800)
client = msgpackrpc.Client(address)
result = client.call('add', 1, 2)  # = > 3  
print result

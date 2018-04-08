<!--
[![Build Status](https://travis-ci.org/msgpack/msgpack-rpc-python.png)](https://travis-ci.org/msgpack/msgpack-rpc-python)
-->
# Unix Domain Socket support
Unix domain socket support is now available for msgpack-rpc. Sample examples below.

## UDS examples

### Server

```python
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
```

### Client
```python
import msgpackrpc.udsaddress
from msgpackrpc.transport import uds

#Use UDSAddress instead of default Address object
client = msgpackrpc.Client(msgpackrpc.udsaddress.UDSAddress("/tmp/exrpc"), builder=uds)
result = client.call('sum', 1, 2)  # = > 
print "Sum of 1 and 2 : %d" % result
```

Go through the below sections for general usage of Message Pack RPC Library

# MessagePack RPC for Python

MessagePack RPC implementation based on Tornado.

## Installation

```sh
% pip install msgpack-rpc-python
```

or

```sh
% python setup.py install
```

### Module dependency

* msgpack-python (>= 0.3)
* tornado (>= 3)

## Example

### Server

```python
import msgpackrpc

class SumServer(object):
    def sum(self, x, y):
        return x + y

server = msgpackrpc.Server(SumServer())
server.listen(msgpackrpc.Address("localhost", 18800))
server.start()
```

### Client

```python
import msgpackrpc

client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
result = client.call('sum', 1, 2)  # = > 3
```

## Run test

In test directory:

```sh
% PYTHONPATH=../ python test/test_msgpackrpc.py
```

Run with timeout test(Timeout test takes about 5 seconds)

```sh
% PYTHONPATH=../ python test/test_msgpackrpc.py --timeout-test
```

## Performance

OS: Mac OS X ver 10.8.3<br />
CPU: Intel Core i7 2.7 GHz<br />
Memory: 16 GB 1600 MHz DDR3

<table>
  <tr>
    <th></th><th>call(QPS)</th><th>async(QPS)</th><th>notify(QPS)</th>
  </tr>
  <tr>
    <td>2.7.3</td><td>5903</td><td>6040</td><td>24877</td>
  </tr>
  <tr>
    <td>3.3.0</td><td>5493</td><td>5812</td><td>23634</td>
  </tr>
  <tr>
    <td>PyPy 1.9.0 with GCC 4.2.1</td><td>5519</td><td>9729</td><td>46406</td>
  </tr>
</table>

Test code are available in example directory(bench_client.py and bench_server.py).

## TODO

* Add advanced return to Server.
* UDP, UNIX Domain support
* Utilities (MultiFuture, SessionPool)

## Copyright

<table>
  <tr>
    <td>Author</td><td>Masahiro Nakagawa <repeatedly@gmail.com></td>
  </tr>
  <tr>
    <td>Copyright</td><td>Copyright (c) 2011- Masahiro Nakagawa</td>
  </tr>
  <tr>
    <td>License</td><td>Apache License, Version 2.0</td>
  </tr>
</table>

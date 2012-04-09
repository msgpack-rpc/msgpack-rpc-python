# MessagePack RPC for Python

MessagePack RPC implementation based on Tornado.

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

## Installation

    python setup.py install

or

    easy_install msgpack-rpc-python

## Dependent modules

* msgpack-python (0.1.12)
* tornado (2.1.1)

## Performance

OS: Mac OS X ver 10.6.8<br />
CPU: Intel Core 2 Duo 2.13GHz<br />
Memory: 4GB 1067MHz DDR3

<table>
  <tr>
    <th></th><th>Request(call/s)</th><th>Notify(call/s)</th>
  </tr>
  <tr>
    <td>2.7.1</td><td>3076</td><td>14182</td>
  </tr>
  <tr>
    <td>3.2.2</td><td>2957</td><td>13472</td>
  </tr>
</table>

## TODO

* Add advanced and async return to Server.
* UDP, UNIX Domain support
* Utilities (MultiFuture, SessionPool)
* Support pyev for performance if needed

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

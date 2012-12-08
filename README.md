[![Build Status](https://travis-ci.org/msgpack/msgpack-rpc-python.png)](https://travis-ci.org/msgpack/msgpack-rpc-python)

# MessagePack RPC for Python

MessagePack RPC implementation based on Tornado.

## Installation

```sh
% python setup.py install
```

or

```sh
% easy_install msgpack-rpc-python
```

### Dependent modules

* msgpack-python (>= 0.1.12)
* tornado (>= 2.1.1)

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
% PYTHONPATH=../ python test_msgpackrpc.py
```

Run with timeout test(Timeout test takes about 5 seconds)

```sh
% PYTHONPATH=../ python test_msgpackrpc.py --timeout-test
```

## Performance

OS: Mac OS X ver 10.8.2<br />
CPU: Intel Core i7 2GHz<br />
Memory: 8GB 1600MHz DDR3

<table>
  <tr>
    <th></th><th>Request(QPS)</th><th>Notify(QPS)</th>
  </tr>
  <tr>
    <td>2.7.2</td><td>4782</td><td>18315</td>
  </tr>
  <tr>
    <td>3.2.3</td><td>4700</td><td>16667</td>
  </tr>
</table>

Test code are available in example directory(bench_client.py and bench_server.py).

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

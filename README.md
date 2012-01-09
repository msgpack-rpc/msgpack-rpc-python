># MessagePack RPC for Python

MessagePack RPC implementation based on Tornado.

# Example

    import msgpackrpc

    address = msgpackrpc.Address("localhost", 18800)
    client = msgpackrpc.Client(address)
    result = client.call('sum', 1, 2)  # = > 3  

# Installation

    python setup.py install

# Dependent modules

* msgpack-python (0.1.12)
* tornado (2.1.1)

# TODO

* Add advanced and async return to Server.
* UDP, UNIX Domain support
* Utilities (MultiFuture, SessionPool)
* Support pyev for performance if needed

# Copyright

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

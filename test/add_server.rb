#!/usr/bin/env ruby
require 'socket'
require 'msgpack/rpc'

class AddHandler
    def add(x,y) return x+y end
end

svr = MessagePack::RPC::Server.new
add_handler = AddHandler.new

for addrinfo in Socket.getaddrinfo(nil, 18800, :AF_UNSPEC, :STREAM, 0, Socket::AI_PASSIVE)
  p addrinfo
  svr.listen(addrinfo[2], 18800, add_handler)
end

svr.run



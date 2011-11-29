#!/usr/bin/env ruby
require 'msgpack/rpc'

class AddHandler
    def add(x,y) return x+y end
end

svr = MessagePack::RPC::Server.new
svr.listen('0.0.0.0', 18800, AddHandler.new)
svr.run



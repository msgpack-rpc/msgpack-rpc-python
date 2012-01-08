class RPCError(Exception):
    pass

class TimeoutError(RPCError):
    pass

class TransportError(RPCError):
    pass

class NoMethodError(RPCError):
    pass

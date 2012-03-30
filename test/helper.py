import os
import sys

def unused_port():
    import socket

    sock = socket.socket()
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

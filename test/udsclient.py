'''
Created on Mar 25, 2013

@author: hvishwanath
'''

import socket
import datetime
import threading
import msgpack

MANUAL = False
ITER = 50
THREADS = 10
SLEEP = 2

def random_word(size = 10):
    abets = 'abcdefghijklmnopqrstuvwxyz'
    rval = []
    import random
    for i in range(0, size):
        rval.append(abets[random.randint(0, 25)])
        
    return ''.join(rval)

def udsInteract():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/tmp/socketname")
    for i in range(0, ITER):
        if MANUAL:
            d = raw_input("Text to send (type x to exit) : ")
        else:
            d = random_word() 
        print "Packing and Sending data..."
        d = msgpack.packb(d)
        s.send(d+"\n")
        data = s.recv(4096)
        print 'Received', repr(data)
        print 'Unpacking'
        data = msgpack.unpackb(data)
        print data
        import time
        time.sleep(SLEEP)
        
    print "Closing connection.."
    s.close()

tlist = []
for i in range(0, THREADS):
    t = threading.Thread(target=udsInteract)
    t.start()
    tlist.append(t)

for t in tlist:
    t.join()    

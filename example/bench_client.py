import msgpackrpc
import time;

Num = 10000

def run_call():
    client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
    before = time.time()
    for x in range(Num):
        client.call('sum', 1, 2)
    after = time.time()
    diff = after - before

    print("call: {0} qps".format(Num / diff))

def run_call_async():
    client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
    before = time.time()
    for x in range(Num):
        # TODO: replace with more heavy sample
        future = client.call_async('sum', 1, 2)
        future.get()
    after = time.time()
    diff = after - before

    print("async: {0} qps".format(Num / diff))

def run_notify():
    client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
    before = time.time()
    for x in range(Num):
        client.notify('sum', 1, 2)
    after = time.time()
    diff = after - before

    print("notify: {0} qps".format(Num / diff))

run_call()
run_call_async()
run_notify()

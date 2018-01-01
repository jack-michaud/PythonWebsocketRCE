import threading
from api.Listener import Listener

NUM = 100000002

count = 0
listen = Listener(1337)

while count < 3:
    listen.start_listen("python")
    listen.stop_listen()
    count += 1

clients = listen.get_clients()

part = NUM / count

threads = [None] * len(clients)
results = [None] * len(clients)

def action(idx, c):
    lower = part * idx
    upper = part * (idx + 1)
    cmd = "sum(range({},{}))".format(lower, upper)
    print "Thread {}: {}".format(idx, cmd)
    result = c.eval(cmd)
    results[idx] = result
    print "Thread {}: {}".format(idx, result)

import time
start = time.time()

for idx in range(len(clients)):
    threads[idx] = threading.Thread(target=action, args=(idx, clients[idx]))
    threads[idx].start()

for thread in threads:
    thread.join()

print "Sum: {}".format(sum([int(r) for r in results]))
print "Elapsed: {}".format(time.time() - start)


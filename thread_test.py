"""
Small example to show the problem of multiple threads accessing one global
variable
"""

from threading import Thread
import time
import random


a = 0

def increaser():
    global a
    olda = a
    time.sleep(random.randint(0, 5))
    a = olda + 1

def decreaser():
    global a
    olda = a
    time.sleep(random.randint(0, 5))
    a = olda - 1

threads = []

for _ in range(100):
    threads.append(Thread(target=increaser))
    threads.append(Thread(target=decreaser))

print("a at the beginning {0}".format(a))

for t in threads:
    t.start()

for t in threads:
    t.join()

print("a at the end {0}".format(a))

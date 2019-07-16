# measure elapsed time

import time

start = time.time()
a = sum([x for x in range(1000000)])
end = time.time()
print(end - start)

start2 = time.time()
b = 0
for x in range(1000000):
    b += x
end2 = time.time()
print(end2 - start2)

assert a == b
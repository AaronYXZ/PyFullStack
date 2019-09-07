import time

start = time.time()
a  = sum([i * i for i in range(1000000)])
end  = time.time()

print(end - start)

start2 = time.time()
b = sum((i * i for i in range(1000000)))
end2 = time.time()

print(end2 - start2)

assert a == b
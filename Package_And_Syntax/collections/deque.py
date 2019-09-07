from collections import deque

# https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p03_keep_last_n_items.html

def search(lines, pattern, history = 5):
    pass
    # previous_lines = deque(maxlen= history)
    # for line in lines:
    #     if pattern in line:

## queue
queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")
queue.append("Graham")
queue.popleft()
queue.popleft()
print(queue)

deque_demo = deque(maxlen= 3)
deque_demo.append(1)
deque_demo.append(2)
deque_demo.append(3)
deque_demo.append(4)
print(deque_demo)
deque_demo.appendleft(0)
print(deque_demo)


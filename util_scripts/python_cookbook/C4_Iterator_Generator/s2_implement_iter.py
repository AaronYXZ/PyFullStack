class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r}'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        pass
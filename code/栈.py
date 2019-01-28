# -*- coding: utf-8 -*-


class Empty(Exception):
    pass


class Stack():
    """
    以list为基础实现的栈
    """

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, e):
        self._data.append(e)

    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop()

    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data[-1]

import sys
data = []
for _ in range(30):
    a = len(data)
    b = sys.getsizeof(data)
    print('长度：{0:3d}; 占用字节：{1:4d}'.format(a,b))
    data.append(None)
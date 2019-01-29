# -*- coding: utf-8 -*-


class Empty(Exception):
    pass


class Queue():
    """
    基于循环列表的队列
    """

    DEFAULT_CAPACITY = 10

    def __init__(self):
        self._data = [None] * Queue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._data[self._front]

    def dequeue(self):

        if self.is_empty():
            raise Empty('Queue is empty')
        temp = self._data[self._front]
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return temp

    def enqueue(self, e):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        temp = (self._front + self._size) % len(self._data)
        self._data[temp] = e
        self._size += 1

    def _resize(self, cap):

        old = self._data
        self._data = [None] * cap
        front = self._front
        for i in range(self._size):
            self._data[i] = old[front]
            front = (1 + front) % len(old)
        self._front = 0

    # 下面的两个方法是双端队列所有的
    def add_first(self, e):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        temp = (self._front - 1) % len(self._data)
        self._data[temp] = e
        self._front = temp
        self._size += 1

    def delete_last(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        temp = self._data[(self._front + self._size - 1) % len(self._data)]
        self._size -= 1
        return temp

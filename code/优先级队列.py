# -*- coding: utf-8 -*-


class Empty(Exception):
    pass


class HeapPriorityQueue():

    """
    使用堆与列表实现的优先级队列
    """

    class Item():
        """
        队列中的项类
        """

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __it__(self, other):
            return self.key < other.key

    def is_empty(self):
        return len(self) == 0

    def parent(self, j):
        """
        返回父节点的索引
        """
        return (j - 1) // 2

    def left(self, j):
        """返回左孩子索引"""
        return 2 * j + 1

    def right(self, j):
        """返回右孩子索引"""
        return 2 * j + 2

    def has_left(self, j):
        """通过判断索引是否出了列表来判断是否存在"""
        return self.left(j) < len(self.data)

    def has_right(self, j):
        return self.right(j) < len(self.data)

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def upheap(self, j):
        """向上堆排序"""
        parent = self.parent(j)
        if j > 0 and self.data[j] < self.data[parent]:
            self.swap(j, parent)
            self.upheap(parent)

    def downheap(self, j):
        """向下堆排序"""
        if self.has_left(j):
            left = self.left(j)
            small = left
            if self.has_right(j):
                right = self.right(j)
                if self.data[right] < self.data[left]:
                    small = right
            if self.data[small] < self.data[j]:
                self.swap(small, j)
                self.downheap(small)

    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def add(self, key, value):
        """添加一个元素，并进行向上堆排序"""
        self.data.append(self.Item(key, value))
        self.upheap(len(self.data) - 1)

    def min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        item = self.data[0]
        return (item.key, item.value)

    def remove_min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        self.swap(0, len(self.data) - 1)
        item = self.data.pop()
        self.downheap(0)
        return (item.key, item.value)

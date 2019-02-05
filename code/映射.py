# -*- coding: utf-8 -*-

from collections import MutableMapping
import random


class MyMap(MutableMapping):

    class item():

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __eq__(self, other):
            return self.key == other.key

        def __ne__(self, other):
            return self.key != other.key

    def __init__(self):
        self.table = []

    def __getitem__(self, item):
        for i in self.table:
            if i.key == item:
                return i.value
        raise KeyError('Key Error: ' + repr(item))

    def __setitem__(self, key, value):
        for i in self.table:
            if i.key == key:
                i.value = value
                return
        self.table.append(self.item(key, value))

    def __delitem__(self, key):
        for n, i in enumerate(self.table):
            if i.key == key:
                self.pop(n)
                return
        raise KeyError('Key Error: ' + repr(key))

    def __len__(self):
        return len(self.table)

    def __iter__(self):
        for i in self.table:
            yield i.key


def hash_code(s):
    mask = (1 << 32) - 1
    h = 0
    for character in s:
        h = (h << 5 & mask) | (h >> 27)
        h += ord(character)
    return h


class HashMapBase(MutableMapping):
    """哈希表的基类，需要在子类中实现_inner_getitem,_inner_setitem,
    _inner_delitem与__iter__"""

    class Item():

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __eq__(self, other):
            return self.key == other.key

        def __ne__(self, other):
            return self.key != other.key

    def __init__(self, cap=11, p=109345121):
        self._table = cap * [None]
        self._n = 0           # 元素数量
        self._prime = p       # MAD中的参数
        self._scale = 1 + random.randrange(p + 1)    # MAD中的参数
        self._shift = random.randrange(p)    # MAD中的参数

    def _hash_func(self, key):
        return (hash(key) * self._scale +
                self._shift) % self._prime % len(self._table)

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        j = self._hash_func(k)
        return self._inner_getitem(j, k)

    def __setitem__(self, key, value):
        j = self._hash_func(key)
        self._inner_setitem(j, key, value)
        if self._n > len(self._table) // 2:  # 调整大小，使负载因子小于等于0.5
            self._resize(2 * len(self._table) - 1)

    def __delitem__(self, key):
        j = self._hash_func(key)
        self._inner_delitem(j, key)
        self._n -= 1

    def _resize(self, cap):
        old = list(self.items())
        self._table = cap * [None]
        self._n = 0
        for (k, v) in old:
            self[k] = v


class HashMapOne(HashMapBase):
    """使用二级容器解决冲突的方式实现的哈希表"""

    def _inner_getitem(self, j, k):
        bucket = self._table[j]  # 把二级容器叫做桶
        if bucket is None:
            raise KeyError('Key Error: ' + repr(k))
        return bucket[k]

    def _inner_setitem(self, j, k, v):
        if self._table[j] is None:
            self._table[j] = MyMap()
        oldsize = len(self._table[j])
        self._table[j][k] = v
        if len(self._table[j]) > oldsize:
            self._n += 1

    def _inner_delitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error: ' + repr(k))
        del bucket[k]

    def __iter__(self):
        for bucket in self._table:
            if bucket is not None:
                for key in bucket:
                    yield key


class HashMapTwo():
    """使用线性探测解决冲突实现的哈希表"""
    _AVAIL = object()  # 标记删除位置

    def _is_available(self, j):
        """判断该位置是否可用"""
        return self._table[j] is None or self._table[j] is HashMapTwo._AVAIL

    def _find_slot(self, j, k):
        """寻找键k所在的索引
           如果找到了，返回(True,索引)
           如果没找到，返回(False,第一个可提供的索引位置)"""

        firstAvail = None
        while True:
            if self._is_available(j):
                if firstAvail is None:  # _AVAIL标记可以是第一个可提供的位置
                    firstAvail = j
                if self._table[j] is None:  # 跳过_AVAIL标记
                    return (False, firstAvail)
            elif k == self._table[j].key:
                return (True, j)
            j = (j + 1) % len(self._table)  # 向下一个查找

    def _inner_getitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError('Key Error: ' + repr(k))
        return self._table[s].value

    def _inner_setitem(self, j, k, v):
        found, s = self._find_slot(j, k)
        if not found:  # 使用第一个可提供的位置
            self._table[s] = self.Item(k, v)
            self._n += 1
        else:
            self._table[s].value = v

    def _inner_delitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError('Key Error: ' + repr(k))
        self._table[s] = HashMapTwo._AVAIL  # 删除标记

    def __iter__(self):
        for j in range(len(self._table)):
            if not self._is_available(j):
                yield self._table[j].key

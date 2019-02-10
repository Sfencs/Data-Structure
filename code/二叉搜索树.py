# -*- coding: utf-8 -*-
from collections import MutableMapping


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

# def after(p):
#     """寻找二叉搜索树的后继节点的伪代码"""
#
#     if right(p) is not None:
#         walk = right(p)
#         while left(right(p)) is not None:  # 找最左
#             walk = left(walk)
#         return walk
#     else:
#         walk = p
#         ancestor = parent(walk)
#         while ancestor is not None and walk == right(ancestor):  # 当walk是左孩子时或walk是根节点时停止
#             walk = ancestor
#             ancestor = parent(walk)
#         return ancestor


def search(T, p, k):
    """二叉树搜索的伪代码"""
    if k == p.key():
        return p
    elif k < p.key() and T.left(p) is not None:
        return search(T, T.left(p))
    elif k > p.key() and T.right(p) is not None:
        return search(T, T.right(p))
    return p


class Tree():
    """
    树的抽象基类
    """

    # 叫做位置的内嵌类，用于封装节点
    class Position():

        def element(self):
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            raise NotImplementedError('must be implemented by subclass')

    def root(self):
        """
        return 根节点的position
        """
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p):
        """

        :param p:一个位置对象
        :return: 返回p的父节点的position对象，如果p是根节点则饭后空
        """
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """

        :param p:一个位置对象
        :return: 返回该位置的孩子节点的数量
        """
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """

        :param p: 一个位置对象
        :return: 返回位置p的孩子的迭代
        """
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """

        :return: 返回整个树的节点个数
        """
        raise NotImplementedError('must be implemented by subclass')

    def is_root(self, p):
        return self.root() == p

    def is_leaf(self, p):
        return self.num_children(p) == 0

    def is_empty(self):
        return len(self) == 0

    def depth(self, p):
        """
        计算节点在树中的深度
        """
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def height(self, p):
        """
        计算节点在树中的深度
        """
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self.height(c) for c in self.children(p))


class BinaryTree(Tree):

    class Node():

        def __init__(self, element, parent=None, left=None, right=None):
            self.element = element
            self.parent = parent
            self.left = left
            self.right = right

    class Position(Tree.Position):

        def __init__(self, container, node):
            self.container = container

            self.node = node

        def element(self):
            return self.node.element

        def __eq__(self, other):
            return isinstance(other, type(self)) and other.node is self.node

    def validate(self, p):
        """
        进行位置验证
        """
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p.container is not self:
            raise ValueError('p does not belong to this container')
        if p.node.parent is p.node:
            raise ValueError('p is no longer valid')
        return p.node

    def make_position(self, node):
        """
        封装节点
        """
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        self._root = None
        self.size = 0

    def __len__(self):
        return self.size

    def root(self):

        return self.make_position(self._root)

    def parent(self, p):
        node = self.validate(p)
        return self.make_position(node.parent)

    def left(self, p):
        node = self.validate(p)
        return self.make_position(node.left)

    def right(self, p):
        node = self.validate(p)
        return self.make_position(node.right)

    def sibling(self, p):
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def num_children(self, p):
        node = self.validate(p)
        count = 0
        if node.left is not None:
            count += 1
        if node.right is not None:
            count += 1
        return count

    def children(self, p):
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    def add_root(self, e):
        if self._root is not None:
            raise ValueError('Root exists')
        self.size += 1
        self._root = self.Node(e)
        return self.make_position(self._root)

    def add_left(self, p, e):
        node = self.validate(p)
        if node.left is not None:
            raise ValueError('Left child exists')
        self.size += 1
        node.left = self.Node(e, node)
        return self.make_position(node.left)

    def add_right(self, p, e):
        node = self.validate(p)
        if node.right is not None:
            raise ValueError('Left child exists')
        self.size += 1
        node.right = self.Node(e, node)
        return self.make_position(node.right)

    def replace(self, p, e):
        node = self.validate(p)
        old = node.element
        node.element = e
        return old

    def delete(self, p):
        """
        删除该位置的节点，如果该节点有两个孩子，则会产生异常，如果只有一个孩子，
        则使其孩子代替该节点与其双亲节点连接
        """
        node = self.validate(p)
        if self.num_children(p) == 2:
            raise ValueError('p has two children')
        child = node.left if node.left else node.right
        if child is not None:
            child.parent = node.parent
        if node is self._root:
            self._root = child
        else:
            parent = node.parent
            if node is parent.left:
                parent.left = child
            else:
                parent.right = child
        self.size -= 1
        node.parent = node
        return node.element

    def preorder(self, p):
        """
        先序遍历节点p为根节点的树
        """
        yield p
        for c in self.children(p):
            for other in self.preorder(c):
                yield other

    def postorder(self, p):
        """
        后序遍历节点p为根的树
        """
        for c in self.children(p):
            for other in self.postorder(c):
                yield other
        yield p

    def breadthfirst(self):
        """
        层序遍历
        """
        if not self.is_empty():
            queue = Queue()
            queue.enqueue(self.root())
            while not queue.is_empty():
                p = queue.dequeue()
                yield p
                for i in self.children(p):
                    queue.enqueue(i)

    def inorder(self, p):
        if self.left(p) is not None:
            for other in self.inorder(self.left(p)):
                yield other
        if self.right(p) is not None:
            for other in self.inorder(self.right(p)):
                yield other


class OrderedMap(BinaryTree, MutableMapping):
    """使用二叉搜索树实现的有序映射"""

    class _Item():

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __eq__(self, other):
            return self.key == other.key

        def __ne__(self, other):
            return self.key != other.key

        def __lt__(self, other):
            return self.key < other.key

    class Position(BinaryTree.Position):

        def key(self):
            return self.element().key

        def value(self):
            return self.element().value

    def _subtree_search(self, p, k):
        """搜索算法"""

        if k == p.key():
            return p
        elif k < p.key():
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
        else:
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        return p

    def _subtree_first_position(self, p):
        """返回p为根的树的最左节点"""
        walk = p
        while self.left(walk) is not None:
            walk = self.left(walk)
        return walk

    def _subtree_last_position(self, p):
        """返回p为根的树的最右节点"""
        walk = p
        while self.right(walk) is not None:
            walk = self.right(walk)
        return walk

    def first(self):
        return self._subtree_first_position(
            self.root()) if len(self) > 0 else None

    def last(self):
        return self._subtree_last_position(
            self.root()) if len(self) > 0 else None

    def before(self, p):
        """前驱位置"""
        if self.left(p):
            return self._subtree_last_position(self.left(p))
        else:
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.left(above):
                walk = above
                above = self.parent(walk)
            return above

    def after(self, p):
        """后继位置"""
        if self.right(p):
            return self._subtree_first_position(self.right(p))
        else:
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.right(above):
                walk = above
                above = self.parent(walk)
            return above

    def find_position(self, k):
        if self.is_empty():
            return None
        else:
            p = self._subtree_search(self.root(), k)
            return p

    def __getitem__(self, k):
        if self.is_empty():
            raise KeyError('Key Error' + repr(k))
        else:
            p = self._subtree_search(self.root(), k)
            if k != p.key():
                raise KeyError('Key Error' + repr(k))
            return p.value()

    def __setitem__(self, k, v):
        if self.is_empty():
            leaf = self.add_root(self._Item(k, v))
        else:

            p = self._subtree_search(self.root(), k)
            if p.key() == k:
                p.element().value = v
                return
            else:
                item = self._Item(k, v)
                if p.key() < k:
                    leaf = self.add_right(p, item)
                else:
                    leaf = self.add_left(p, item)

    def __iter__(self):
        p = self.first()
        while p is not None:
            yield p.key()
            p = self.after(p)

    def mapdelete(self, p):
        if self.left(p) and self.right(p):  # 两个孩子都有的时候
            replacement = self._subtree_last_position(
                self.left(p))  # 用左子树最右位置代替
            self.replace(p, replacement.element())
            p = replacement
        self.delete(p)

    def __delitem__(self, k):
        if not self.is_empty():
            p = self._subtree_search(self.root(), k)
            if k == p.key():
                self.mapdelete(p)
                return
        raise KeyError('Key Error' + repr(k))

    def find_min(self):
        """找最小值，返回键值元组"""
        if self.is_empty():
            return None
        else:
            p = self.first()
            return(p.key(), p.value())

    def find_ge(self, k):
        """找第一个大于等于k的键值元组"""
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if p.key() < k:
                p = self.after(p)
            return (p.key(), p.value()) if p is not None else None

    def find_range(self, start, stop):

        if not self.is_empty():
            if start is None:
                p = self.first()
            else:
                p = self.find_position(start)
                if p.key() < start:
                    p = self.after(p)
            while p is not None and (stop is None or p.key() < stop):
                yield (p.key(), p.value())
                p = self.after(p)

# tree = OrderedMap()
# tree[1] = 1
# tree[7] = 7
# tree[2] = 2
# for (k,v) in tree.items():
#     print(v)
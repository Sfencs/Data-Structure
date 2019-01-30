# -*- coding: utf-8 -*-


class Empty(Exception):
    pass


class LinkedList():

    """
    单向链表
    """

    class Node():
        def __init__(self, element, next):
            self.element = element
            self.next = next

    def __init__(self):
        self.head = None
        self.size = 0

    def add_head(self, e):
        new = self.Node(e, self.head)
        self.head = new
        self.size += 1

    def remove_first(self):
        if self.size == 0:
            raise Empty('linkedlist is empty')
        self.head = self.head.next
        self.size -= 1


class CircularQueue():

    """
    使用循环链表实现的队列
    """

    class Node():
        def __init__(self, element, next):
            self.element = element
            self.next = next

    def __init__(self):
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def first(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        return self.tail.next.element

    def dequeue(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        old_head = self.tail.next
        if self.size == 1:
            self.tail = None
        else:
            self.tail.next = old_head.next
        self.size -= 1
        return old_head.element

    def enqueue(self, e):
        new = self.Node(e, None)
        if self.is_empty():
            new.next = new
        else:
            new.next = self.tail.next
            self.tail.next = new
        self.tail = new
        self.size += 1

    def rotate(self):
        """
        将队列的头部变为尾部，循环移动一位
        """
        if self.size > 0:
            self.tail = self.tail.next

class DoubleLinkedList():

    """
    具有头哨兵与尾哨兵的双向链表
    """

    class Node():
        def __init__(self,element,prev,next):
            self.element = element
            self.prev = prev
            self.next = next

    def __init__(self):
        self.head = self.Node(None,None,None)
        self.tail = self.Node(None,None,None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def insert_between(self,e,predecessor,successor):
        new = self.Node(e,predecessor,successor)
        predecessor.next = new
        successor.prev = new
        self.size += 1
        return new

    def delete_node(self,node):
        predecessor = node.prev
        successor = node.next
        predecessor.next = successor
        successor.prev = predecessor
        element = node.element
        self.size -= 1
        node.prev=node.next=None
        return element
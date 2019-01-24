# -*- coding: utf-8 -*-


import os


def binary_search(data, target, low, high):
    """
    二分查找，对有序列表进行查找，如果找到则返回True，否则返回False
    """

    if low > high:
        return False
    else:
        mid = (low + high) // 2
        if target == data[mid]:
            return True
        elif target < data[mid]:
            return binary_search(data, target, low, mid - 1)
        else:
            return binary_search(data, target, mid + 1, high)


def binary_sum(S, start, stop):
    """
    二路递归计算一个序列的和，例如S[0:5],就像切片的范围一样

    """

    if start >= stop:
        return 0
    elif start == stop - 1:
        return S[start]
    else:
        mid = (start + stop) // 2
        return binary_sum(S, start, mid) + binary_sum(S, mid, stop)


def disk_usage(path):
    """
    计算一个文件系统的磁盘使用情况，

    """

    total = os.path.getsize(path)
    if os.path.isdir(path):
        for filename in os.listdir(path):
            childpath = os.path.join(path, filename)
            total += disk_usage(childpath)
    print('{0:<7}'.format(total), path)
    return total


def fibonacci(n):
    """
    斐波那契数列计算，返回的是一个元组

    """

    if n <= 1:
        return (n, 0)
    else:
        (a, b) = fibonacci(n - 1)
        return(a + b, a)

# import sys
# def limitless(n):
#     print('第' + str(n) + '次调用')
#     n += 1
#     return limitless(n)
#
# print(sys.getrecursionlimit())
# sys.setrecursionlimit(10000)
# limitless(1)


def factorial(n):
    """
    阶乘递归函数

    """
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def facttail(n, res):
    """
    阶乘尾递归

    """

    if n < 0:
        return 0
    elif n == 0:
        return 1
    elif n == 1:
        return res
    else:
        return facttail(n - 1, n *res)


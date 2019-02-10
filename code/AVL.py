# -*- coding: utf-8 -*-
from 二叉搜索树 import OrderedMap

class AvlTree(OrderedMap):

    class Node(OrderedMap.Node):
        def __init__(self, element, parent=None, left=None, right=None):
            super().__init__(element,parent,left,right)
            self.height = 0

        def left_height(self):
            return self.left.height if self.left is not None else 0

        def right_height(self):
            return self.right.height if self.right is not None else 0

    def _left_left(self,p):
        this = p.node        # 有变化的就4个节点
        left = this.left
        parent = this.parent
        left_right = this.left.right
        if parent is not None:
            if this is parent.left:
                parent.left = left
            else:
                parent.right = left
        else:
            self._root = left
        this.parent = left
        left.parent = parent
        this.left = left_right
        left.right = this
        if left_right is not None:
            left_right.parent = this

    def _right_right(self,p):
        this = p.node                 # 有变化的就4个节点
        right = this.right
        parent = this.parent
        right_left = this.right.left
        if parent is not None:
            if this is parent.left:
                parent.left = right
            else:
                parent.right = right
        else:
            self._root = right
        this.parent = right
        right.parent = parent
        this.right = right_left
        right.left = this
        if right_left is not None:
            right_left.parent = this

    def _left_right(self,p):
        self._right_right(self.left(p))
        self._left_left(p)

    def _right_left(self,p):
        self._left_left(self.right(p))
        self._right_right(p)

    def _isbalanced(self,p):
        """判断节点是否平衡"""

        return abs(p.node.left_height() - p.node.right_height()) <= 1

    def _recompute_height(self,p):
        """重新计算高度"""
        p.node.height = 1 + max(p.node.left_height(),p.node.right_height())

    def _rebalanced(self,p):
        while p is not None:
            if self._isbalanced(p):
                self._recompute_height(p)
                p = self.parent(p)
            else:

                if p.node.left_height()>p.node.right_height() and p.node.left.left_height()>p.node.left.right_height():
                    # LL的情况，只有自己和左孩子的高度可能变化
                    self._left_left(p)
                elif p.node.right_height()>p.node.left_height() and p.node.right.right_height()>p.node.right.left_height():
                    # RR的情况，只有自己和右孩子的高度可能变化
                    self._right_right(p)
                elif p.node.left_height()>p.node.right_height() and p.node.left.left_height()<p.node.left.right_height():
                    # LR的情况，只有自己和左孩子和左孩子的右孩子的高度可能变化
                    left = self.left(p)
                    self._left_right(p)
                    self._recompute_height(left)
                else:
                    # RL的情况，只有自己和右孩子和右孩子的左孩子的高度可能变化
                    right = self.right(p)
                    self._right_left(p)
                    self._recompute_height(right)
                while p is not None:
                    # 调整所有p的祖先的高度
                    self._recompute_height(p)
                    p = self.parent(p)

    def _rebalanced_insert(self,p):
        """插入时的平衡调整"""
        self._rebalanced(p)

    def _rebalanced_delete(self, p):
        """删除时的平衡调整"""
        self._rebalanced(p)

    def __setitem__(self, k, v):
        """优化setitem"""
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
        self._rebalanced_insert(leaf)

    def mapdelete(self, p):
        if self.left(p) and self.right(p):  # 两个孩子都有的时候
            replacement = self._subtree_last_position(
                self.left(p))  # 用左子树最右位置代替
            self.replace(p, replacement.element())
            p = replacement
        parent = self.parent(p)
        self.delete(p)
        self._rebalanced_delete(parent)



tree = AvlTree()
tree[1] = 1
tree[2] = 2
tree[3] = 3
tree[4] = 4
tree[5] = 5
for p in tree.breadthfirst():
    print(str(p.value())+str(p.node.height))
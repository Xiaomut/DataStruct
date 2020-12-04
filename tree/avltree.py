#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   avltree.py
@Time    :   2020/11/24 10:17:07
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

from bitree import BiTreeNode, BST


class AVLNode(BiTreeNode):
    def __init__(self, data):
        BiTreeNode.__init__(self, data)
        self.bf = 0


class AVLTree(BST):
    def __init__(self, nums=None):
        BST.__init__(self, nums)

    def rotate_left(self, p, c):
        s2 = c.lchild
        p.rchild = s2
        if s2:
            s2.parent = p

        c.lchild = p
        p.parent = c

        p.bf = 0
        c.bf = 0
        return c

    def rotate_right(self, p, c):
        s2 = c.rchild
        p.lchild = s2
        if s2:
            s2.parent = p

        c.rchild = p
        p.parent = c

        p.bf = 0
        c.bf = 0
        return c

    def rotate_right_left(self, p, c):
        g = c.lchild

        s3 = g.rchild
        c.lchild = s3
        if s3:
            s3.parent = c
        g.rchild = c
        c.parent = g

        s2 = g.lchild
        p.rchild = s2
        if s2:
            s2.parent = p

        g.lchild = p
        p.parent = g

        # 更新bf
        if g.bf > 0:
            p.bf = -1
            c.bf = 0
        else:
            p.bf = 0
            c.bf = 1
        g.bf = 0
        return g

    def rotate_left_right(self, p, c):
        g = c.rchild

        s2 = g.lchild
        c.lchild = s2
        if s2:
            s2.parent = c
        g.lchild = c
        c.parent = g

        s3 = g.rchild
        p.lchild = s3
        if s3:
            s3.parent = p

        g.rchild = p
        p.parent = g

        # 更新bf
        if g.bf < 0:
            p.bf = 1
            c.bf = 0
        else:
            p.bf = 0
            c.bf = -1
        g.bf = 0
        return g

    # 插入
    def insert_no_rec(self, val):
        p = self.root
        # 空树变成根节点
        if not p:
            self.root = BiTreeNode(val)
            return
        # 1. 插入
        while True:
            if val < p.data:
                if p.lchild:
                    p = p.lchild
                # 如果左孩子不存在
                else:
                    p.lchild = BiTreeNode(val)
                    p.lchild.parent = p
                    # node存储的是插入的节点
                    node = p.lchild
                    break
            elif val > p.data:
                if p.rchild:
                    p = p.rchild
                else:
                    p.rchild = BiTreeNode(val)
                    p.rchild.parent = p
                    node = p.rchild
                    break
            else:  # 不能插入相同元素
                return

        # 2. 更新节点
        while node.parent:
            if node.parent.lchild == node:  # 传递从左子树来的，左子树更沉
                # 更新node.parent的bf
                if node.parent.bf < 0:  # 原来node.parent.f == -1, 更新后变为 -2
                    # 做旋转
                    # 看node哪边沉
                    g = node.parent.parent
                    if node.bf > 0:
                        n = self.rotate_left_right(node.parent, node)
                    else:
                        n = self.rotate_right(node.parent, node)
                    # 记得把n和g连起来
                elif node.parent.bf > 0:  # 原来node.parent.f == 1, 更新后变为 0
                    node.parent.bf = 0
                    break
                else:  # 原来node.parent.f == 0, 更新后变为 -1
                    node.parent.bf = -1
                    node = node.parent
                    continue
            else:  # 传递是从右子树来的，右子树更沉
                # 更新node.parent的bf
                if node.parent.bf > 0:  # 原来node.parent.f == 1, 更新后变为 2
                    # 做旋转
                    # 看node哪边沉
                    g = node.parent.parent
                    if node.bf < 0:  # 右左，右左旋转
                        n = self.rotate_right_left(node.parent, node)
                    else:  # 右右，左旋
                        n = self.rotate_left(node.parent, node)
                    # 记得把n和g连起来
                elif node.parent.bf < 0:  # 原来node.parent.f == -1, 更新后变为 0
                    node.parent.bf = 0
                    break
                else:  # 原来node.parent.f == 0, 更新后变为 1
                    node.parent.bf = 1
                    node = node.parent
                    continue

            # 链接旋转后的子树
            n.parent = g
            if g:  # 如果g不为空，则n为根节点
                if node.parent == g.lchild:
                    g.lchild = n
                else:
                    g.rchild = n
                break
            else:
                self.root = n
                break

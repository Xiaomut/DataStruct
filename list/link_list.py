#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   link_list.py
@Time    :   2020/11/12 10:18:16
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''
"""
头插法
尾插法
"""

class Node:
    def __init__(self, item):
        self.item = item
        self.next = None

# 头插法
def create_linklist_head(nums):
    head = Node(nums[0])
    for element in nums[1:]:
        node = Node(element)
        node.next = head
        head = node
    return head


def create_linklist_tail(nums):
    head = Node(nums[0])
    tail = head
    for element in nums[1:]:
        node = Node(element)
        tail.next = node
        tail = node
    return head


def print_linklist(lk):
    while lk:
        print(lk.item, end=',')
        lk = lk.next


lk = create_linklist_head([1,2,3])
lk2 = create_linklist_tail([1,2,3])
print_linklist(lk)
print_linklist(lk2)
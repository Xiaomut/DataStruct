#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   rotateRight.py
@Time    :   2020/12/01 10:17:09
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

# 61. Rotate List


def rotateRight(head, k):
    length = len(head)
    if length > k:
        return head[k + 1:] + head[:k + 1]
    elif length == k:
        return head
    else:
        k = k % length
        return head[k + 1:] + head[:k + 1]


print(rotateRight(head=[1, 2, 3, 4, 5], k=2))

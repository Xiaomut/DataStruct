#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   6. LeftRotateString.py
@Time    :   2021/10/09 20:48:18
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

def LeftRotateString(s, n):
    return s[n:] + s[:n]


if __name__ == "__main__":
    pass
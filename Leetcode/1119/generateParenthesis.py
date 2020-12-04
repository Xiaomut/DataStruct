#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   generateParenthesis.py
@Time    :   2020/11/19 19:28:17
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''
# ------------------------------------------------------------
"""22. Generate Parentheses"""


def generateParenthesis(n):
    left = ['('] * n
    right = [')'] * n

    i = 0

    ss = []
    s = '('
    for i in n:
        s = ''.join(['('] * i)


if __name__ == "__main__":
    generateParenthesis(3)
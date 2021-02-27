#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   isValid.py
@Time    :   2020/11/16 17:31:00
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''
# -----------------------------------------------------------
"""20. Valid Parentheses"""


def isValid(s):
    stack = []
    for i in s:
        if i == '(':
            stack.append(i)
        elif i == ')':
            if stack == [] or stack[-1] != '(':
                return False
            else:
                stack.pop()
        elif i == '[':
            stack.append(i)
        elif i == ']':
            if stack == [] or stack[-1] != '[':
                return False
            else:
                stack.pop()
        elif i == '{':
            stack.append(i)
        elif i == '}':
            if stack == [] or stack[-1] != '{':
                return False
            else:
                stack.pop()
    if stack == []:
        return True
    else:
        return False


print(isValid("[](){{"))
"""
Runtime: 24 ms, faster than 94.17% of Python3 online submissions for Valid Parentheses.
Memory Usage: 14.2 MB, less than 47.06% of Python3 online submissions for Valid Parentheses.
"""
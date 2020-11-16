#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   romanToInt.py
@Time    :   2020/11/14 15:38:03
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


def romanToInt(s: str) -> int:
    dicts = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
    values = {'I':1, 'V':2, 'X':3, 'L':4, 'C':5, 'D':6, 'M':7}

    count = 0
    new_s = s[::-1]
    for index, strs in enumerate(new_s):
        if index == 0:
            count += dicts.get(strs)
        else:
            if values.get(strs) < values.get(new_s[index-1]):
                count = count - dicts.get(strs)
            else:
                count += dicts.get(strs)
    return count
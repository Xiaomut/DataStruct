#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   findTheDifference.py
@Time    :   2020/11/14 11:14:59
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


"""
389. Find the Difference
"""

""""""
def findTheDifference(s, t):
    words = list(t)
    for i in s:
        if i in words:
            words.remove(i)
        else:
            return i
    return words[-1]


# Memory less then 100% and faster than 83.67%
def findTheDifference(s: str, t: str) -> str:
    d = {}
    for i in range(len(s)):
        if s[i] == t[i]:
            pass
        else:
            if s[i] in d:
                d[s[i]] +=1
            else:
                d[s[i]] = 1

            if t[i] in d:
                d[t[i]] -=1
            else:
                d[t[i]] = -1

    if t[-1] in d:
        d[t[-1]] -= 1
    else:
        d[t[-1]] = -1
    
    for k,v in d.items():
        if v == -1:
            return k

print(findTheDifference(s = "", t = "a"))
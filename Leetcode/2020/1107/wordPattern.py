#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   wordPattern.py
@Time    :   2020/11/07 21:41:33
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

def wordPattern(pattern, s):
    data = {}

    words = s.split()
    if len(words) != len(pattern):
        return False
    for pat, word in zip(pattern, s.split()):
        if pat not in data.keys() and word not in data.values():
            data[pat] = word
        elif pat not in data.keys() and word in data.values():
            return False
        else:
            if data[pat] == word:
                continue
            else:
                return False
    return True


print(wordPattern("aaa", "aa aa aa aa"))
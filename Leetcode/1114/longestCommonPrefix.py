#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   longestCommonPrefix.py
@Time    :   2020/11/14 16:03:38
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

"""14. Longest Common Prefix"""

def longestCommonPrefix(strs):
    mask = strs[0]
    for s in strs[1:]:
        if len(s) < len(mask):
            mask = s
    
    for s in strs:
        if len(mask) == 1:
            if not mask in s:
                return ""
        else:
            if mask in s:
                continue
            else:
                pass
    return mask
            
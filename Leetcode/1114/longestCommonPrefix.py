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
        if len(s) == 0:
            return ""
        if len(s) < len(mask):
            mask = s

    def smooth(mask):
        for s in strs:
            if not s.startswith(mask):
                mask = mask[:-1]
                if len(mask) >= 1:
                    return smooth(mask)
                else:
                    return ""
            else:
                continue
        return mask

    return smooth(mask)


res = longestCommonPrefix(["flower",  "flow",  "flight"])
print(res)

# return mask

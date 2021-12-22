#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   15. findAnagrams.py
@Time    :   2021/12/14 10:59:35
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''


from typing import List


def findAnagrams(s: str, p: str) -> List[int]:

    l1, l2 = len(s), len(p)
    if l1 < l2:
        return []

    from collections import Counter
    c2 = Counter(p)

    res = []
    for i in range(l1-l2+1):
        tmp = s[i:i+l2]
        c1 = Counter(tmp)
        if c1 == c2:
            res.append(i)
    return res



if __name__ == "__main__":
    s = "cbaebabacd"
    p = "abc"

    res = findAnagrams(s, p)
    print(res)
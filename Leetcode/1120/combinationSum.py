#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   combinationSum.py
@Time    :   2020/11/20 16:52:37
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

#-----------------------------------------------------
"""
39. Combination Sum
"""


def combinationSum(candidates, target):
    ans = []

    def func(c, s, start, target, arr):
        if s >= target:
            if s == target:
                ans.append(arr)
            return
        for i in range(start, len(c)):
            func(c, s + c[i], i, target, arr + [c[i]])
        return

    func(candidates, 0, 0, target, [])
    return ans


print(combinationSum(candidates=[2, 3, 5], target=8))

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   letterCombinations.py
@Time    :   2020/11/16 17:04:45
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''
# --------------------------------------------------------
"""
17. Letter Combinations of a Phone Number
"""


def letterCombinations(digits):
    dicts = {
        2: 'abc',
        3: 'def',
        4: 'ghi',
        5: 'jkl',
        6: 'mno',
        7: 'pqrs',
        8: 'tuv',
        9: 'wxyz'
    }

    values = len(digits)
    if values == 0:
        return []
    elif values == 1:
        return list(dicts[int(digits)])

    nums = []
    for index, digit in enumerate(digits):
        nums.append(list(dicts[int(digit)]))
    # print(nums)
    if values == 2:
        res = []
        for i in nums[0]:
            for j in nums[1]:
                res.append(i + j)
    elif values == 3:
        res = []
        for i in nums[0]:
            for j in nums[1]:
                for k in nums[2]:
                    res.append(i + j + k)
    elif values == 4:
        res = []
        for i in nums[0]:
            for j in nums[1]:
                for k in nums[2]:
                    for l in nums[3]:
                        res.append(i + j + k + l)

    return res


res = letterCombinations('243')
print(res)

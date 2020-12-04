#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   strStr.py
@Time    :   2020/11/19 19:51:06
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


def strStr(haystack, needle):
    if needle == "":
        return 0
    elif needle not in haystack:
        return -1
    elif len(needle) == len(haystack):
        return 0
    elif len(needle) == 1:
        for _, i in enumerate(haystack):
            if i == needle:
                return _
    else:
        length = len(needle)
        for i in range(len(haystack) - length + 1):
            # tmp = haystack[i:i + length]
            # print(tmp)
            if haystack[i:i + length] == needle:
                return i
            else:
                continue


print(strStr(haystack="mississippi", needle="pi"))
"""
Runtime: 24 ms, faster than 95.11% of Python3 online submissions for Implement strStr().
Memory Usage: 14.2 MB, less than 46.07% of Python3 online submissions for Implement strStr().
"""


def removeDuplicates(nums):
    # res = set(nums)
    # print(res)
    # for i in res:
    #     print(i, end=',')
    # return len(res)
    news = []
    for num in nums:
        if num not in news:
            news.append(num)
    print(news)
    return len(news)


removeDuplicates([1, 1, 2])

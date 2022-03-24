#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   5. Longest Palindromic Substring.py
@Time    :   2021/12/08 11:37:27
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

"""
Given a string s, return the longest palindromic substring in s.
"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        res = ''
        def helper(l, r):
            while (l >= 0 and r < len(s) and s[r] == s[l]):
                l -= 1 
                r += 1
            return s[l + 1: r]

        for i in range(len(s)):
            tmp = helper(i, i)
            print(tmp)
            if len(tmp) > len(res):
                res = tmp
            tmp = helper(i, i + 1)
            print(tmp)
            if len(tmp) > len(res):
                res = tmp
        return res


if __name__ == "__main__":
    solution = Solution()
    res = solution.longestPalindrome('asdffda')
    print(res)
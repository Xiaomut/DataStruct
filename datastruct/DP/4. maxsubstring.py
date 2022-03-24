#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   4. maxsubstring.py
@Time    :   2021/10/11 10:22:19
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''


def longest_substring(s):
    dp = [1]*len(s)
    for i in range(1,len(s)):
        temp = s[i-dp[i-1]:i]
        if s[i] not in temp:
            dp[i]=dp[i-1]+1
        else:
            index = temp.index(s[i])
            dp[i] = i-(index+i-dp[i-1])
    print(max(dp))


if __name__ == "__main__":
    longest_substring('pwwkew')



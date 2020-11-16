#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   longestPalindrome.py
@Time    :   2020/11/14 11:29:05
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


# def longestPalindrome(s):
#     if len(s) == 1:
#         return s
#     datas = {}
#     pass


def longestPalindrome1(s):
    n = len(s)
    dp = [[False]*n for i in range(n)]
    output = ''
    
    for end in range(n) :
        for start in range(end+1) :
            
            if s[start] == s[end] :
                
                l = end-start+1
                dp[start][end] = l<3 or dp[start+1][end-1]
                
                if l > len(output) and dp[start][end]:
                    output = s[start:end+1]
    
    return output


def longestPalindrome2(self, s: str) -> str:
        
    def helper(l, r) :
        
        while l >= 0 and r < len(s) and s[l] == s[r] :
            l -= 1
            r += 1
                
        return (l+1, r)

        
    dist = lambda x : x[1]-x[0]
    pos = (0, 0)
    
    for i in range(len(s)) :
        
        x = helper(i, i)
        y = helper(i, i+1)
        
        pos = max(pos, x, y, key=dist)
        
    l, r = pos
    return s[l:r]


# print(longestPalindrome1(s="baabad"))
print(longestPalindrome2(s="baabad"))
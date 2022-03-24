#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   22. Generate Parentheses.py
@Time    :   2021/12/08 15:17:17
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

"""Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses."""
from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res = []
        def backtrack(string, left, right, n):
            if left == 0 and right == 0:
                res.append(string)
            elif right<left:
                return
            else:
                if left == n:
                    backtrack(string+'(', left-1, right, n)
                elif left == 0:
                    backtrack(string+')', left, right-1, n)
                else:
                    backtrack(string+'(', left-1, right, n)
                    backtrack(string+')', left, right-1, n)
        backtrack('', n, n, n)
        return res

    """
    DP问题，自底向上，从最外层开始递归，从内层开始算起，不断累计，输出最后结果
    """
    def generateParenthesis2(self, n: int) -> List[str]:
        if n == 0:
            return []
        if n == 1:
            return ['()']
        ans = set()
        for x in self.generateParenthesis2(n - 1):
            for i in range(len(x)):
                ans.add(x[:i] + '()' + x[i:])
        return ans


if __name__ == "__main__":
    solution = Solution()
    res = solution.generateParenthesis2(3)
    print(res)

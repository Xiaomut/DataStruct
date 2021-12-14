#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   3. countBits.py
@Time    :   2021/12/08 16:13:38
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

"""给定一个非负整数 n ，请计算 0 到 n 之间的每个数字的二进制表示中 1 的个数，并输出一个数组。"""
from typing import List


class Solution:
    def countBits(self, n: int) -> List[int]:
        res = []
        for i in range(n+1):
            tmp = list(str(bin(i))[2:]).count('1')
            res.append(tmp)
        return res


if __name__ == "__main__":
    solution = Solution()
    res = solution.countBits(2)
    print(res)
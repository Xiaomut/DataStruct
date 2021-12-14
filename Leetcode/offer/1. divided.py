#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   1. divided.py
@Time    :   2021/12/08 15:52:05
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''


class Solution:
    def divide(self, a: int, b: int) -> int:
        ret = 0
        # flag = False if (a > 0 and b > 0) or (a < 0 and b < 0) else True
        flag = True if (a > 0) ^ (b > 0) else False
        a, b = abs(a), abs(b)

        def calc(x, y):
            n = 1
            while x > y << 1:
                y <<= 1
                n <<= 1
            return n, y

        while a >= b:
            cnt, val = calc(a, b)
            ret += cnt
            a -= val
        ret = -ret if flag else ret
        return ret - 1 if ret >= 2 ** 31 else ret


if __name__ == "__main__":
    solution = Solution()
    res = solution.divide(7, -3)
    print(res)


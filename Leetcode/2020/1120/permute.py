#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   permute.py
@Time    :   2020/11/20 17:10:34
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

# 46. Permutations


def permute(nums):
    result = []

    def rec(x, y):
        print(f'The input is: ({str(x)}, {str(y)})')
        if len(y) == 1:
            result.append(x + y)
        else:
            for i, v in enumerate(y):
                print(f'x + [v] = {x + [v]}')
                rec(x + [v], y[:i] + y[i + 1:])
        print(f'result: {result}')

    rec([], nums)
    return result


print(permute(nums=[1, 2, 3]))

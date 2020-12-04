#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   canJump.py
@Time    :   2020/11/23 17:59:50
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


# 55. Jump Game
def canJump(nums):
    length = len(nums)
    for index, num in enumerate(nums):
        tmp_index = index + num]
        if tmp_index >= length - 1:
            return True
        else:
            index = tmp_index
            if num == 0:
                return False
            else:
                continue
    return False


print(canJump([3, 0, 8, 2, 0, 0, 1]))

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   8. myAtoi.py
@Time    :   2021/12/24 16:59:37
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''


def myAtoi(s: str) -> int:
    import re

    nums = re.findall('^[+-]?\d+', s.strip())
    if nums:
        num = nums[0]
        print(num)

    
if __name__ == "__main__":
    myAtoi(s="  words and -42") # words and 987
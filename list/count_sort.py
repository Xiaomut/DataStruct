#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   count_sort.py
@Time    :   2020/11/03 14:19:37
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

import random


def count_sort(nums, max_count=100):
    count = [0 for _ in range(max_count)]
    for val in nums:
        count[val] += 1
    nums.clear()r
    for index, val in enumerate(count):
        for i in range(val):
            nums.append(index)


nums = [random.randint(0,5) for _ in range(10)]
print(nums)
count_sort(nums)
print(nums)
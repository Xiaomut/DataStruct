#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   radix_sort.py
@Time    :   2020/11/04 23:40:28
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

import random

"""
基数排序
O(kn)   k=log(10, n)
O(k+n)

"""


def radix_sort(nums):
    max_num = max(nums)
    it = 0
    while 10 ** it <= max_num:
        buckets = [[] for _ in range(10)]
        for var in nums:
            digit = (var // 10 ** it) % 10
            buckets[digit].append(var)
        # 分桶完成
        nums.clear()
        for buc in buckets:
            nums.extend(buc)
        # 把数重新写回nums
        it += 1


nums = list(range(100))
random.shuffle(nums)
radix_sort(nums)
print(nums)
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   59. KthLargest.py
@Time    :   2021/12/10 09:52:17
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

"""
设计一个找到数据流中第 k 大元素的类（class）。注意是排序后的第 k 大元素，不是第 k 个不同的元素。

请实现 KthLargest 类：
- KthLargest(int k, int[] nums) 使用整数 k 和整数流 nums 初始化对象。
- int add(int val) 将 val 插入数据流 nums 后，返回当前数据流中第 k 大的元素。
"""
from typing import List
from heapq import heappush, heappop, heapify

class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        from heapq import heapify, heappop, heappush
        self.k = k
        # self.nums = heapify(nums)

        self.nums = []
        for i in nums:
            heappush(self.nums, i)

            if len(self.nums) > k:
                heappop(self.nums)

    def add(self, val: int) -> int:

        print(self.nums)
        heappush(self.nums, val)
        if len(self.nums) > self.k:
            heappop(self.nums)

        return self.nums[0]


if __name__ == "__main__":
    kla = KthLargest(3, [4, 5, 8, 2, 6, 9])
    print(kla.add(5))
    
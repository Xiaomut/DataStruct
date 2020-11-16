#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   merge_sort.py
@Time    :   2020/11/03 11:01:34
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


"""
归并排序    O(nlogn) O(n)
分解：将列表越分越小，直至分成一个元素
终止条件：一个元素是有序的
合并：将两个有序的列表归并，列表越来越大
"""

import random


def merge(nums, low, mid, high):
    i = low
    j = mid + 1
    tmp = []
    while i <= mid and j <= high:
        if nums[i] < nums[j]:
            tmp.append(nums[i])
            i += 1
        else:
            tmp.append(nums[j])
            j += 1
    while i <= mid:
        tmp.append(nums[i])
        i += 1
    while j <= high:
        tmp.append(nums[j])
        j += 1
    nums[low:high+1] = tmp


def merge_sort(nums, low, high):
    if low < high:
        mid = (low + high) // 2
        merge_sort(nums, low, mid)
        merge_sort(nums, mid+1, high)
        # 查看中间变化
        # print(nums[low:high+1])
        # 实现归并的递归
        merge(nums, low, mid, high)


if __name__ == "__main__":
    nums = list(range(10))
    random.shuffle(nums)
    print(nums)

    merge_sort(nums, 0, len(nums)-1)
    print(nums)

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   topK.py
@Time    :   2020/11/03 10:38:10
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


"""
现有n个数，设计算法得到前k个最大的数. ( k < n )

解决思路：
1. 排序后切片       O(nlogn)
2. 排序             O(kn)
3. 堆排序           O(nlogk)

1) 取列表前k个元素建立一个小根堆，堆顶就是目前第k个最大的数
2) 依次向后遍历原列表，对于列表中的元素，如果小于堆顶，则忽略该元素，如果大于堆顶，则将堆顶更换为该元素，并且对堆进行一次调整
3) 遍历列表所有元素后，倒序弹出堆顶
"""

import random


def sift(nums, low, high):
    """
    :param nums: 列表
    :param low: 堆的根节点位置
    :param high: 堆的最后一个元素的位置
    :return:
    """
    # i最开始指向根节点
    i = low
    # j开始是左孩子
    j = 2 * i + 1
    # 把堆顶存起来
    tmp = nums[low]
    # 只要j位置有数
    while j <= high:
        # 如果有孩子有并且比较大
        if j + 1 <= high and nums[j+1] < nums[j]:
            # j指向右孩子
             j = j+1
        if nums[j] < tmp:
            nums[i] = nums[j]
            # 往下看一层
            i = j
            j = 2*i + 1
        else:
            # tmp更大，把tmp放到i的位置上，把tmp放到某一级领导位置上
            break
    # 把tmp放到叶子节点上
    nums[i] = tmp
    # print(nums)


def topK(nums, k):
    heap = nums[0:k]
    for i in range((k-2)//2, -1, -1):
        sift(heap, i, k-1)
    # 1. 建堆
    for i in range(k, len(nums)):
        if nums[i] > heap[0]:
            heap[0] = nums[i]
            sift(heap, 0, k-1)
    # 2. 遍历
    for i in range(k-1, -1, -1):
        # 将i指向当前堆的最后一个元素
        nums[0], nums[i] = nums[i], nums[0]
        # i-1 是新的high
        sift(nums, 0, i-1)
    return heap


def heap_sort(nums):
    n = len(nums)
    # i表示建堆的时候调整的部分的根的下标
    for i in range((n-2)//2, -1, -1):
        sift(nums, i, n-1)
    for i in range(n-1, -1, -1):
        # 将i指向当前堆的最后一个元素
        nums[0], nums[i] = nums[i], nums[0]
        # i-1 是新的high
        sift(nums, 0, i-1)

if __name__ == "__main__":
    nums = list(range(10))
    random.shuffle(nums)
    print(topK(nums, 5))
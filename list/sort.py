#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sort.py
@Time    :   2020/10/28 21:28:52
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


"""
冒泡排序
插入排序
选择排序
堆排序
"""

import copy
import random
import sys
sys.path.append('../')
sys.path.append('./')

from search import decorator



# 关键点在于  1. 取的范围  2. 还有循环次数 O(n**2)
@decorator
def bubble_sort(nums):
    length = len(nums)
    for i in range(length-1):
        exchange = False
        for j in range(length-i-1):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]
                exchange = True
        if not exchange:
            return 
        

# O(n**2)
@decorator
def select_sout(nums):
    length = len(nums)
    for i in range(length-1):
        min_index = i
        for j in range(i+1, length-1):
            if nums[j] < nums[min_index]:
                min_index = j
        if min_index != i:
            nums[min_index], nums[i] = nums[i], nums[min_index]


# O(n**2)
def insert_sort(nums):
    length = len(nums)
    # 注意是从1开始
    for i in range(1, length):
        tmp = nums[i]
        # j是手里的牌下标
        j = i-1
        while j>=0 and nums[j] > tmp:
            nums[j+1] = nums[j]
            j -= 1
        nums[j+1] = tmp


# 快排
# 取一个元素p（第一个元素），使元素p归位；
# 列表被p分为两部分，左边都比p小，右边都比p大；
# 递归完成排序
# O(nlogn)

# 缺点：1. 递归 最多999次
#       2. 最坏情况 倒序的话就会重复很多不必要的操作
def partition(nums, left, right):
    tmp = nums[left]
    while left < right:
        # 找比最初始值小，从右开始找
        while left < right  and nums[right] >= tmp:
            # 往左走一步
            right -= 1
        # 把右边的值写到左边空位上
        nums[left] = nums[right]
        while left < right and nums[left] <= tmp:
            left += 1
        # 把左边的值写到右边空位上
        nums[right] = nums[left]
    # tmp归位
    nums[left] = tmp
    return left


def _quick_sort(nums, left, right):
    if left < right:
        mid = partition(nums, left, right)
        _quick_sort(nums, left, mid-1)
        _quick_sort(nums, mid+1, right)

@decorator
def quick_sort(nums):
    _quick_sort(nums, 0, len(nums)-1)


# 堆排序
# 1. 建立堆
# 2. 得到堆顶元素，为最大元素
# 3. 去掉堆顶，将堆最后一个元素放到堆顶，此时可通过一次调整重新使堆有序
# 4. 堆顶元素为第二大元素
# 5. 重复3. 直到堆变空

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
        if j + 1 <= high and nums[j+1] > nums[j]:
            # j指向右孩子
             j = j+1
        if nums[j] > tmp:
            nums[i] = nums[j]
            # 往下看一层
            i = j
            j = 2*i + 1
        else:
            # tmp更大，把tmp放到i的位置上，把tmp放到某一级领导位置上
            # nums[i] = tmp
            break
    # 把tmp放到叶子节点上
    nums[i] = tmp
    # print(nums)


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


# 集成库
# q->queue 优先队列
import heapq


def heap_sort2(nums):
    # 建堆
    heapq.heapify(nums)
    print(nums)
    n = len(nums)
    for i in range(n):
        print(heapq.heappop(nums), end=', ')


if __name__ == "__main__":
    # nums = [5,7,4,6,3,1,2,9,8]
    nums = list(range(10))
    random.shuffle(nums)
    print(nums)

    nums1 = copy.deepcopy(nums)
    nums2 = copy.deepcopy(nums)
    nums3 = copy.deepcopy(nums)

    # quick_sort(nums1)
    # bubble_sort(nums2)

    # heap_sort(nums3)
    # print(nums3)
    # heap_sort2(nums3)

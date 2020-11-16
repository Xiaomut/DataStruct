#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   search.py
@Time    :   2020/10/28 21:04:34
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

import time


def decorator(func):
   def wrapper(*args, **kwargs):
       t1 = time.time()
       result = func(*args, **kwargs)
       t2 = time.time()
       print(f'{func.__name__} running time: {t2-t1:.2f} secs.')
       return result
   return wrapper


@decorator
def linear_search(li, target):
    for index, i in enumerate(li):
        if i == target:
            return index
    return None


@decorator
def binary_search(li, target):
    left = 0
    right = len(li) - 1
    while left <= right:
        mid = (right + left) // 2
        if li[mid] < target:
            left = mid + 1
        elif li[mid] > target:
            right = mid - 1
        else:
            return mid
    return None


if __name__ == "__main__":
    li = list(range(10000000))
    linear_search(li, 500000)
    binary_search(li, 500000)
    # linear_search running time: 0.05 secs.
    # binary_search running time: 0.00 secs.
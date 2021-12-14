#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   7. reOrderArrayTwo.py
@Time    :   2021/10/19 15:48:00
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

def reOrderArrayTwo(array):
    left = 0
    right = len(array) - 1
    
    while left < right:
        while left < right and array[left] % 2 != 0:
            left += 1
        while left < right and array[right] % 2 == 0:
            right -= 1
        array[right], array[left] = array[left], array[right]
    return array


if __name__ == "__main__":
    test = [1,2,3,4]
    res = reOrderArrayTwo(test)
    print(res)
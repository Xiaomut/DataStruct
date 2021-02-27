#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   maxArea.py
@Time    :   2020/11/14 13:51:55
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

"""
11. Container With Most Water
"""

def maxArea(height):
    # dicts = {}
    n = len(height)
    output = 0
    for h in range(n-1):
        for i in range(h+1, n):
            low_num = min(height[h], height[i])
            water_num = low_num * (i - h)
            output = max(water_num, output)
            # print(str(i-h) + f'water_num: {water_num}')
    return output


print(maxArea([1,2,1]))
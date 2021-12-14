#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   activity_selection.py
@Time    :   2021/10/08 17:07:17
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
activities.sort(key=lambda x: x[1])
# print(activities)

# 贪心算法
def activity_selection(a):
    res = [a[0]]
    for i in range(1, len(a)):
        # 当前活动的开始时间小于等于最后一个入选活动的结束时间
        if a[i][0] >= res[-1][1]:  
            # 不冲突
            res.append(a[i])
    return res


if __name__ == "__main__":
    print(activity_selection(activities))
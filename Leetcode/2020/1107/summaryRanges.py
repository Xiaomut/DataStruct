#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   summaryRanges.py
@Time    :   2020/11/07 18:23:22
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

def summaryRanges(nums):

    res = []
    length = len(nums)
    if nums == []:
        return []
    elif length == 1:
        return [str(nums[0])]
    i = 0
    while i < length:
        if i == length - 1:
            res.append(str(nums[i]))
            return res
        flag = False
        tmp = nums[i]  # 存储最初的值
        # tmp_num = 0
        for index, j in enumerate(nums[i+1:], i+1):
            if j != (nums[index-1] + 1):
                if not flag:
                    print(f'{[nums[i], nums[i]]} --> "{nums[i]}"')
                    res.append(str(nums[i]))
                    i += 1
                    break
                else:
                    print(f'{[tmp, nums[index-1]]} --> "{tmp}->{nums[index-1]}"')
                    res.append(str(tmp)+'->'+str(nums[index-1]))
                    i += 1
                    break
            else:
                flag = True
                i += 1
                if i == (length - 1):
                    res.append(str(tmp)+'->'+str(nums[index]))
                    return res
    return res


# def summaryRanges(nums):
#     res = '*'
    


res = summaryRanges([0,1,2,4,5,7])
print(res)

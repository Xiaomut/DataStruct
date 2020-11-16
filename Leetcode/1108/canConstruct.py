#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   canConstruct.py
@Time    :   2020/11/08 21:25:50
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


def canConstruct(ransomNote, magazine):
    ransomNote = list(ransomNote)
    magazine = list(magazine)
    for ran in ransomNote:
        if ran not in magazine:
            return False
        else:
            try:
                magazine.remove(ran)
            except:
                return False
    return True

# def canConstruct(ransomNote, magazine):
#     nums = {}
#     for ran in ransomNote:
#         nums[ran] = nums.get(ran, 0) + 1
#     for mag in magazine:
#         if mag in nums.keys():
#             nums[mag] -= 1
#     for i in nums.values():
#         if i > 0:
#             return False
#     return True

print(canConstruct(ransomNote = "aa", magazine = "ab"))
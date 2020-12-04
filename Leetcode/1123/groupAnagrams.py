#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   groupAnagrams.py
@Time    :   2020/11/23 17:31:06
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

# 49. Group Anagrams


def groupAnagrams(strs):
    dicts = {}

    for s in strs:
        # values = list(s)
        # print(values)
        value = {}
        for i in s:
            if i not in value.keys():
                value[i] = 1
            else:
                value[i] += 1
        # print(list(value.items()))
        tmp_key = str(sorted(list(value.items())))
        if tmp_key not in dicts.keys():
            dicts[tmp_key] = [s]
        else:
            dicts[tmp_key].append(s)
    return list(dicts.values())


print(groupAnagrams(strs=["eat", "tea", "tan", "ate", "nat", "bat"]))

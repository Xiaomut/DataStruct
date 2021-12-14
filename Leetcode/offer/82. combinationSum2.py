#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   82. combinationSum2.py
@Time    :   2021/12/10 15:45:26
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

"""
给定一个可能有重复数字的整数数组 candidates 和一个目标数 target ，找出 candidates 中所有可以使数字和为 target 的组合。

candidates 中的每个数字在每个组合中只能使用一次，解集不能包含重复的组合。 
"""
from typing import List


def combinationSum2(candidates: List[int], target: int) -> List[List[int]]:

    def dfs(candidates, begin, end, path, res, target):
        if target == 0:
            res.append(path)
            return res
        
        for index in range(begin, end):
            residue = target - candidates[index]
            if residue < 0:
                break
            if index > begin and candidates[index-1] == candidates[index]:
                continue
            dfs(candidates, index+1, end, path+[candidates[index]], res, residue)
    
    res = []
    candidates.sort()
    dfs(candidates, 0, len(candidates), [], res, target)

    return res


if __name__ == "__main__":

    candidates = [10,1,2,7,6,1,5]
    target = 8
    res = combinationSum2(candidates, target)
    print(res)
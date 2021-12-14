#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   81. combinationSum.py
@Time    :   2021/12/09 10:54:59
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''


"""
剑指 Offer II 081. 允许重复选择元素的组合
给定一个无重复元素的正整数数组 candidates 和一个正整数 target ，找出 candidates 中所有可以使数字和为目标数 target 的唯一组合。
candidates 中的数字可以无限制重复被选取。如果至少一个所选数字数量不同，则两种组合是唯一的。 
对于给定的输入，保证和为 target 的唯一组合数少于 150 个。

示例 1：
输入: candidates = [2,3,6,7], target = 7
输出: [[7],[2,2,3]]

示例 2：
输入: candidates = [2,3,5], target = 8
输出: [[2,2,2,2],[2,3,3],[3,5]]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/combination-sum
"""

from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        def dfs(candidates, begin, size, path, res, target):
            print(f'dfs(candidates: {candidates}, begin: {begin}, size: {size}, path: {path}, res: {res}, target: {target}')
            if target < 0:
                return
            if target == 0:
                res.append(path)
                return

            for index in range(begin, size):
                dfs(candidates, index, size, path + [candidates[index]], res, target - candidates[index])

        size = len(candidates)
        if size == 0:
            return []
        path = []
        res = []
        dfs(candidates, 0, size, path, res, target)
        return res

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

        def dfs(candidates, begin, size, path, res, target):
            print(f'dfs(candidates: {candidates}, begin: {begin}, size: {size}, path: {path}, res: {res}, target: {target}')
            if target == 0:
                res.append(path)
                return

            for index in range(begin, size):
                residue = target - candidates[index]
                if residue < 0:
                    break

                dfs(candidates, index, size, path + [candidates[index]], res, residue)

        size = len(candidates)
        if size == 0:
            return []
        candidates.sort()
        path = []
        res = []
        dfs(candidates, 0, size, path, res, target)
        return res



if __name__ == "__main__":
    solution = Solution()
    res = solution.combinationSum2(candidates = [2,3,6,7], target = 7)
    print(res)
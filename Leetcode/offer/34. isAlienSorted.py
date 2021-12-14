#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   34. isAlienSorted.py
@Time    :   2021/12/10 11:33:31
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

from typing import List


def isAlienSorted(words: List[str], order: str) -> bool:
    dic = {}
    for i in range(len(order)):
        dic[order[i]] = i
    
    length = len(words)

    for l in range(1, length):
        for s in range(len(words[l-1])):
            try:
                tmp = words[l-1][s]
                tmp2 = words[l][s]
                if dic[words[l-1][s]] < dic[words[l][s]]:
                    break
                else:
                    return False
            except:
                return False
    return True


if __name__ == "__main__":
    words = ["fxasxpc","dfbdrifhp","nwzgs","cmwqriv","ebulyfyve","miracx","sxckdwzv","dtijzluhts","wwbmnge","qmjwymmyox"]
    order = "zkgwaverfimqxbnctdplsjyohu"
    res = isAlienSorted(words, order)
    print(res)
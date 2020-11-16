#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   maze.py
@Time    :   2020/11/11 21:21:58
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,1,0,0,0,1,0,1],
    [1,0,0,1,0,0,0,1,0,1],
    [1,0,0,0,0,1,1,0,0,1],
    [1,0,1,1,1,0,0,0,0,1],
    [1,0,0,0,1,0,0,0,0,1],
    [1,0,1,0,0,0,1,0,0,1],
    [1,0,1,1,1,0,1,1,0,1],
    [1,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]

directs = [
    lambda x,y: (x+1, y),
    lambda x,y: (x-1, y),
    lambda x,y: (x, y-1),
    lambda x,y: (x, y+1)
]

def maze_path(x1,y1,x2,y2):
    stack = []
    stack.append((x1, y1))
    while len(stack) > 0:
        # 当前节点
        cur_node = stack[-1] 
        if cur_node[0] == x2 and cur_node[1] == y2:
            for p in stack:
                print(p)
            return True
        # (x,y) 四个方向 为 (x-1, y); (x+1, y); (x, y-1); (x, y+1)
        for direct in directs:
            next_node = direct(cur_node[0], cur_node[1])
            # 如果下一个节点能走
            if maze[next_node[0]][next_node[1]] == 0:
                stack.append(next_node)
                # 标记为已走过的路程
                maze[next_node[0]][next_node[1]] = 2
                break
        maze[next_node[0]][next_node[1]] = 2
        stack.pop()
    return False


maze_path(1,1,8,8)
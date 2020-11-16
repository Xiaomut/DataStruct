#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   maze_q.py
@Time    :   2020/11/12 09:56:59
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


"""
思路：从一个节点开始，寻找所有接下来能继续走的点，继续不断寻找，
      直到找到出口
使用队列存储当前正在考虑的节点
"""

from collections import deque

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

def print_r(path):
    cur_node = path[-1]
    real_path = []
    while cur_node[2] == -1:
        real_path.append(cur_node[0:2])
        cur_node = path[cur_node[2]]
    # 起点
    real_path.append(cur_node[0:2])
    real_path.reverse()
    for i in real_path:
        print(i)


def maze_path_queue(x1, y1, x2, y2):
    queue = deque()
    queue.append((x1, y1, -1))
    path = []
    while len(queue) > 0:
        # 当前节点，出队
        cur_node = queue.pop()
        path.append(cur_node)
        if cur_node[0] == x2 and cur_node[1] == y2:
            print_r(path)
            return True
        for direct in directs:
            next_node = direct(cur_node[0], cur_node[1])
            if maze[next_node[0]][next_node[1]] == 0:
                # 后续节点进队，记录哪个节点带进来的
                queue.append((next_node[0], next_node[1], len(path)-1))
                # 标记为已走过
                maze[next_node[0]][next_node[1]] = 2
    return False


maze_path_queue(1,1,8,8)
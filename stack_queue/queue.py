#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   queue.py
@Time    :   2020/11/12 09:45:04
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

class Queue:
    def __init__(self, size=100):
        self.queue = [0 for _ in range(size)]
        self.size = size
        self.rear = 0   # 队尾指针
        self.front = 0  # 队首指针

    def push(self, element):
        if not self.is_full():
            self.rear = (self.rear + 1) % self.size
            self.queue[self.rear] = element
        else:
            raise IndexError("Queue is full")

    def pop(self):
        if not self.is_empty():
            self.front = (self.front + 1) % self.size
            return self.queue[self.front]
        else:
            raise IndexError('Queue is empty.')

    def is_empty(self):
        return self.rear == self.front

    def is_full(self):
        return (self.rear + 1) % self.size == self.front


from collections import deque

q = deque()



if __name__ == "__main__":
    q = Queue(5)
    # 之能存n-1
    for i in range(4):
        q.push(i)

# Definition for singly-linked list.
import sys
sys.path.append('X:/python/DataStruct/list')

from link_list import create_linklist_head, create_linklist_tail, print_linklist


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution(object):
    def getIntersectionNode(self, headA, headB):
        pA = headA
        pB = headB

        while (pA != pB):
            pA = pA.next if pA else headB
            pB = pB.next if pB else headA

        return pA
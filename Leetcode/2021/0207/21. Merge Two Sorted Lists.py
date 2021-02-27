# Definition for singly-linked list.
import sys
sys.path.append('X:/python/DataStruct/list')

from link_list import create_linklist_head, create_linklist_tail, print_linklist


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# 1. iterator
def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    res = ListNode()
    cur = res

    while l1 and l2:
        if l1.val <= l2.val:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    cur.next = l1 or l2

    return res.next


# 2. recursion
def mergeTwoLists2(l1: ListNode, l2: ListNode) -> ListNode:
    # 终止条件
    if l1 == None or l2 == None:
        return l1 or l2
    if l1.val <= l2.val:
        l1.next = mergeTwoLists(l1.next, l2)
        return l1
    else:
        l2.next = mergeTwoLists(l1, l2.next)
        return l2


if __name__ == "__main__":
    l1 = create_linklist_tail([1, 2, 3])
    l2 = create_linklist_tail([1, 2, 3])
    # print_linklist(l1)
    print_linklist(mergeTwoLists(l1, l2))

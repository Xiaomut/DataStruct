"""
输入两个单调递增的链表，输出两个链表合成后的链表，当然我们需要合成后的链表满足单调不减规则。

输入：
{1,3,5},{2,4,6}
返回值：
{1,2,3,4,5,6}
"""

import sys
sys.path.append('X:/python/DataStruct/list')

from link_list import create_linklist_head, create_linklist_tail, print_linklist, Node


def Merge(pHead1, pHead2):

    if pHead1 == [] and pHead2 == []:
        return []

    res = Node(None)
    cur = res
    
    while pHead1 is not None or pHead2 is not None:
        if pHead1 is None:
            num1 = 0
        elif pHead2 is None:
            num2 = 0
        else:
            num1 = pHead1.val
            num2 = pHead2.val
        if num1 < num2:
            cur.val = num1
            cur = cur.next
            pHead1 = pHead1.next
        else:
            cur.val = num2
            cur = cur.next
            pHead2 = pHead2.next

    return cur.next
    

if __name__ == "__main__":
    l1 = create_linklist_tail([1, 3, 5])
    l2 = create_linklist_tail([2, 4, 6])
    res = Merge(l1, l2)
    print(res)




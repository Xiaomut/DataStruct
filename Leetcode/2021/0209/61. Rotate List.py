# Definition for singly-linked list.
import sys
sys.path.append('X:/python/DataStruct/list')

from link_list import create_linklist_head, create_linklist_tail, print_linklist


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def rotateRight(head: ListNode, k: int) -> ListNode:

    count = 0
    cur = head
    while cur:
        count += 1
        cur = cur.next

    if count == 0:
        return []

    res = ListNode()
    cur = res

    def find_node(head, k):
        cur = head
        i = 0
        while i < k:
            cur = cur.next
            i += 1
        return cur

    mode = k % count if (k // count) > 0 else k
    num = 0
    # top = head
    interval = find_node(head, count - mode)

    while interval:
        cur.next = interval
        cur = cur.next
        interval = interval.next

    while num < count - mode:
        cur.next = head
        cur = cur.next
        head = head.next
        num += 1
        # print('---------------------')

    cur.next = None
    return res.next


if __name__ == "__main__":
    l1 = create_linklist_tail([1, 2, 3])
    # print_linklist(l1)
    print_linklist(rotateRight(l1, 2))
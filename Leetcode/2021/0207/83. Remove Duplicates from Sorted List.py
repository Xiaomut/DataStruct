import sys
sys.path.append('X:/python/DataStruct/list')

from link_list import create_linklist_head, create_linklist_tail, print_linklist


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def deleteDuplicates(head: ListNode) -> ListNode:
    res = ListNode()
    cur = res

    if head == []:
        return []
    if head is not None and head.val == 0:
        cur.next = head
        cur = cur.next
        head = head.next

    while head:
        if cur.val != head.val:
            cur.next = head
            cur = cur.next
            head = head.next
        else:
            head = head.next

    cur.next = None
    return res.next


if __name__ == "__main__":
    """
    Runtime: 32 ms, faster than 98.63% of Python3 online submissions for Remove Duplicates from Sorted List.
    Memory Usage: 14.2 MB, less than 85.96% of Python3 online submissions for Remove Duplicates from Sorted List.
    """
    l1 = create_linklist_tail([0, 0, 0, 0])
    # print_linklist(l1)
    # print()
    # print(deleteDuplicates(l1))
    print_linklist(deleteDuplicates(l1))
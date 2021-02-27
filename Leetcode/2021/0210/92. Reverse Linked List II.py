# Definition for singly-linked list.
import sys
sys.path.append('X:/python/DataStruct/list')

from link_list import create_linklist_head, create_linklist_tail, print_linklist


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverseBetween(head: ListNode, m: int, n: int) -> ListNode:

    if head == []:
        return []

    def find_node(head, k):
        cur = head
        i = 0
        while i < k - 1:
            cur = cur.next
            i += 1
        return cur

    m_node = find_node(head, m)
    n_node = find_node(head, n)

    temp_m_next = m_node.next
    m_node.next = n_node.next
    n_node.next = temp_m_next

    res = ListNode()
    cur = res

    # while head:
    #     if head == m_node:
    #         cur.next.val = n_node.val
    #         cur.next = head.next
    #     elif head == n_node:
    #         cur.next.val = m_node.val
    #         cur.next = head.next
    #     else:
    #         cur.next = head
    #     cur = cur.next
    #     head = head.next
    #     print(cur.val)

    cur.next = None
    return res.next


if __name__ == "__main__":
    l1 = create_linklist_tail([1, 2, 3, 4, 5])
    print_linklist(reverseBetween(l1, 2, 4))

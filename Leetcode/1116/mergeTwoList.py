class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        # l1 = self.create_linklist_tail(l1)
        # l2 = self.create_linklist_tail(l2)
        # for l1
        if l1 == [] and l2 == []:
            return []
        elif l1 == []:
            return l2
        elif l2 == []:
            return l1
        else:
            head = ListNode(l1[0])

    def create_linklist_tail(self, nums):
        if len(nums) > 1:
            head = ListNode(nums[0])
            tail = head
            for element in nums[1:]:
                node = ListNode(element)
                tail.next = node
                tail = node
            return head
        elif len(nums) == 1:
            return ListNode(nums[0])
        else:
            return []
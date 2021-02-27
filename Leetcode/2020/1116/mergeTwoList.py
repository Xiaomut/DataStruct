class ListNode:
    def __init__(self, item):
        self.item = item
        self.next = None

    # def __iter__(self):
    #     return self


"""
链表失败了！！！
优化方法：
插值排序，快速排序等

查找法，二分查找法
"""


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
            if len(l1) < len(l2):
                node_list = self.create_linklist_tail(l1)
                tmp_list = l2
            else:
                node_list = self.create_linklist_tail(l2)
                tmp_list = l1

            # print(node_list)

            while node_list:
                num = node_list.item
                tmp = node_list  # 保存前一个值
                for index2, j in enumerate(tmp_list):
                    if num < j:
                        tmp = node_list
                        node_list = node_list.next
                        if not node_list:
                            node_list = tmp
                            node_list.next = j
                        else:
                            break
                    else:
                        node = ListNode(j)
                        node_list.next = node
                        tmp.next = node_list.item
                        tmp_list.pop(0)
            return node_list

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


solu = Solution()
res = solu.mergeTwoLists(l1=[1, 2, 4], l2=[1, 3, 4])
print(res)
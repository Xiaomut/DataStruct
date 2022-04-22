# 链表

- 尾插法是正序

```py
class Node:
    def __init__(self, val=0):
        self.val = val
        self.next = None


# 头插法
def create_linklist_head(nums):
    head = Node(nums[0])
    for element in nums[1:]:
        node = Node(element)
        node.next = head
        head = node
    return head


def create_linklist_tail(nums):
    head = Node(nums[0])
    tail = head
    for element in nums[1:]:
        node = Node(element)
        tail.next = node
        tail = node
    return head
```

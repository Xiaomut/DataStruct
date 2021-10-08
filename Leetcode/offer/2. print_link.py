import sys
sys.path.append('X:/python/DataStruct/list')

from link_list import create_linklist_head, create_linklist_tail, print_linklist


def printListFromTailToHead(listNode):
        
    if listNode == None:
        return []
    
    res = []
    while listNode is not None:
        res.append(listNode.next.head)
        listNode = listNode.next
    
    return res[::-1]


if __name__ == "__main__":
    l1 = create_linklist_tail([1, 2, 3, 4, 5])
    # print_linklist(l1)
    res = printListFromTailToHead(l1)
    print(res)

"""
有一个长度为N的升序数组，比如[1,2,3,4,5]，将它进行旋转，即把一个数组最开始的若干个元素搬到数组的末尾，变成一个旋转数组，比如变成了[3,4,5,1,2]，或者[4,5,1,2,3]这样的。请问，给定这样一个旋转数组，求它的最小值。

[3,4,5,1,2]
1
"""


def minNumberInRotateArray(rotateArray):
    res = rotateArray[0]
    for i in range(len(rotateArray) - 1):
        if rotateArray[i] > rotateArray[i + 1]:
            res = rotateArray[i + 1]
            return res
    return res


if __name__ == "__main__":

    data = [1,2,2,2,2,2]
    res = minNumberInRotateArray(data)
    print(res)
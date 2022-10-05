# STL 迭代器设计原理

先看一段代码

```c++
#include <algorithm>
#include <iterator>
#include <list>
#include <iostream>
using namespace std;


int main() {
list<int> coll;

for (int i = 1; i <= 6; ++i) {
coll.push_front(i);
coll.push_back(i);
}

remove(coll.begin(), coll.end(), 3);

copy(coll.cbegin(), coll.cend(), ostream_iterator<int>(cout, " "));

cout << endl;
}
```

这段代码的执行结果是

```bash
6 5 4 2 1 1 2 4 5 6 5 6
```

令人疑惑的是为什么答案不是

```bash
6 5 4 2 1 1 2 4 5 6
```

反而最后面两个元素没有被删除，list 的 size 没有改变，也就是说为什么没有实现(或者说调用) `list.erase()` ， 毕竟这样的话看起来更加的合理。

原因与 STL 的迭代器设计原则有关，**迭代器的设计目的是将 数据结构（容器等）和算法进行分离。**迭代器是容器内部某个位置的抽象概念，迭代器对所属的容器一无所知，任何以迭代器访问容器的算法，都不得通过迭代器调用容器类所提供的任何成员函数。


# remove_if 函数

在《C++标准库第二版》函数对象一章看到的一个例子

```c++
#include <iostream>
#include <list>
#include <algorithm>
using namespace std;

class Nth {
private:
    int nth;
    int count;
public:
    Nth (int n) : nth(n), count(0) {}

    bool operator() (int) {
        return ++count == nth;
    }
};

int main() {
    list <int> coll {1,2,3,4,5,6,7,8,9,10};
    auto pos = remove_if(coll.begin(), coll.end(), Nth(3));
    coll.erase(pos, coll.end());
    for (auto elm : coll) {
        cout << elm << " ";
    }
}

```

实际执行结果是

```bash
1 2 4 5 7 8 9 10 
```

可以发现第三个数和第六个数都被删除了。

原因和 remove_if 的实现有关(下面是g++9.2.1里面的实现)

```c++
  template<typename _ForwardIterator, typename _Predicate>
    _ForwardIterator
    __remove_if(_ForwardIterator __first, _ForwardIterator __last,
		_Predicate __pred)
    {
      __first = std::__find_if(__first, __last, __pred);
      if (__first == __last)
	return __first;
      _ForwardIterator __result = __first;
      ++__first;
      for (; __first != __last; ++__first)
	if (!__pred(__first))
	  {
	    *__result = _GLIBCXX_MOVE(*__first);
	    ++__result;
	  }
      return __result;
    }
```


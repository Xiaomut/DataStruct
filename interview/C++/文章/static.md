**转载**

> [C++ 类中的static成员的初始化和特点](https://blog.csdn.net/men_wen/article/details/64443040)

```c++
#include <iostream>
using namespace std;

class Test{
public:
    int a1;
    int a2 = 4;
    
    int& b1;
    int& b2 = a2;
    
    const int c1;
    const int c2 = 10;
    
    static int d1;
    // static int d2 = 22; //  错误：ISO C++ 不允许在类内初始化非常量静态成员‘Test::d2’
    
    const static int e1;
    const static int e2 = 20;
    
    Test(int k1, int k2) : b1(k1), c1(k2) {};
    
};

int Test::d1 = 5;
const int Test::e1 = 15;

int main() {
    //Test t(2, 3);
    
    return 0;
}
```

这些特殊类型的成员变量主要有：

**静态成员属于类作用域，但不属于类对象，它的生命周期和普通的静态变量一样，程序运行时进行分配内存和初始化，程序结束时则被释放。所以不能在类的构造函数中进行初始化。**

### static成员的优点

- static 成员的名字是在类的作用域中，因此可以**避免与其它类成员或全局对象名字冲突**。
- 可以实施封装，**static成员可以是私有的，而全局对象不可以**。
- 阅读程序容易看出 static 成员与某个类相关联，这种可见性可以**清晰地反映程序员的意图**。

### static 成员函数特点

- 因为 **static 成员函数没有this指针**，所以静态成员函数不可以访问非静态成员。
- 非静态成员函数可以访问静态成员。
- 静态数据成员与类的大小无关，因为静态成员只是作用在类的范围而已。

### static用法总结

- C 语言中：

  - 用于函数内部修饰变量，即函数内的静态变量。这种变量的生存期长于该函数，使得函数具有一定的“状态”。使用静态变量的函数一般是不可重入的，也不是线程安全的，比如strtok(3)。
    - 用在文件级别（函数体之外），修饰变量或函数，表示该变量或函数只在本文件可见，其他文件看不到也访问不到该变量或函数。专业的说法叫“具有internal linkage”（简言之：不暴露给别的translation unit）。
    
- c++语言中（由于 C++ 引入了类，在保持与C语言兼容的同时，static关键字又有了两种新用法）：

  - 用于修饰类的数据成员，即所谓“静态成员”。这种数据成员的生存期大于class的对象（实例/instance）。静态数据成员是每个class有一份，普通数据成员是每个instance 有一份。
- 用于修饰class的成员函数，即所谓“静态成员函数”。这种成员函数只能访问静态成员和其他静态程员函数，不能访问非静态成员和非静态成员函数。
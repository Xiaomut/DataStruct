​		mutalbe 的中文意思是“可变的，易变的”，跟 constant（既C++中的const）是反义词。在 C++ 中，mutable也是为了突破 const 的限制而设置的。被 mutable 修饰的变量，将永远处于可变的状态，即使在一个 const 函数中。

　　我们知道，如果类的成员函数不会改变对象的状态，那么这个成员函数一般会声明成 const 的。但是，有些时候，我们需要在 const 的函数里面修改一些跟类状态无关的数据成员，那么这个数据成员就应该被 mutalbe 来修饰。

​		下面是一个小例子：

```c++
#include <iostream>
using namespace std;

class ClxTest {
public:
    void Output() const;
};

void ClxTest::Output() const
{
    cout << "Output for test!" << endl;
}

void OutputTest(const ClxTest& lx)
{
    lx.Output();
}
```

​		类 ClxTest 的成员函数 Output 是用来输出的，不会修改类的状态，所以被声明为 const 的。函数 OutputTest 也是用来输出的，里面调用了对象 lx 的 Output 输出方法，为了防止在函数中调用其他成员函数修改任何成员变量，所以参数也被const 修饰。

　　如果现在，我们要增添一个功能：计算每个对象的输出次数。如果用来计数的变量是普通的变量的话，那么在 const 成员函数 Output 里面是不能修改该变量的值的；而该变量跟对象的状态无关，所以应该为了修改该变量而去掉 Output 的 const 属性。这个时候，就该我们的 mutable 出场了——只要用 mutalbe 来修饰这个变量，所有问题就迎刃而解了。

​		下面是修改过的代码：

```c++
#include <iostream>
using namespace std;

class ClxTest {
public:
    ClxTest();
    ~ClxTest();
    void Output() const;
    int GetOutputTimes() const;

private:
    mutable int m_iTimes;
};

ClxTest::ClxTest()
{
    m_iTimes = 0;
}

ClxTest::~ClxTest()
{
}

void ClxTest::Output() const
{
    cout << "Output for test!" << endl;
    m_iTimes++;
}

int ClxTest::GetOutputTimes() const
{
    return m_iTimes;
}

void OutputTest(const ClxTest& lx)
{
    cout << lx.GetOutputTimes() << endl;
    lx.Output();
    cout << lx.GetOutputTimes() << endl;
}
```

计数器 m_iTimes 被 mutable 修饰，那么它就可以突破 const 的限制，在被 const 修饰的函数里面也能被修改。

### 其他理解

​		const 意思是“这个函数不修改对象内部状态”。为了保证这一点，编译器也会主动替你检查，确保你没有修改对象成员变量，否则内部状态就变了。mutable 意思是“这个成员变量不算对象内部状态”。

​		比如，你搞了个变量，用来统计某个对象的访问次数（比如供 debug 用）。它变成什么显然并不影响对象功用，但编译器并不知道：它仍然会阻止一个声明为 const 的函数修改这个变量。把这个计数变量声明为 mutable，编译器就明白了：这个变量不算对象内部状态，修改它并不影响 const 语义，所以就不需要禁止 const 函数修改它了。
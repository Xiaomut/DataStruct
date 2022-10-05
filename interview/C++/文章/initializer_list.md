**转载**

> [c++initializer_list详解](https://blog.csdn.net/fengxinlinux/article/details/72614874)

​		initializer_list是C++11提供的新类型，定义在头文件中。用于表示某种特定类型的值的数组，和vector一样，initializer_list也是一种模板类型。

​		要介绍initializer_list的使用，有必要先谈一谈列表初始化。C++11 扩大了初始化列表的适用范围，使其可用于所有内置类型和用户定义的类型。无论是初始化对象还是某些时候为对象赋新值，都可以使用这样一组由花括号括起来的初始值了。使用初始化列表时，可添加 =，也可不添加。

```c++
//定义一个变量并初始化
int units_sold=0;
int units_sold(0);
int units_sold={0};  //列表初始化
int units_sold{0};    //列表初始化
```

​		当初始化列表用于内置类型的变量时，这种初始化形式有一个重要特点：如果我们使用列表初始化值存在丢失信息的风险，则编译器将报错：

```c++
int main() {
    float fl = 10; 
    int a = {fl}; // 警告：narrowing conversion of ‘fl’ from ‘float’ to ‘int’
}
```

​		列表初始化就谈到这里，接下来介绍 initializer_list 的使用。它提供的操作如下:

```c++
initializer_list<T> lst; 
//默认初始化；T类型元素的空列表
initializer_list<T> lst{a,b,c...};
//lst的元素数量和初始值一样多；lst的元素是对应初始值的副本
lst2(lst)   
lst2=lst  
//拷贝或赋值一个initializer_list对象不会拷贝列表中的元素；拷贝后，原始列表和副本元素共享
lst.size()  //列表中的元素数量
lst.begin()  //返回指向lst中首元素的指针
lst.end()   //返回指向lst中尾元素下一位置的指针
```

​		**需要注意的是, initializer_list 对象中的元素永远是常量值，我们无法改变initializer_list 对象中元素的值。并且，拷贝或赋值一个 initializer_list 对象不会拷贝列表中的元素，其实只是引用而已，原始列表和副本共享元素。**

​		和使用 vector 一样，我们也可以使用迭代器访问 initializer_list 里的元素。

```c++
void error_msg(initializer_list<string> il)
{
   for(auto beg=il.begin();beg!=il.end();++beg)
      cout<<*beg<<" ";
   cout<<endl;
}
```

​		如果想向initializer_list形参中传递一个值的序列，则必须把序列放在一对花括号内：

```c++
// expected 和 actual 是 string 对象
if(expected != actual)
   error_msg({"functionX",expectde,actual});
else
   error_msg({"functionX","okay"});
```

​		说了这么多，那 initializer_list 到底有什么应用呢？有了 initializer_list 之后，对于 STL 的 container 的初始化就方便多了,比如以前初始化一个 vector 需要这样：

```c++
std::vector v;
v.push_back(1);
v.push_back(2);
v.push_back(3);
v.push_back(4);
```

​		而现在 c++11 添加了 initializer_list 后，我们可以这样初始化:

```c++
std::vector v = { 1, 2, 3, 4 };
```

​		并且，C++11允许构造函数和其他函数把初始化列表当做参数。

```c++
#include <iostream>
#include <vector>

class MyNumber {
public:
    MyNumber(const std::initializer_list<int>& v)
    {
        for (auto itm : v) {
            mVec.push_back(itm);
        }
    }

    void print()
    {
        for (auto itm : mVec) {
            std::cout << itm << " ";
        }
    }

private:
    std::vector<int> mVec;
};

int main()
{
    MyNumber m = { 1, 2, 3, 4 };
    m.print(); // 1 2 3 4

    return 0;
}
```


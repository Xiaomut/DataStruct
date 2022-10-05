**转载**

> [C++类型转换：隐式类型转换、类类型转换、显示类型转换](https://segmentfault.com/a/1190000016582440)

​		C++ 语言是一种强类型语言，当我们需要用一种类型的对象来替代另一种类型的对象进行相关操作时，必须首先进行类型转换。在 C++ 语言中，类型转换有两种方式，隐式类型转换和显式类型转换。今天我们就来聊一聊这些类型转换的具体意义和应用特点。

## 1. 隐式类型转换

​		在有隐式类型转换的表达式中，使用者不需要明确指定一个类型的对象该转换为另外哪一个类型，这个工作将隐含地由编译器来完成，编译器将分析表达式的含义，进行类型转换。

​		隐式类型转换针对不同的类型有不同的转换方式，总体可以分为两种类型，算术类型和类类型。

### 1.1 算术类型转换

​		算术类型转换的设计原则就是尽可能避免损失精度。

​		具体地，有以下几条参考规则：

1. **整型提升：将小整数类型转换成较大的整数类型**。例如，如果一个运算对象的类型是long double，那么另外一个运算对象，无论它的类型是什么，都会被转换成long double。
2. **有符号类型转换为无符号类型**。类型转换一般不会改变对象内存的值，当一个有符号类型的对象转换为无符号类型时，其表示出来的值可能发生变化，例如，int a = -1 (0xff); unsigned int b = a; 则b的值为255。
3. **在条件判断中，非布尔类型自动转换为布尔类型**。如果指针或算术类型的值为 0，转换为 false，否则转换为 true。

### 1.2 类类型转换

​		在 C++ 中，可以通过定义单参数构造函数和转换函数来进行类类型转换，这种方式也称为用户定义的转换（User-Defined Conversion）。这种方式在使用的时候不需要指明转换类型，而是由编译器自动进行选择转换函数，所以也是一种隐式类型转换。

​		用户定义的类类型转换可以由编译器自动执行，但是编译器每次只能执行一种类类型的转换。如果一个对象需要从类型 A 自动转换为类型 C，则类型 A 必须有直接转换为类型 C 的函数，不允许类型 A 转换为类型 B，然后类型 B 转换为类型C。

#### 1.2.1 转换构造函数

​		如果一个类的某个构造函数只接受一个参数，且没有被声明为 explicit，则它实际上定义了将这个参数的类型转换为此类类型的隐式转换机制，我们把这种构造函数称为转换构造函数。在转换构造函数中只允许一步类类型的转换。

​		最常见的例子就是将 C 类型字符串转换为 string 类型，例如 `string s = "hello world"`，因为 string 类有一个构造函数 `string(const char *s)`，所以 `"hello world"` 字符串可以自动转换为一个 string 类型的临时变量，然后将这个临时变量的值复制到 s 中。

​		我们可以自定义一个类类型如下：

```c++
class Sales_data {
public:
    Sales_data() = default;
    Sales_data(const std::string& s)
        : bookNo(s)
    {
    }
    Sales_data(const std::string& s, unsigned n, double p)
        : bookNo(s)
        , units_sold(n)
        , revenue(p * n)
    {
    }
    Sales_data(std::istream&);

    std::string isbn() const { return bookNo; }
    Sales_data& combine(const Sales_data&);

private:
    std::string bookNo;
    unsigned units_sold;
    double revenue;
};
```

​		在上述例子中，由于Sales_data( const std::string &s )；构造函数的存在，因此存在 string 类型到 Sales_data 的转换，因此在需要 Sales_data 对象的时候，我们可以使用 string 类型替代。

```c++
Sales_data item;
string null_book = "9-999-99999-9";
item.combine( null_book );
```

​		只有一次的隐式类类型转换是可行的，而 item.combine( "9-999-99999-9" )是错误的，因为在该语句中，存在着两次隐式转换，一次是字符串常量"9-999-99999-9"到string的转换，另一次是string到Sales_data的转换。

**explicit constructors**： 
		如果你不想隐式转换，以防用户误操作怎么办？ 
		可以通过将构造函数声明为 explicit 来阻止隐式转换。explicit 构造函数只能用于直接初始化。不允许编译器执行其它默认操作（比如类型转换，赋值初始化）。**关键字 explicit 只对一个实参的构造函数有效。**

#### 1.2.2 类型转换函数

​		在类类型转换中，我们通常有两个需求，一个是将其他类型的数据转换为我们自定义类的类型，另一个是将自定义类的类型在需要的时候转换为其他的数据类型。转换构造函数能很好地满足前一个需求，针对后面一个需求，我们除了可以使用普通的成员函数进行显示转换，在 C++ 中，还可以使用类型转换函数进行隐式转换。类型转换函数的作用就是将一个类的对象转换成另一类型的数据。

​		我们经常写下述代码：

```c++
while( cin >> num ){
    ...
}
```

​		输入操作符 >> 是二元操作符，返回左操作数作为其表达式结果，因此 cin >> num 返回 cin, 然而cin是输入流istream的对象，该对象能出现在条件表达式中，是因为在istream中定义了类型转换函数 operator bool();

​		类型转换函数一般形式：

```c++
operator 目标类型()
{
    ...
    return 目标类型数据;
}
```

​		例如：

```c++
class A {
public:
    A(const int x) : _x(x) {}
    operator int() { return _x; }
private:
    int _x;
};

int main () {
    A a(10);
    int res = a + 20;
    std::cout << res << std::endl;
}
```

​		输出结果为30. 由于类 A 定义了从该类对象到 int 类型的转换函数，所以在进行整数算术运算的时候，可以直接使用该类对象，因为编译器会隐式地调用该类型转换函数将类对象转换为整型数据。

## 2. 显式类型转换

​		显式类型转换就是在表达式中明确指定将一种类型转换为另一种类型。隐式类型转换一般是由编译器进行转换操作，显示类型转换是由程序员写明要转换成的目标类型。显示类型转换又被称为强制类型转换。

### 2.1 C 风格的强制转换

​		C 风格的强制转换很简单，不管什么类型的转换都可以使用使用下面的方式。

```c++
type val = (type)(expression);
```

​		当然，C++ 支持 C 风格的强制转换，但是 C 风格的强制转换可能带来一些隐患，让一些问题难以察觉。

### 2.2 C++ 命名强制类型转换

​		C++ 提供了 4 个命名的强制类型转换，它们都有如下的基本形式：

```c++
type val = cast-name<type>(expression);
```

​		cast-name 是 static_cast、dynamic_cast、const_cast、reinterpret_cast 中的一种。在这里简单探讨一下。

#### 2.1.1 static_cast

​		static_cast 很像 C 语言中的旧式类型转换。它能进行基础类型之间的转换，也能将带有可被单参调用的构造函数或用户自定义类型转换操作符的类型转换，还能在存有继承关系的类之间进行转换（即可将基类转换为子类，也可将子类转换为基类），还能将 non-const 对象转换为 const 对象（注意：反之则不行，那是 const_cast 的职责）。

​		static_cast 转换时并不进行运行时安全检查，所以是非安全的，很容易出问题。因此 C++ 引入 dynamic_cast 来处理安全转型。

#### 2.1.2 dynamic_cast

​		dynamic_cast 主要用来在继承体系中的安全向下转型,是实现多态的一种方式。

​		它能安全地将指向基类的指针转型为指向子类的指针或引用，并获知转型动作成功是否。如果转型失败会返回 NULL（转型对象为指针时）或抛出异常（转型对象为引用时）。dynamic_cast 会使用运行时信息（RTTI）来进行类型安全检查，因此 dynamic_cast 存在一定的效率损失。（我曾见过属于优化代码80/20法则中的20那一部分的一段游戏代码，起初使用的是 dynamic_cast，后来被换成 static_cast 以提升效率，当然这仅是权宜之策，并非好的设计。)

#### 2.1.3 const_cast

​		前面提到 const_cast 可去除对象的常量性（const），它还可以去除对象的易变性（volatile）。const_cast 的唯一职责就在于此，若将 const_cast 用于其他转型将会报错。

#### 2.1.4 reinterpret_cast

​		reinterpret_cast 用来执行低级转型，如将执行一个 int 的指针强转为 int。其转换结果与编译平台息息相关，不具有可移植性，因此在一般的代码中不常见到它。reinterpret_cast 常用的一个用途是转换函数指针类型，即可以将一种类型的函数指针转换为另一种类型的函数指针，但这种转换可能会导致不正确的结果。总之，reinterpret_cast 只用于底层代码，一般我们都用不到它，如果你的代码中使用到这种转型，务必明白自己在干什么。

以上内容部分来自网上其他的博客，参考：

> 1. [https://www.cnblogs.com/chio/...](https://www.cnblogs.com/chio/archive/2007/07/18/822389.html)
> 2. [https://blog.csdn.net/kesalin...](https://blog.csdn.net/kesalin/article/details/8119586)
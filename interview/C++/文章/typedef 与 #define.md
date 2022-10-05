**转载**

> [typedef和#define的用法与区别](https://www.cnblogs.com/kerwinshaw/archive/2009/02/02/1382428.html)

## 一、typedef 的用法

​		在 C/C++ 中，typedef 常用来定义一个标识符及关键字的别名，它是语言编译过程的一部分，但它并不实际分配内存空间，例如：

```c++
typedef    int       INT;
typedef    int       ARRAY[10];
typedef   (int*)   pINT;
```

​		typedef 可以增强程序的可读性，以及标识符的灵活性，但它也有“非直观性”等缺点。

## 二、#define 的用法

​		#define 为一宏定义语句，通常用它来定义常量(包括无参量与带参量)，以及用来实现那些“表面似和善、背后一长串”的宏，它本身并不在编译过程中进行，而是在这之前(**预处理过程**)就已经完成了，但也因此难以发现潜在的错误及其它代码维护问题。例如：

```c++
#define   INT             int
#define   TRUE         1
#define   Add(a,b)     ((a)+(b));
#define   Loop_10    for (int i=0; i<10; i++)
```

​		在 Scott Meyer 的 Effective C++ 一书的条款 1 中有关于 #define 语句弊端的分析，以及好的替代方法，大家可参看。

## 三、typedef 与 #define 的区别

​		从以上的概念便也能基本清楚，typedef 只是为了增加可读性而为标识符另起的新名称(仅仅只是个别名)，而 #define 原本在 C 中是为了定义常量，到了C++，const、enum、inline 的出现使它也渐渐成为了起别名的工具。有时很容易搞不清楚与 typedef 两者到底该用哪个好，如 `#define INT int` 这样的语句，用 typedef 一样可以完成，用哪个好呢？我主张用 typedef，因为在早期的许多C编译器中这条语句是非法的，只是现今的编译器又做了扩充。为了尽可能地兼容，一般都遵循 #define 定义“可读”的常量以及一些宏语句的任务，而 typedef 则常用来定义关键字、冗长的类型的别名。

​		宏定义只是简单的字符串代换(原地扩展)，而typedef则不是原地扩展，它的新名字具有一定的封装性，以致于新命名的标识符具有更易定义变量的功能。请看上面第一大点代码的第三行：`typedef (int*) pINT;` 以及下面这行:
`#define pINT2 int*`。

​		效果相同？实则不同！实践中见差别：`pINT a,b;` 的效果同 `int *a; int *b;` 表示定义了两个整型指针变量。而 `pINT2 a,b;` 的效果同 `int *a, b;` 表示定义了一个整型指针变量 a 和整型变量 b。

## 四、typedef 的四个用途和两个陷阱

**用途一**

​		定义一种类型的别名，而不只是简单的宏替换。可以用作同时声明指针型的多个对象。比如： `char* pa, pb; `   这多数不符合我们的意图，它只声明了一个指向字符变量的指针，和一个字符变量。以下则可行：

```c++
typedef char* PCHAR;  // 一般用大写 
PCHAR pa,pb;     // 可行，同时声明了两个指向字符变量的指针 
```

​		虽然  `char *pa, *pb;`  也可行，但相对来说没有用 typedef 的形式直观，尤其在需要大量指针的地方，typedef的方式更省事。 

**用途二**

​		用在旧的 C 代码中（具体多旧没有查），帮助 struct。以前的代码中，声明struct 新对象时，必须要带上 struct，即形式为: `struct 结构名 对象名`，如： 

```c++
struct   tagPOINT1 
{ 
    int   x; 
    int   y; 
}; 
struct   tagPOINT1   p1;   
```

​		而在 C++ 中，则可以直接写：`结构名 对象名`，即： `tagPOINT1   p1; `。 估计某人觉得经常多写一个struct太麻烦了，于是就发明了： 

```c++
typedef struct tagPOINT {
    int x;
    int y;
} POINT;

POINT p1; // 这样就比原来的方式少写了一个struct，比较省事，尤其在大量使用的时候
```

​		或许在 C++ 中，typedef 的这种用途二不是很大，但是理解了它，对掌握以前的旧代码还是有帮助的，毕竟我们在项目中有可能会遇到较早些年代遗留下来的代码。 

**用途三**

​		用 typedef 来定义与平台无关的类型。比如定义一个叫   REAL   的浮点类型，在目标平台一上，让它表示最高精度的类型为： 
`typedef long double REAL; `  
在不支持 long double 的平台二上，改为： 
`typedef double REAL;  `
在连 double 都不支持的平台三上，改为： 
`typedef float REAL; ` 

​		也就是说，当跨平台时，只要改下 typedef 本身就行，不用对其他源码做任何修改。 标准库就广泛使用了这个技巧，比如 size_t。 另外，因为 typedef 是定义了一种类型的新别名，不是简单的字符串替换，所以它比宏来得稳健（虽然用宏有时也可以完成以上的用途）。 

**用途四**

​		为复杂的声明定义一个新的简单的别名。方法是：在原来的声明里逐步用别名替换一部分复杂声明，如此循环，把带变量名的部分留到最后替换，得到的就是原声明的最简化版。举例： 

原声明：`int *(*a[5])(int, char*); `
变量名为 a，直接用一个新别名 pFun 替换 a 就可以了： 
`typedef int *(*pFun)(int, char*);` 
原声明的最简化版： 
`pFun a[5]; `  

原声明：`void (*b[10]) (void (*)()); `
变量名为 b，先替换右边部分括号里的，pFunParam 为别名一： 
`typedef void (*pFunParam)(); `
再替换左边的变量 b，pFunx 为别名二： 
`typedef void (*pFunx)(pFunParam); `
原声明的最简化版： 
`pFunx b[10]; `

原声明：`doube(*)() (*e)[9]; ` 
变量名为 e，先替换左边部分，pFuny 为别名一： 
`typedef double(*pFuny)();` 
再替换右边的变量 e，pFunParamy 为别名二 
`typedef pFuny (*pFunParamy)[9]; `
原声明的最简化版： 
`pFunParamy e; ` 

​		理解复杂声明可用的“右左法则”：从变量名看起，先往右，再往左，碰到一个圆括号就调转阅读的方向；括号内分析完就跳出括号，还是按先右后左的顺序，如此循环，直到整个声明分析完。举例： 

`int (*func)(int *p); `
		首先找到变量名 func，外面有一对圆括号，而且左边是一个 `*` 号，这说明 func 是一个指针；然后跳出这个圆括号，先看右边，又遇到圆括号，这说明`(*func)` 是一个函数，所以 func 是一个指向这类函数的指针，即函数指针，这类函数具有` int *` 类型的形参，返回值类型是 int。 

`int (*func[5])(int *); `
func 右边是一个 [] 运算符，说明 func 是具有 5 个元素的数组；func 的左边有一个 `*`，说明 func 的元素是指针（注意这里的 `*` 不是修饰 func，而是修饰 func[5]的，原因是 [] 运算符优先级比 `*` 高，func 先跟 [] 结合）。跳出这个括号，看右边，又遇到圆括号，说明 func 数组的元素是函数类型的指针，它指向的函数具有`int*` 类型的形参，返回值类型为 int。 

也可以记住2个模式： 
`type (*)(...)` 函数指针 
`type (*)[]` 数组指针   

**陷阱一** 

​		记住，typedef 是定义了一种类型的新别名，不同于宏，它不是简单的字符串替换。比如： 
先定义： 
`typedef char* PSTR; `
然后： 
`int mystrcmp(const PSTR, const PSTR); `

​		`const PSTR` 实际上相当于  `const char*`  吗？不是的，它实际上相当于`char* const`。 原因在于 const 给予了整个指针本身以常量性，也就是形成了常量指针 `char* const`。 简单来说，记住当 const 和 typedef 一起出现时，typedef 不会是简单的字符串替换就行。 

**陷阱二**

​		typedef 在语法上是一个存储类的关键字（如auto、extern、mutable、static、register等一样），虽然它并不真正影响对象的存储特性，如： 
`typedef static int INT2;`  编译将失败，会提示“指定了一个以上的存储类”。
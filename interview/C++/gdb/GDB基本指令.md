*学习过程中使用的操作系统是Centos 6， 跟着学的教程是GitChat的课程《Linux GDB调试指南》，记录下学习过程供以后复习*

> [《Linux GDB调试指南》](<https://gitbook.cn/gitchat/column/5c0e149eedba1b683458fd5f#catalog>)

# 调试信息与调试原理

## 环境配置

```shell
yum install gcc
yum install gcc-g++
yum install gdb
```

## 调试信息

使用`-g`选项在编译后的程序中保留调试符号信息

```shell
gcc -g -o hello hello.c
```

包含调试信息的程序文件会比不包含调试信息的程序大很多

```shell
[root@carl gdb_study]# ls -l hello_server
# 包含调试信息的程序大小
-rwxr-xr-x 1 root root 7696 May  4 15:27 hello_server
# 使用strip命令去除程序的调试信息
[root@carl gdb_study]# strip hello_server
[root@carl gdb_study]# ls -l hello_server
# 去除调试信息后的程序大小
-rwxr-xr-x 1 root root 4288 May  4 15:35 hello_server
```

**编译器的程序优化选项**

在实际生成调试程序时，一般不仅要加上 -g 选项，也建议关闭编译器的程序优化选项。编译器的程序优化选项一般有五个级别，从 O0 ~ O4 （ 注意第一个 O0 ，是字母 O 加上数字 0 ）， O0 表示不优化，从 O1 ~ O4 优化级别越来越高，O4 最高。这样做的目的是为了调试的时候，符号文件显示的调试变量等能与源代码完全对应起来。

# 启动GDB调试

**使用GDB调试程序的三种方式**

- gdb filename (直接调试目标程序)
- gdb attach pid (附加进程)
- gdb filename corename (调试core文件)

## 直接调试目标程序

```shell
gdb filename # 附加程序
(gdb) run # 启动程序，程序真正开始运行
```

## 附加进程

在某些情况下，一个程序已经启动了，我们想调试这个程序，但是又不想重启这个程序。可以使用 **gdb attach 进程 ID** 来将 GDB 调试器附加到程序上。使用 **detach**让程序与调试器分离

## 调试core文件

```shell
# 首先检查系统是否开启程序崩溃产生core文件的机制
ulimit -a
core file size          (blocks, -c) 0  # 从这看到系统并未开启core机制
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 7412
max locked memory       (kbytes, -l) 64
max memory size         (kbytes, -m) unlimited
open files                      (-n) 65535
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 10240
cpu time               (seconds, -t) unlimited
max user processes              (-u) 7412
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
ulimit -c unlimited  # 开启生成core文件，不限制大小
```

生成的 core 文件的默认命名方式是 core.pid

**/proc/sys/kernel/core_uses_pid** 可以控制产生的 core 文件的文件名中是否添加 PID 作为扩展，如果添加则文件内容为 1，否则为 0；**/proc/sys/kernel/core_pattern** 可以设置格式化的 core 文件保存位置或文件名

# GDB常用调试命令概览

| 命令名称    | 命令缩写 | **命令说明**                                           |
| :---------- | :------- | :----------------------------------------------------- |
| run         | r        | 运行一个程序                                           |
| continue    | c        | 让暂停的程序继续运行                                   |
| next        | n        | 运行到下一行                                           |
| step        | s        | 如果有调用函数，进入调用的函数内部，相当于 step into   |
| until       | u        | 运行到指定行停下来                                     |
| finish      | fi       | 结束当前调用函数，到上一层函数调用处                   |
| return      | return   | 结束当前调用函数并返回指定值，到上一层函数调用处       |
| jump        | j        | 将当前程序执行流跳转到指定行或地址                     |
| print       | p        | 打印变量或寄存器值                                     |
| backtrace   | bt       | 查看当前线程的调用堆栈                                 |
| frame       | f        | 切换到当前调用线程的指定堆栈，具体堆栈通过堆栈序号指定 |
| thread      | thread   | 切换到指定线程                                         |
| break       | b        | 添加断点                                               |
| tbreak      | tb       | 添加临时断点                                           |
| delete      | del      | 删除断点                                               |
| enable      | enable   | 启用某个断点                                           |
| disable     | disable  | 禁用某个断点                                           |
| watch       | watch    | 监视某一个变量或内存地址的值是否发生变化               |
| list        | l        | 显示源码                                               |
| info        | info     | 查看断点 / 线程等信息                                  |
| ptype       | ptype    | 查看变量类型                                           |
| disassemble | dis      | 查看汇编代码                                           |
| set args    |          | 设置程序启动命令行参数                                 |
| show args   |          | 查看设置的命令行参数                                   |

## GDB 补充命令

### set print object on/off

​		打开/关闭显示当前对象的真实类别。

```c++
#include <iostream>
using namespace std;

class Base {
public:
    void func1() { }
    virtual void func2() { }
};

class Derived : public Base {
public:
    void func1() { }
    void func2() { }
};

int main() {
    Base b;
    Derived d;
    Base* bp = &b;
    
    bp->func1();  // Base::func1()
    bp->func2();  // Base::func2()
    
    bp = &d;
    bp->func1();  // Base::func1()
    bp->func2();  // Derived::func2()
    
    return 0;
}
```

​		在上面的测试代码中 在执行到代码段

```c++
    bp = &d;
    bp->func1();  // Base::func1()
    bp->func2();  // Derived::func2()
```

​		的时候，如果我们没有设置 `set print object on`。那么我们尝试打印 bp 

```bash
(gdb) set print object off
(gdb) print bp
$5 = (Base *) 0x7fffffffdd98  # bp 显示为 Base指针
(gdb) ptype bp  # 打印的是 Base 类
type = class Base {
  public:
    void func1(void);
    virtual void func2(void);
} *
```

​		设置 `set print object on`

```bash
(gdb) set print object on
(gdb) print bp
$6 = (Derived *) 0x7fffffffdd98 # bp 显示是 Derived指针
(gdb) ptype bp  # 仍然打印 Base 类
type = /* real type = Derived * */  # 但是说明了真实类型
class Base {
  public:
    void func1(void);
    virtual void func2(void);
} *
```

​		所以我们可以通过 `set print object on/off` 来决定使用 print 命令的时候是否显示对象的真实类型。如果不想使用这个命令的话，使用 ptype 命令也可以知道对象的真实类型。



# GDB常用命令详解

## run(简写为r)

输入`run`命令启动程序，再次输入则重启程序

## continue(简写为c)

当GDB触发断点或者Ctrl + c 中断后，如果想让程序继续运行，输入`continue`即可

## break(简写为b)

这是添加断点的命令

- break functionname 在函数名为functionname的入口处添加一个断点
- break line 在当前文件行号为line处添加一个断点
- break filename:LineNo 在filename文件行号为LineNo处添加一个断点

```shell
// 在main函数处添加断点
(gdb) b main
```

## backtrace

可以通过 **backtrace** 命令来查看当前的调用堆栈。

## frame

如果想切换到其他堆栈处，可以使用 frame 命令（简写为 f），该命令的使用方法是“**frame 堆栈编号**（编号不加 #）”。

## info

在程序中加了很多断点，而我们想查看加了哪些断点时，可以使用 **info break** 命令。

## disable/enable

如果我们想禁用某个断点，使用“**disable 断点编号**”就可以禁用这个断点了，被禁用的断点不会再被触发；同理，被禁用的断点也可以使用“**enable 断点编号**”重新启用。

如果 **disable** 命令和 **enable** 命令不加断点编号，则分别表示禁用和启用所有断点。

## delete

使用“**delete 编号**”可以删除某个断点，如 **delete 2 3** 则表示要删除的断点 2 和断点 3。

## list

**list** 命令（简写为 l）可以查看当前断点处的代码（默认10行）。

第一次输入 **list** 命令会显示断点处前后的代码，继续输入 **list** 指令会以递增行号的形式继续显示剩下的代码行，一直到文件结束为止。当然 list 指令还可以往前和往后显示代码，命令分别是“**list +** （加号）”和“**list -** （减号）”。

## print

通过 **print** 命令（简写为 p）我们可以在调试过程中方便地查看变量的值，**也可以修改当前内存中的变量值。**

```bash
# 修改
(gdb) p a=10 
```

## ptype

GDB 还有另外一个命令叫 **ptype** ，顾名思义，其含义是“print type”，就是输出一个变量的类型。

## info

info 命令是一个复合指令，还可以用来查看当前进程的所有线程运行情况。

可以通过“thread 线程编号”切换到具体的线程上去。例如，想切换到线程 2 上去，只要输入 **thread 2** 即可。因此利用 **info thread** 命令就可以调试多线程程序。

**info** 命令还可以用来查看当前函数的参数值，组合命令是 **info args**。

## next

**next** 命令（简写为 n）是让 GDB 调到下一条命令去执行，这里的下一条命令不一定是代码的下一行，而是根据程序逻辑跳转到相应的位置。**next** 命令用调试的术语叫“单步步过”（step over），即遇到函数调用直接跳过，不进入函数体内部。

## step

**step** 命令（简写为 **s**）就是“单步步入”（step into），顾名思义，就是遇到函数调用，进入函数内部。

## finish

**finish** 命令会执行函数到正常退出该函数

## return 

**return** 命令是立即结束执行当前函数并返回，也就是说，如果当前函数还有剩余的代码未执行完毕，也不会执行了。

## until

**until** 命令（简写为 **u**）可以指定程序运行到某一行停下来。

## jump

```bash
jump <location>
```

**location** 可以是程序的行号或者函数的地址，jump 会让程序执行流跳转到指定位置执行，当然其行为也是不可控制的，例如您跳过了某个对象的初始化代码，直接执行操作该对象的代码，那么可能会导致程序崩溃或其他意外行为。如果 **jump** 跳转到的位置后续没有断点，那么 GDB 会执行完跳转处的代码会继续执行。

## disassemble

GDB 默认反汇编为 AT&T 格式的指令，可以通过 show disassembly-flavor 查看，如果习惯 intel 汇编格式可以用命令 set disassembly-flavor intel 来设置。

## set args/show args

很多程序需要我们传递命令行参数。在 GDB 调试中，很多人会觉得可以使用 **gdb filename args** 这种形式来给 GDB 调试的程序传递命令行参数，这样是不行的。正确的做法是在用 GDB 附加程序后，在使用 **run** 命令之前，使用“**set args 参数内容**”来设置命令行参数。

可以通过 **show args** 查看命令行参数是否设置成功。

如果单个命令行参数之间含有空格，可以使用引号将参数包裹起来。

如果想清除掉已经设置好的命令行参数，使用 **set args** 不加任何参数即可。

## tbreak

**tbreak** 命令也是添加一个断点，第一个字母“**t**”的意思是 temporarily（临时的），也就是说这个命令加的断点是临时的，所谓临时断点，就是一旦该断点触发一次后就会自动删除。

## watch

**watch** 命令是一个强大的命令，它可以用来监视一个变量或者一段内存，当这个变量或者该内存处的值发生变化时，GDB 就会中断下来。被监视的某个变量或者某个内存地址会产生一个 watch point（观察点）。

## display

**display** 命令监视的变量或者内存地址，每次程序中断下来都会自动输出这些变量或内存的值。例如，假设程序有一些全局变量，每次断点停下来我都希望 GDB 可以自动输出这些变量的最新值，那么使用“**display 变量名**”设置即可。

## 将 print 打印结果显示完整

当使用 print 命令打印一个字符串或者字符数组时，如果该字符串太长，print 命令默认显示不全的，我们可以通过在 GDB 中输入 set print element 0 命令设置一下，这样再次使用 print 命令就能完整地显示该变量的所有字符串了。

## 让被 GDB 调试的程序接收信号

这个程序中，我们接收到 Ctrl + C 信号（对应信号 SIGINT）时会简单打印一行信息，而当用 GDB 调试这个程序时，由于 Ctrl + C 默认会被 GDB 接收到（让调试器中断下来），导致无法模拟程序接收这一信号。解决这个问题有两种方式：

- 在 GDB 中使用 signal 函数手动给程序发送信号，这里就是 signal SIGINT；
- 改变 GDB 信号处理的设置，通过 handle SIGINT nostop print 告诉 GDB 在接收到 SIGINT 时不要停止，并把该信号传递给调试目标程序 。

## 函数明明存在，添加断点时却无效

有时候一个函数明明存在，并且我们的程序也存在调试符号，使用 break functionName 添加断点时 GDB 却提示

```bash
Make breakpoint pending on future shared library load? y/n
```

即使输入 y 命令，添加的断点可能也不会被正确地触发，此时需要改变添加断点的方式，使用该函数所在的代码文件和行号添加断点就能达到效果。

## 多线程下禁止线程切换

GDB 提供了一个在调试时将程序执行流锁定在当前调试线程的命令：set scheduler-locking on。当然也可以关闭这一选项，使用 set scheduler-locking off。

## 条件断点

在实际调试中，我们一般会用到三种断点：普通断点、条件断点和硬件断点。

硬件断点又叫数据断点，这样的断点其实就是前面课程中介绍的用 watch 命令添加的部分断点（为什么是部分而不是全部，前面介绍原因了，watch 添加的断点有部分是通过软中断实现的，不属于硬件断点）。硬件断点的触发时机是监视的内存地址或者变量值发生变化。

普通断点就是除去条件断点和硬件断点以外的断点。

添加条件断点的命令是 `break [lineNo] if [condition]`，其中 lineNo 是程序触发断点后需要停下的位置，condition 是断点触发的条件。这里可以写成 `break 11 if i==5000`，其中，11 就是调用 do_something_fun() 函数所在的行号。当然这里的行号必须是合理行号，如果行号非法或者行号位置不合理也不会触发这个断点。

## 使用 GDB 调试多进程程序

这里说的多进程程序指的是一个进程使用 Linux 系统调用 fork() 函数产生的子进程，没有相互关联的进程就是普通的 GDB 调试，不必刻意讨论。

在实际的应用中，如有这样一类程序，如 Nginx，对于客户端的连接是采用多进程模型，当 Nginx 接受客户端连接后，创建一个新的进程来处理这一路连接上的信息来往，新产生的进程与原进程互为父子关系，那么如何用 GDB 调试这样的父子进程呢？一般有两种方法：

- 用 GDB 先调试父进程，等子进程 fork 出来后，使用 gdb attach 到子进程上去，当然这需要重新开启一个 session 窗口用于调试，gdb attach 的用法在前面已经介绍过了；
- GDB 调试器提供了一个选项叫 follow-fork，可以使用 show follow-fork mode 查看当前值，也可以通过 set follow-fork mode 来设置是当一个进程 fork 出新的子进程时，GDB 是继续调试父进程还是子进程（取值是 child），默认是父进程（ 取值是 parent）。

```bash
(gdb) show follow-fork mode     
Debugger response to a program call of fork or vfork is "parent".
(gdb) set follow-fork child
(gdb) show follow-fork mode
Debugger response to a program call of fork or vfork is "child".
(gdb) 
```
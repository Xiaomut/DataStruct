**转载**

> [C++11多线程-mutex (1)](https://www.jianshu.com/p/96eac2d183b1)
> [C++11多线程-mutex (2)](https://www.jianshu.com/p/8bd389d4ed83)

# mutex

## 概念

​		mutex 又称互斥量，用于提供对共享变量的互斥访问。C++11 中 mutex 相关的类都在 <mutex> 头文件中。共四种互斥类:

| 序号 | 名称                       | 用途                                            |
| :--: | -------------------------- | ----------------------------------------------- |
|  1   | std::mutex                 | 最基本也是最常用的互斥类                        |
|  2   | std::recursive_mutex       | 同一线程内可递归(重入)的互斥类                  |
|  3   | std::timed_mutex           | 除具备mutex功能外，还提供了带时限请求锁定的能力 |
|  4   | std::recursive_timed_mutex | 同一线程内可递归(重入)的timed_mutex             |

​		与 std::thread 一样，mutex相关类不支持拷贝构造、不支持赋值。同时 mutex 类也不支持 move 语义( move 构造、move 赋值)。不用担心会误用这些操作，真要这么做了的话，编译器会阻止你的。

## lock, try_lock, unlock

​		mutex 的标准操作，四个 mutex 类都支持这些操作，但是不同类在行为上有些微的差异。

### lock

​		锁住互斥量。调用 lock 时有三种情况:

1. 如果互斥量没有被锁住，则调用线程将该 mutex 锁住，直到调用线程调用 unlock 释放。
2. 如果 mutex 已被其它线程  lock，则调用线程将被阻塞，直到其它线程unlock 该 mutex。
3. 如果当前 mutex 已经被调用者线程锁住，则 std::mutex 死锁，而recursive 系列则成功返回。

### try_lock

​		尝试锁住 mutex，调用该函数同样也有三种情况：

1. 如果互斥量没有被锁住，则调用线程将该 mutex 锁住(返回 true )，直到调用线程调用 unlock 释放。
2. 如果 mutex 已被其它线程 lock，则调用线程将失败，并返回 false。
3. 如果当前 mutex 已经被调用者线程锁住，则 std::mutex 死锁，而recursive 系列则成功返回 true。

### unlock

​		解锁 mutex，释放对 mutex 的所有权。值得一提的时，对于 recursive 系列mutex，unlock 次数需要与 lock 次数相同才可以完全解锁。

### 例子

```c++
#include <iostream>
#include <thread>
#include <mutex>
using namespace std;

void inc(mutex& mtx, int loop, int& counter) {
  for (int i = 0; i < loop; ++i) {
    // 调用 try_lock, 如果lock 失败会直接返回，造成 ++counter 次数减少一次
    // mtx.try_lock();
    mtx.lock();
    ++counter;
    mtx.unlock();
  }
}

int main() {
  thread ts[5];
  mutex mtx;
  int counter = 0;

  for (thread& thr : ts) {
    thr = thread(inc, ref(mtx), 1000, ref(counter));
  }
  for (thread& thr : ts) {
    thr.join();
  }
  cout << counter << endl;

  return 0;
}
```

## try_lock_for, try_lock_until

​		这两个函数仅用于 timed 系列的 mutex(std::timed_mutex, std::recursive_timed_mutex)，函数最多会等待指定的时间，如果仍未获得锁，则返回 false。除超时设定外，这两个函数与 try_lock 行为一致。

```c++
// 等待指定时长
template <class Rep, class Period>
try_lock_for(const chrono::duration<Rep, Period>& rel_time);
// 等待到指定时间
template <class Clock, class Duration>
try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
```

### 例子

```c++
#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>
using namespace std;

void run(timed_mutex& mtx) {
  auto time = chrono::milliseconds(500);
  if (mtx.try_lock_for(time)) {
    cout << "got lock" << endl;
  } else {
    cout << "don't get lock" << endl;
  }
}

int main() {
  timed_mutex mtx;
  mtx.lock();
  thread thr(run, ref(mtx));
  thr.join();
  mtx.unlock();
  return 0;
}
// output
don't get lock
```

​		C++11 在提供了常规 mutex 的基础上，还提供了一些易用性的类，本节我们将一起看一下这些类。

## lock_guard

​		lock_guard 利用了 C++ RAII 的特性，在构造函数中上锁，析构函数中解锁。lock_guard 是一个模板类，其原型为

```c++
template <class Mutex> class lock_guard
```

​		模板参数 Mutex 代表互斥量，可以是上一篇介绍的 std::mutex, std::timed_mutex, std::recursive_mutex, std::recursive_timed_mutex 中的任何一个，也可以是 std::unique_lock (下面即将介绍)，这些都提供了 lock 和 unlock 的能力。
​		**lock_guard 仅用于上锁、解锁，不对 mutex 承担供任何生周期的管理，因此在使用的时候，请确保 lock_guard 管理的 mutex 一直有效。**
​		同其它 mutex 类一样，locak_guard 不允许拷贝，即拷贝构造和赋值函数被声明为 delete。

```c++
lock_guard(lock_guard const&) = delete;
lock_guard& operator=(lock_guard const&) = delete;
```

​		lock_guard 的设计保证了即使程序在锁定期间发生了异常，也会安全的释放锁，不会发生死锁。

```c++
#include <iostream>
#include <mutex>

std::mutex mtx;

void safe_thread() {
  try {
    // guard 离开作用域，析构时自动释放锁
    std::lock_guard<std::mutex> guard(mtx);
    throw std::logic_error("logic error");
  } catch (std::exception &ex) {
    std::cerr << "[caught] " << ex.what() << std::endl;
  }
}

int main() {
  safe_thread();
  // 此处仍能上锁
  mtx.lock();
  std::cout << "got lock" << std::endl;
  mtx.unlock();
  return 0;
}
```

## unique_lock

​		lock_guard 提供了简单上锁、解锁操作，但当我们需要更灵活的操作时便无能为力了。这些就需要 unique_lock 上场了。unique_lock 拥有对 Mutex 的**所有权**，一但初始化了 unique_lock，其就接管了该 mutex, 在 unique_lock 结束生命周期前(析构前)，其它地方就不要再直接使用该 mutex了。unique_lock 提供的功能较多，此处不一一列举。

## std::call_once

​		该函数的作用顾名思义：保证 call_once 调用的函数只被执行一次。该函数需要与 std::once_flag 配合使用。std::once_flag 被设计为对外封闭的，即外部没有任何渠道可以改变 once_flag 的值，仅可以通过 std::call_once 函数修改。一般情况下我们在自己实现 call_once 效果时，往往使用一个全局变量，以及双重检查锁(DCL)来实现，即便这样该实现仍然会有很多坑(多核环境下)。有兴趣的读者可以搜索一下 DCL 来看，此处不再赘述。
​		C++11为我们提供了简便的解决方案，所需做的仅仅像下面这样使用即可。

```c++
#include <iostream>
#include <thread>
#include <mutex>

void initialize() { std::cout << __FUNCTION__ << std::endl; }

std::once_flag of;

void func() {
  std::cout << "begin" << std::endl;
  std::call_once(of, initialize);
  std::cout << "end" << std::endl;
}

int main() {
  std::thread thr[3];
  for (std::thread& t : thr) {
    t = std::thread(func);
  }
  for (std::thread& t : thr) {
    t.join();
  }
  return 0;
}
// output
begin
initialize  // func just run once
end
begin
end
begin
end
```

## std::try_lock

​		当有多个 mutex 需要执行 try_lock 时，该函数提供了简便的操作。try_lock 会按参数从左到右的顺序，对 mutex **顺次执行** try_lock 操作。当其中某个mutex.try_lock 失败(返回 false 或抛出异常)时，已成功锁定的 mutex 都将被解锁。需要注意的是，**该函数成功时返回 -1**， 否则返回失败 mutex 的索引，索引从 0 开始计数。

```c++
template <class L1, class L2, class... L3>
int try_lock(L1&, L2&, L3&...);
```

## std::lock

​		std::lock 是较智能的上批量上锁方式，采用死锁算法来锁定给定的 mutex 列表，避免死锁。该函数对 mutex 列表的上锁顺序是不确定的。该函数保证: 如果成功，则所有 mutex 全部上锁，如果失败，则全部解锁。

```c++
template <class L1, class L2, class... L3>
void lock(L1&, L2&, L3&...);
```


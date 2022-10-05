**转载**

> [C++11多线程-条件变量(std::condition_variable)](https://www.jianshu.com/p/a31d4fb5594f)

## 简介

​		前面我们介绍了线程( std::thread )和互斥量( std::mutex )，互斥量是多线程间同时访问某一共享变量时，保证变量可被安全访问的手段。在多线程编程中，还有另一种十分常见的行为：线程同步。线程同步是指线程间需要按照预定的先后次序顺序进行的行为。C++11 对这种行为也提供了有力的支持，这就是条件变量。条件变量位于头文件 condition_variable下。本章我们将简要介绍一下该类，在文章的最后我们会综合运用 std::mutex 和 std::condition_variable，实现一个 chan 类，该类可在多线程间安全的通信，具有广泛的应用场景。

## std::condition_variable

​		条件变量提供了两类操作：wait和notify。这两类操作构成了多线程同步的基础。

### wait

​		wait 是线程的等待动作，直到其它线程将其唤醒后，才会继续往下执行。下面通过伪代码来说明其用法：

```c++
std::mutex mutex;
std::condition_variable cv;
// 条件变量与临界区有关，用来获取和释放一个锁，因此通常会和mutex联用。
std::unique_lock lock(mutex);
// 此处会释放lock，然后在cv上等待，直到其它线程通过cv.notify_xxx来唤醒当前线程，cv被唤醒后会再次对lock进行上锁，然后wait函数才会返回。
// wait返回后可以安全的使用mutex保护的临界区内的数据。此时mutex仍为上锁状态
cv.wait(lock)
```

​		需要注意的一点是, wait 有时会在没有任何线程调用 notify 的情况下返回，这种情况就是有名的 [**spurious wakeup**](https://docs.microsoft.com/zh-cn/windows/desktop/api/synchapi/nf-synchapi-sleepconditionvariablecs)。因此当wait返回时，你需要再次检查 wait 的前置条件是否满足，如果不满足则需要再次 wait。wait 提供了重载的版本，用于提供前置检查。

```c++
template <typename Predicate>
void wait(unique_lock<mutex> &lock, Predicate pred) {
    while(!pred()) {
        wait(lock);
    }
}
```

​		除 wait 外, 条件变量还提供了 wait_for 和 wait_until，这两个名称是不是看着有点儿眼熟，std::mutex 也提供了 `_for` 和 `_until` 操作。在 C++11 多线程编程中，需要等待一段时间的操作，一般情况下都会有 xxx_for 和 xxx_until 版本。前者用于等待指定时长，后者用于等待到指定的时间。

## notify

了解了 wait，notify 就简单多了：唤醒 wait 在该条件变量上的线程。notify 有两个版本：notify_one 和 notify_all。

- notify_one 唤醒等待的一个线程，注意只唤醒一个。
- notify_all 唤醒所有等待的线程。使用该函数时应避免出现[惊群效应](https://blog.csdn.net/lyztyycode/article/details/78648798?locationNum=6&fps=1)。

其使用方式见下例：

```c++
std::mutex mutex;
std::condition_variable cv;

std::unique_lock lock(mutex);
// 所有等待在cv变量上的线程都会被唤醒。但直到lock释放了mutex，被唤醒的线程才会从wait返回。
cv.notify_all(lock)
```


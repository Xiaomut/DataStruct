# struct 中空数组的使用

看 Redis `intset` 的源码的时候发现 `intset` 的定义如下。

```c
typedef struct intset {
    uint32_t encoding;
    uint32_t length;
    int8_t contents[];
} intset
```

 `contents` 数组的作用是保存实际的 `intset` 元素，比较有趣的是 `contents` 数组在 `intset` 初始化的时候是空的，也就是说不占用存储空间，可以通过如下代码来验证.

```c
#include <stdint.h>
#include <stdio.h>

int main() {
    typedef struct intset {
        uint32_t encoding;
        uint32_t length;
        int8_t contents[];
    } intset;

    printf("%lu\n", sizeof(intset));  // 8
}
```

在 Redis 里面，`contents` 用来建立动态数组，这是一种比较常用的用法。

> 结构体末尾的空数组是个广泛使用的常见技巧，常用来构成缓冲区。比起指针，用空数组有这样的优势：
>  1.不需要初始化，数组名直接就是所在的偏移
>  2.不占任何空间，指针需要占用int长度空间，空数组不占任何空间。
>
>  “这个数组不占用任何内存”，意味着这样的结构节省空间；“该数组的内存地址就和他后面的元素的地址相同”，意味着无需初始化，数组名就是后面元素的地址，直接就能当做指针使用。
>
>  这样的写法最适合制作动态buffer。因为可以这样分配空间：
>  malloc（sizeof(struct XXX）＋ buff_len）；
>  看出来好处没有？直接就把buffer的结构体和缓冲区一块分配了。用起来也非常方便，因为现在空数组其实变成了buff_len长度的数组了。
>  这样的好处是：
>  一次分配解决问题，省了不少麻烦。大家知道为了防止内存泄漏，如果是分两次分配（结构体和缓冲区），那么要是第二次malloc失败了，必须回滚释放第一 个分配的结构体。这样带来了编码麻烦。其次，分配了第二个缓冲区以后，如果结构里面用的是指针，还要为这个指针赋值。同样，在free这个buffer的 时候，用指针也要两次free。如果用空数组，所有问题一次解决。
>
>  其次，大家知道小内存的管理是非常困难的，如果用指针，这个buffer的struct部分就是小内存了，在系统内存在多了势必严重影响内存管理的性能。要是用空数组把struct和实际数据缓冲区一次分配大块问题，就没有这个问题。
>
>  如此看来，用空数组既简化编码，又解决了小内存碎片问题提高了性能，何乐不为？应该广泛采用。
>
> [来源](http://blog.chinaunix.net/uid-9718353-id-1998040.html)
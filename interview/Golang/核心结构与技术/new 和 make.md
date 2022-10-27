

    - 切片、映射和通道，使用 make()
    - 数组、结构体和所有的值类型，使用 new()



##  map 和 struct vs new() 和 make()

`new()` 和 `make()` 这两个内置函数已经在第 [7.2.4](07.2.md) 节通过切片的例子说明过一次。

现在为止我们已经见到了可以使用 `make()` 的三种类型中的其中两个：

    slices  /  maps / channels（见第 14 章）

下面的例子说明了在映射上使用 `new()` 和 `make()` 的区别以及可能发生的错误：

示例 10.4 [new_make.go](examples/chapter_10/new_make.go)（不能编译）

```go
package main

type Foo map[string]string
type Bar struct {
    thingOne string
    thingTwo int
}

func main() {
    // OK
    y := new(Bar)
    (*y).thingOne = "hello"
    (*y).thingTwo = 1

    // NOT OK
    z := make(Bar) // 编译错误：cannot make type Bar
    (*z).thingOne = "hello"
    (*z).thingTwo = 1

    // OK
    x := make(Foo)
    x["x"] = "goodbye"
    x["y"] = "world"

    // NOT OK
    u := new(Foo)
    (*u)["x"] = "goodbye" // 运行时错误!! panic: assignment to entry in nil map
    (*u)["y"] = "world"
}
```

试图 `make()` 一个结构体变量，会引发一个编译错误，这还不是太糟糕，但是 `new()` 一个 `map` 并试图向其填充数据，将会引发运行时错误！ 因为 `new(Foo)` 返回的是一个指向 `nil` 的指针，它尚未被分配内存。所以在使用 `map` 时要特别谨慎。

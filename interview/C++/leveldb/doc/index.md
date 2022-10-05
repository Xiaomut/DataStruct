# leveldb

_Jeff Dean, Sanjay Ghemawat_

leveldb库提供持久键值存储。 键和值是任意字节数组。 键根据用户指定的排序函数进行排序。

## 打开数据库 Opening A Database

leveldb数据库具有与文件系统目录对应的名称。 数据库的所有内容都存储在此目录中。 以下示例显示如何打开数据库，并在必要时创建它：

```cpp
#include <cassert>
#include "leveldb/db.h"

leveldb::DB* db;
leveldb::Options options;
options.create_if_missing = true;
leveldb::Status status = leveldb::DB::Open(options, "/tmp/testdb", &db);
assert(status.ok());
```

如果要在数据库已存在时引发错误，请在`leveldb :: DB :: Open`调用之前添加以下代码：

```cpp
options.error_if_exists = true;
```

## 状态 Status

您可能已经注意到上面的`leveldb :: Status`类型。 leveldb中的大多数函数都会返回此类型的值，这些函数可能会遇到错误。 您可以检查这样的结果是否正常，还可以打印相关的错误消息：

```cpp
leveldb::Status s = ...;
if (!s.ok()) cerr << s.ToString() << endl;
```

## 关闭数据库 Closing A Database

使用完数据库之后，只需删除数据库对象。例子:

```cpp
... open the db as described above ...
... do something with db ...
delete db;
```

## 读写操作 Reads And Writes

数据库提供Put，Delete和Get方法来修改/查询数据库。 例如，以下代码将存储在key1下的值移动到key2。

```cpp
std::string value;
leveldb::Status s = db->Get(leveldb::ReadOptions(), key1, &value);
if (s.ok()) s = db->Put(leveldb::WriteOptions(), key2, value);
if (s.ok()) s = db->Delete(leveldb::WriteOptions(), key1);
```

## 原子更新 Atomic Updates

请注意，如果进程在设置置key2之后，删除key1之间死亡，则会在多个键（key1,key2）下保留相同的值。 使用`WriteBatch`类原子地进行一组更新可以避免这些问题：

```cpp
#include "leveldb/write_batch.h"
...
std::string value;
leveldb::Status s = db->Get(leveldb::ReadOptions(), key1, &value);
if (s.ok()) {
  leveldb::WriteBatch batch;
  batch.Delete(key1);
  batch.Put(key2, value);
  s = db->Write(leveldb::WriteOptions(), &batch);
}
```

`WriteBatch`包含对数据库进行的一系列编辑，批处理中的这些编辑将按顺序进行操作。 请注意，我们在Put之前调用Delete，这样如果key1与key2相同，我们最终也不会错误地删除该值（即删除了key1, 也没有成功地将值写入key2）。

除了原子性优势之外，`WriteBatch`还可以通过将大量单个操作放入同一批来加速批量更新。

## 同步写入 Synchronous Writes

默认情况下，每次写入leveldb都是异步的：它在进程将数据写入写入操作系统（内核）后返回。 从操作系统内存到底层持久存储的转移是异步发生的。 可以为特定写入打开sync标志，使得在正在写入的数据直到真正写入到可持久化存储器后才返回。 （在Posix系统上，这是通过在写操作返回之前调用`fsync(...)`或`fdatasync(...)`或`msync(...，MS_SYNC)`来实现的。）

```c++
leveldb::WriteOptions write_options;
write_options.sync = true;
db->Put(write_options, ...);
```

异步写入通常比同步写入快一千倍。 异步写入的缺点是机器崩溃可能导致最后几次更新丢失。 请注意，仅写入过程（即，不是重新启动）的崩溃不会导致任何损失，因为即使同步失败，也会在更新完成之前将更新从进程内存推送到操作系统（内核）中。

通常可以安全地使用异步写入。 例如，在将大量数据加载到数据库中时，您可以通过在崩溃后重新启动批量加载来处理丢失的更新。 当每次单独写入都是同步的情况下，同步与异步的混合方案也是可行的，并且在发生崩溃的情况下，通过在上一次运行完成最后一次同步写入之后的位置重新启动批量加载来防止更新的丢失。 （同步写入可以更新描述崩溃时重新启动位置的标记。）

`WriteBatch`提供了异步写入的替代方法。 可以在同一WriteBatch中放置多个更新，并使用同步一次写入（即，`write_options.sync`设置为true）。 同步写入的额外成本将分摊到批处理中的所有写入。

## 并发 Concurrency

一个数据库在同一时间内只能由一个进程打开。 leveldb从操作系统获取锁来防止竞争（misuse）。 在单个进程中，多个并发线程可以安全地共享相同的`leveldb :: DB`对象。 即，不同的线程可以在没有任何外部同步的情况下写入或获取迭代器或在同一数据库上调用Get（leveldb实现将自动执行所需的同步）。 但是，其他对象（如Iterator和`WriteBatch`）可能需要外部同步。 如果两个线程共享这样的对象，则它们必须使用自己的锁定协议来保护对它的访问。 公共头文件中提供了更多详细信息。

## 迭代器 Iteration

以下示例演示如何打印一个数据库中的所有键值对。

```c++
leveldb::Iterator* it = db->NewIterator(leveldb::ReadOptions());
for (it->SeekToFirst(); it->Valid(); it->Next()) {
  cout << it->key().ToString() << ": "  << it->value().ToString() << endl;
}
assert(it->status().ok());  // Check for any errors found during the scan
delete it;
```

以下代码显示了如何仅处理[start，limit]范围内的键：

```c++
for (it->Seek(start);
   it->Valid() && it->key().ToString() < limit;
   it->Next()) {
  ...
}
```

您还可以按相反顺序处理条目。（警告：反向迭代可能比前向迭代慢一些。）

```c++
for (it->SeekToLast(); it->Valid(); it->Prev()) {
  ...
}
```

## 快照 Snapshots

快照在键值存储的整个状态上提供一致的只读视图。 `ReadOptions :: snapshot`可能是非NULL，表示读取应该在特定版本的DB状态上运行。 如果`ReadOptions :: snapshot`为NULL，则读操作将对当前状态的隐式(implicit)快照进行操作。

快照通过`DB::GetSnapshot()`方法创建：

```c++
leveldb::ReadOptions options;
options.snapshot = db->GetSnapshot();
... apply some updates to db ...
leveldb::Iterator* iter = db->NewIterator(options);
... read using iter to view the state when the snapshot was created ...
delete iter;
db->ReleaseSnapshot(options.snapshot);
```

请注意，当不再需要快照时，应使用`DB :: ReleaseSnapshot`接口释放快照。 这允许实现摆脱为了支持对该快照读而需要维护的状态。(This allows the implementation to get rid of state that was being maintained just to support reading as of that snapshot.)

## 切片 Slice

上面的`it-> key（）`和`it-> value（）`调用的返回值是`leveldb :: Slice`类型的实例。 Slice是一个简单的结构，包含一个长度和一个指向外部字节数组的指针。 返回Slice是比返回`std :: string`的更好(cheaper)的替代方法，因为我们不需要复制可能存在的占空间更大的键和值。 此外，leveldb方法不返回以null结尾的C样式字符串，因为leveldb键和值允许包含“'\ 0”字节。

C ++字符串和以null结尾的C风格字符串可以很容易地转换为Slice：

```c++
leveldb::Slice s1 = "hello";

std::string str("world");
leveldb::Slice s2 = str;
```

Slice可以很容易地转换回C ++字符串：

```c++
std::string str = s1.ToString();
assert(str == std::string("hello"));
```

使用Slices时要小心，因为调用者需要确保在使用Slice时Slice指针所指向的内容在外部作用域仍然存活。 例如，以下做法就存在bug：

```c++
leveldb::Slice slice;
if (...) {
  std::string str = ...;
  slice = str;
}
Use(slice);
```

当if语句超出范围时，str将被销毁，并且slice的后备存储(backing storage)将消失。

## 比较器 Comparators

前面的示例使用key的默认排序函数，它按字典顺序排序字节。 但是，您可以在打开数据库时提供自定义比较器。 例如，假设每个数据库密钥由两个数字组成，我们应该按第一个数字排序，用第二个数字打破联系。 首先，定义表达这些规则的`leveldb :: Comparator`的适当子类：

```c++
class TwoPartComparator : public leveldb::Comparator {
 public:
  // Three-way comparison function:
  //   if a < b: negative result
  //   if a > b: positive result
  //   else: zero result
  int Compare(const leveldb::Slice& a, const leveldb::Slice& b) const {
    int a1, a2, b1, b2;
    ParseKey(a, &a1, &a2);
    ParseKey(b, &b1, &b2);
    if (a1 < b1) return -1;
    if (a1 > b1) return +1;
    if (a2 < b2) return -1;
    if (a2 > b2) return +1;
    return 0;
  }

  // Ignore the following methods for now:
  const char* Name() const { return "TwoPartComparator"; }
  void FindShortestSeparator(std::string*, const leveldb::Slice&) const {}
  void FindShortSuccessor(std::string*) const {}
};
```

现在使用此自定义比较器创建数据库：

```c++
TwoPartComparator cmp;
leveldb::DB* db;
leveldb::Options options;
options.create_if_missing = true;
options.comparator = &cmp;
leveldb::Status status = leveldb::DB::Open(options, "/tmp/testdb", &db);
```

## 向后兼容性 Backwards compatibility

比较器的Name方法的返回值在创建数据库时附加到其上，并在每个后续数据库打开时进行检查。 如果名称改变，`leveldb :: DB :: Open`调用将失败。 因此，当且仅当新key格式和比较功能与现有数据库不兼容时，才更改名称，并且可以删除所有现有数据库的内容。

但是，您可以通过一些预先规划逐步演变您的key格式。 例如，您可以在每个键的末尾存储版本号（一个字节应该足以满足大多数用途）。 当您希望切换到新的key格式（例如，将可选的第三部分添加到由`TwoPartComparator`处理的key）时，（a）保持相同的比较器名称（b）提高新key的版本号（c）更改比较器功能，并使用键中的版本号来决定如何解释它们。

## 性能 Performance

可以通过更改`include / options.h`中定义的类型的默认值来调整性能。

## （数据）块大小 Block size

leveldb将相邻的密钥组合在一起成为同一个块，这样的块是进出永久存储器的单元。 默认块大小约为4096个未压缩字节。 主要功能是对数据库内容进行批量扫描的应用程序可能希望增加此大小。对小数据进行大量点读取(point reads)的应用可能希望切换到较小的块大小。 使用小于1千字节或大于几兆字节的块没有太大好处。 另请注意，块大小较大时压缩效果更好。

## 压缩 Compression

每个块在写入持久存储之前都是单独压缩的。 默认情况下压缩处于启用状态，因为默认压缩方法非常快，并且对于不可压缩数据会自动禁用压缩方法。 在极少数情况下，应用程序可能希望完全禁用压缩，但只有在基准测试显示有性能改进时才应该这样做：

```c++
leveldb::Options options;
options.compression = leveldb::kNoCompression;
... leveldb::DB::Open(options, name, ...) ....
```

## 缓存 Cache

数据库的内容存储在文件系统中的一组文件中，每个文件存储一系列压缩块。 如果options.block_cache为非NULL，则它用于缓存常用的未压缩块内容。

```c++
#include "leveldb/cache.h"

leveldb::Options options;
options.block_cache = leveldb::NewLRUCache(100 * 1048576);  // 100MB cache
leveldb::DB* db;
leveldb::DB::Open(options, name, &db);
... use the db ...
delete db
delete options.block_cache;
```

请注意，缓存用于保存未压缩的数据，因此应根据应用程序级别的数据大小进行调整，而不应通过减少用于压缩块的缓存来增大此缓存。 （压缩块的缓存留给操作系统缓冲区缓存，或客户端提供的任何自定义Env实现。）

执行批量读取时，应用程序可能希望禁用缓存，以便批量读取处理的数据不会最终取代大多数缓存的内容。 per-iterator选项可用于实现此目的：

```c++
leveldb::ReadOptions options;
options.fill_cache = false;
leveldb::Iterator* it = db->NewIterator(options);
for (it->SeekToFirst(); it->Valid(); it->Next()) {
  ...
}
```

## 键(的内存)布局 Key Layout

请注意，磁盘传输和缓存的单位是一个块。 相邻的键（根据数据库排序规则排序）通常放在同一个块中。 因此，应用程序可以通过将一起访问的键放在彼此附近并将不常使用的键放置在键空间的单独区域中来提高其性能。

例如，假设我们在leveldb之上实现了一个简单的文件系统。 我们可能希望存储的条目类型是：

​    filename -> permission-bits, length, list of file_block_ids

​    file_block_id -> data

我们可能希望使用一个字母（例如'/'）和带有不同字母（例如'0'）的`file_block_id`键作为文件名键的前缀，这样只扫描元数据就不会强制我们获取和缓存庞大的文件内容。

## 过滤器 Filters

由于leveldb数据在磁盘上的组织方式，单个`Get（）`调用可能涉及从磁盘进行多次读取。 可选的FilterPolicy机制可用于大幅减少磁盘读取次数。

```c++
leveldb::Options options;
options.filter_policy = NewBloomFilterPolicy(10);
leveldb::DB* db;
leveldb::DB::Open(options, "/tmp/testdb", &db);
... use the database ...
delete db;
delete options.filter_policy;
```

上述代码将基于Bloom过滤器的过滤策略与数据库相关联。 基于Bloom过滤器的过滤依赖于每个键在内存中保留一些数据位（在上面这种情况下，每个键10位，因为这是我们传递给`NewBloomFilterPolicy`的参数）。 此过滤器将Get（）调用所需的不必要磁盘读取次数减少约100倍。增加每个键的位数可以实现更低的内存开销。 我们建议工作集大于内存容量且执行大量随机读取的应用程序设置过滤策略。

如果您使用自定义比较器，则应确保您使用的过滤器与比较器兼容。 例如，考虑比较键时忽略尾随空格的比较器。 `NewBloomFilterPolicy`不能与这样的比较器一起使用。 相反，应用程序应提供自定义过滤器策略，该策略也会忽略尾随空格。 例如：

```c++
class CustomFilterPolicy : public leveldb::FilterPolicy {
 private:
  FilterPolicy* builtin_policy_;

 public:
  CustomFilterPolicy() : builtin_policy_(NewBloomFilterPolicy(10)) {}
  ~CustomFilterPolicy() { delete builtin_policy_; }

  const char* Name() const { return "IgnoreTrailingSpacesFilter"; }

  void CreateFilter(const Slice* keys, int n, std::string* dst) const {
    // Use builtin bloom filter code after removing trailing spaces
    std::vector<Slice> trimmed(n);
    for (int i = 0; i < n; i++) {
      trimmed[i] = RemoveTrailingSpaces(keys[i]);
    }
    return builtin_policy_->CreateFilter(&trimmed[i], n, dst);
  }
};
```

高级应用程序可能会提供过滤器策略，该策略不使用布隆过滤器，而是使用其他一些机制来汇总一组键。 有关详细信息，请参阅`leveldb / filter_policy.h`。

## 校验和 Checksums

leveldb将校验和与它存储在文件系统中的所有数据相关联。 对于验证这些校验和的积极程度(aggressively)，提供了两个单独的控件：

`ReadOptions :: verify_checksums`可以设置为true以强制校验和验证代表特定读取从文件系统读取的所有数据。 默认情况下，不会执行此类验证。

在打开数据库之前，可以将`Options :: paranoid_checks`设置为true，以使数据库实现在检测到内部数据出错时立即引发错误。 根据数据库的哪个部分已损坏，可能会在打开数据库时引发错误，或者稍后由另一个数据库操作引发错误。 默认情况下，paranoid checking已关闭，因此即使其持久存储的某些部分已损坏，也可以使用该数据库。

如果数据库已损坏（可能在开启paranoid checking时无法打开），则可以使用`leveldb :: RepairDB`函数尽可能多地恢复数据

## 获取近似大小 Approximate Sizes

`GetApproximateSizes`方法可用于获取一个或多个键范围使用的文件系统空间的近似字节数。

```c++
leveldb::Range ranges[2];
ranges[0] = leveldb::Range("a", "c");
ranges[1] = leveldb::Range("x", "z");
uint64_t sizes[2];
leveldb::Status s = db->GetApproximateSizes(ranges, 2, sizes);
```

前面的调用将`sizes [0]`设置为键范围`[a..c)`，并且`sizes [1]`保存使用的文件系统空间的近似字节数，使用的是大概的字节数。 键范围`[x..z）`。

## 环境 Environment

leveldb实现执行的所有文件操作（和其他操作系统调用）都通过`leveldb :: Env`对象进行路由。 需求更复杂的客户可能希望提供他们自己的Env实现以获得更好的控制。 例如，应用程序可能会在文件IO路径中引入人为延迟，以限制leveldb对系统中其他活动的影响。

```c++
class SlowEnv : public leveldb::Env {
  ... implementation of the Env interface ...
};

SlowEnv env;
leveldb::Options options;
options.env = &env;
Status s = leveldb::DB::Open(options, ...);
```

## 移植 Porting

通过提供由`leveldb / port / port.h`导出的类型/方法/函数的平台特定实现，可以将leveldb移植到新平台。 有关详细信息，请参阅`leveldb / port / port_example.h`。

## 其他信息 Other Information

有关leveldb实现的详细信息，请参阅以下文档：

1. Implementation notes (impl.md)

2. Format of an immutable Table file (table_format.md)

3. Format of a log file (log_format.md)
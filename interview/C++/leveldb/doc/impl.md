## 文件 Files

leveldb的实现类似于single[Bigtable tablet (section 5.3)](http://research.google.com/archive/bigtable.html).

但是，组成表示(representation)的文件的组织方式有些不同，下面将对此进行说明。

每个数据库由存储在目录中的一组文件表示。 有几种不同类型的文件，如下所述：

### 日志文件 Log files

日志文件（* .log）存储一系列最新更新。 每个更新都附加到当前日志文件。 当日志文件达到预定大小（默认情况下大约为4MB）时，会将其转换为已排序的表（参阅下文），并创建新的日志文件以供记录将来的更新。

当前日志文件的副本保存在内存中（`memtable`）。 每次读取时都会查阅此副本，以便读取操作反映(reflect)所有已记录的更新。

## 排序表 Sorted tables

排序表（* .ldb）存储按键排序的条目序列。 每个条目都是键的值，或键的删除标记。 （保留删除标记以隐藏旧排序表中存在的过期值）。

所有的排序表被分为成一系列级别。 从日志文件生成的排序表放在一个特殊的**young**级别（也称为level-0）。 当level-0文件的数量超过某个阈值（当前为四个）时，所有level-0文件将与level-1级文件合并，以生成一系列新的level-1文件（每到达2MB数据就创建一个新的level-1文件）

level-0级别的文件可能包含重叠键。 但是，其他级别的文件具有不同的非重叠键范围。 考虑级别L，其中L> = 1。当level-L中的文件的大小超过（10 ^ L）MB（即，级别-1为10MB，级别2为100MB，...）时， 此文件会和level-(L + 1)中的所有重叠文件合并以形成一组新的level-(L + 1)文件。 这些合并仅使用批量读取和写入（最小化开销）将新更新从level-0逐渐迁移到最大级别。

### Manifest文件

MANIFEST文件列出组成每个级别的排序表集，相应的键范围和其他重要元数据。 每当重新打开数据库时，都会创建一个新的MANIFEST文件（文件名中嵌入一个新编号）。 MANIFEST文件被格式化为日志，并且会将对服务状态所做的更改（添加或删除文件）记录到此日志中。

### Current文件

CURRENT是一个简单的文本文件，其中包含最新的MANIFEST文件的名称。

### Info logs

信息性消息将打印到名为LOG和LOG.old的文件中。

### Others

用于其他目的的其他文件也可能存在（LOCK，* .dbtmp）。

## Level 0

当日志文件增长到特定大小（默认为4MB）时：创建一个全新的memtable和日志文件，并在此文件中记录将来的更新。

在后台：

1. 将先前的memtable的内容写入sstable。
2. 丢弃memtable。
3. 删除旧的日志文件和旧的memtable。
4. 将新的sstable添加到level-0。

## 压缩 Compactions

当level-L的大小超过其限制时，我们在后台线程中压缩它。 压缩过程从level-L中选择文件，从level-(L+1)中选择所有重叠文件。 请注意，如果level-L文件仅与level-(L + 1)文件的一部分重叠，则level-(L + 1)的整个文件也会被压缩，并在压缩后被丢弃。 除此之外：因为level-0是特殊的（其中的文件可能相互重叠），我们特别处理从level-0到level-1的压缩：level-0的压缩可能会选择多个level-0文件，以防其中一些 文件相互重叠。

压缩合并会生成一系列level-(L + 1)文件。 在当前输出文件达到目标文件大小（2MB）后，我们就会生成新的level-(L + 1)文件。 当当前输出文件的键范围增长到足以超过十个level(L + 2)文件时，也将进行压缩。 最后一条规则确保稍后压缩level(L + 1)文件不会与level(L + 2)文件产生太多的键重叠。

旧文件将被丢弃，新文件将添加到服务状态(serving state)。

特定级别的压缩在key空间中循环。 更详细地说，对于每个level-L，我们记住level-L处的最后一次压缩的结束键。level-L的下一次压缩将选择在该键之后开始的第一个文件（如果不存在则回到key空间的开头）。

压缩后会删除被覆盖的值。 如果没有更高编号的级别包含范围与当前键重叠的文件，它们也会丢弃删除标记。

### 定时 Timing

Level-0压缩将从0级读取最多4个1MB文件，最坏情况下会读取所有level-1文件（10MB）。 即我们将读取14MB并写入14MB。

除了特殊的level-0压缩之外，其他压缩情况下将从level-L中选择一个2MB文件。在最坏的情况下，这将与level(L + 1)重叠大约12个文件（10个因为level-(L + 1)通常为level-L的10倍大小，另外两个在边界处，因为level-L的文件范围通常不会与level-(L + 1)的文件范围对齐。 因此，压缩将读取26MB并写入26MB。 假设磁盘IO速率为100MB / s（现代驱动器的球场范围），最坏情况下的压缩成本约为0.5秒。

如果我们在后台进行慢速写入，比如只用说100MB/ s速度的10％，那么压缩可能需要5秒钟。 如果用户以10MB / s的速度写入，我们可能会构建大量的level-0文件（约50个文件以保存5 * 10MB）。 由于在每次读取时都需要将更多文件合并在一起，这可能显着增加读取的成本。

解决方案1：为了减少此问题，我们可能希望在level-0的文件数量较大时增加日志切换阈值。 虽然缺点是这个阈值越大，我们需要更多的内存来保存相应的memtable。

解决方案2：当level-0文件的数量增加时，我们人为地降低写入速率。

解决方案3：降低合并成本。 也许大多数level-0文件的块都会在缓存中保持未压缩状态，我们只需要担心合并迭代器中的O（N）复杂性。

### 文件数量 Number of files

我们可以将单文件的大小设置地更大以减少总文件数，而不是总是设置为2MB，但代价是更多的突发性压缩。 或者，我们可以将文件集分成多个目录。

在2011年2月4日对ext3文件系统进行的实验显示，在具有不同文件数的目录中打开100K文件的时间如下：

| Files in directory | Microseconds to open a file |
| ------------------ | --------------------------- |
|               1000 |                           9 |
|              10000 |                          10 |
|             100000 |                          16 |

那么或许在现代文件系统上的分片不是必需的？

## 复原(解压缩)  Recovery

*检查CURRENT以查找最新提交的MANIFEST的名称
*检查指定的MANIFEST文件
*清理过时的文件
*我们可以在这里打开所有sstables，但使用惰性加载可能更好......
*将日志块转换为新的level-0 sstable
*开始使用恢复的序列将新写入指向新的日志文件＃

## 垃圾收集文件 Garbage collection of files

`DeleteObsoleteFiles（）`在每次压缩结束时和恢复结束时被调用。 它找到数据库中所有文件的名称。 它删除所有不是当前日志文件的日志文件。 它删除所有未从某个级别引用并且不是活动压缩的输出的表文件。


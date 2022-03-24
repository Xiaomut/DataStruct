# 

## 1. 底层原理

### 1.1 MySQL Server 架构

<div align="center" width="80%"><img src="./assets/MySQL Server.png"></div>

自顶向下大致可以分为`网络连接层，服务层，存储引擎层，系统文件层`

- 网络连接层
    - 客户端连接器
- 服务层
    - 连接池 (Connection Pool)
    - 系统管理和控制工具 (Management Service & Utilities)
    - SQL接口 (SQL Interface)
    - 解析器 (Parser)
    - 查询优化器 (Optimizer)
        - <font color="red">选择 -> 投影 -> 连接 策略</font>
        ```sql
        select uid, name from user where gender=1;
        ```
    - 缓存 (Cache & Buffer)
        - 缓存机制是由一系列小缓存组成的。可以直接从缓存中取数据
- 存储引擎层
    - `作用: `负责数据的存储与提取，与底层系统文件进行交互。
- 系统文件层
    - `作用: `存储数据和日志，完成与存储引擎的交互
    - 日志文件
        - 错误日志 (Error log)
            - 默认开启
            ```sql
            show VARIABLES like "%log_err%";
            ```
        - 通用查询日志 (General query log)
            - 记录一般查询语句
            ```sql
            show VARIABLES like "%general%";
            ```
        - 二进制日志 (binary log)
            - 记录对MySQL数据库执行的更改操作，并且记录了语句的发生时间、执行时长；但是不记录select、show等不修改数据库的SQL。主要用于数据库恢复和主从复制
            ```sql
            show VARIABLES like "%log_bin%";  
            show VARIABLES like "%binlog%";  
            show binary logs;
            ```
        - 慢查询日志 (Slow query log)
            - 记录所有执行时间超时的查询SQL，默认是10s
            ```sql
            show VARIABLES like "%slow_query%";
            show VARIABLES like "%long_query_time%";
            ```
    - 配置文件
        - `作用: `用于存放MySQL所有的配置信息文件，如 `my.cnf`, `my.ini` 等
    - 数据文件
        - `db.opt: `记录这个库的默认使用的字符集和校验规则
        - `frm: `存储与表相关的元数据(meta)信息，包括表结构的定义信息等，每一张表都会有一个frm文件
        - `MYD: `MyISAM存储引擎专用，存放MyISAM表的数据，没一张表都会有一个MYD文件
        - `MYI: `MyISAM存储引擎专用，存放MyISAM表的索引相关信息，每一张MyISAM表对应一个MYI文件
        - `ibd`和`IBDATA: `存放 `InnoDB` 的数据文件（包括索引）。`InnoDB` 存储引擎有两种表空间方式: 独享表空间和共享表空间。独享表空间用 `.ibd` 来存放，共享表空间用 `.ibdata`，所有表共同使用一个（或多个，自行配置）`.ibdata` 文件
        ```sql
        show VARIABLES like "%datadir%";
        ```


### 1.2 SQL 运行机制

- 建立连接 (Connectors&Connection Pool)，通过客户端/服务器通信协议与MySQL建立连接。通信方式是 "半双工"。对于每一个MySQL的连接，时刻都有一个线程状态来标识这个连接在做什么。
    - 通讯机制
        - 全双工: 能同时发送和接收数据
        - 半双工: 指在某一时刻，只能接收或发送数据，不能同时
        - 单工: 只能发送或接收数据
    - 线程状态 `show processlist`
- 查询缓存 (Cache&Buffer) 
    ```sql
    show VARIABLES like "%query_cache%"; 
    show VARIABLES like "%Qcache%";
    ```
    - MySQL的一个可查询优化的地方，如果开启且在查询缓存过程中查询到完全相同的SQL语句，则将查询结果直接返回给客户端；如果没有开启查询缓存或没有查询到完全相同的SQL语句，则会由解析器进行语法语义解析，并生成"解析树"
    - 缓存select查询的结果和SQL语句
    - 执行select查询时，先查询缓存，判断是否存在可用的记录集，要求完全相同（包括参数值），这样才会匹配缓存数据中。
    - 即使开启查询缓存，以下SQL也不能缓存 
        - 查询语句使用 `SQL_NO_CACHE`
        - 查询的结果大于 `query_cache_limit` 设置
        - 查询中有一些不确定的参数，如now()
- 解析器，将客户端发送的SQL进行语法解析，生成"解析树"。预处理器根据MySQL规则进一步检查"解析树是否合法"
- 查询优化器，根据"解析树"生成最优的执行计划。MySQL使用很多优化策略生成最优的执行计划，可以分为两类: `静态优化（编译时优化）、动态优化（运行时优化）`
    - 等价变换策略
    - 优化count、min、max等函数
    - 提前终止查询
- 查询执行引擎，负责执行SQL语句，此时查询执行引擎会根据SQL语句中表的存储引擎类型以及对应的API接口与底层存储引擎缓存或物理文件的交互，得到查询结果并返回给客户端。若开启查询引擎，这时会将SQL语句和结果完整的保存到查询缓存中
    - 如果开启了查询缓存，先将查询结果做缓存操作
    - 返回结果过多，采用增量模式返回

### 1.3 MySQL 存储引擎

`show engines`

- InnoDB: 支持事务，具有提交，回滚和崩溃恢复能力，事务安全
- MyISAM: 不支持事务和外键，访问速度快
- Memory: 利用内存创建表，访问速度非常快，因为数据在内存，而且默认使用Hash索引，但是一旦关闭，数据就会丢失
- Archive: 归档类型引擎，仅能支持insert和select语句
- Csv: 以CSV文件进行数据存储，由于文件限制，所有列必须强制指定not null，另外csv引擎也不支持索引和分区，适合做数据交换的中间表
- BlackHole: 黑洞，只进不出，进来小时，所有插入数据都不会保存
- Federated: 可以访问远端MySQL数据库中的表，一个本地表，不保存数据，访问远程表内容


#### 1.3.1 InnoDB 和 MyISAM 对比

- 事务和外键
    - `InnoDB` 支持事务和外键，具有安全性和完整性，适合大量insert和update操作
    - `MyISAM` 不支持事务和外键，提供高速存储和检索，适合大量的select查询操作
- 锁机制
    - `InnoDB` 支持行级锁，锁定指定记录。基于索引来加锁实现
    - `MyISAM` 支持表级锁，锁定整张表
- 索引结构
    - `InnoDB` 使用聚集索引，索引和记录在一起存储，既缓存索引，也缓存记录
    - `MyISAM` 使用非聚集索引，索引和记录分开
- 并发处理能力
    - `InnoDB` 读写阻塞，可以通过隔离级别有关，可以采用多版本并发控制(MVCC)来支持高并发
    - `MyISAM` 使用表级锁，会导致写操作并发率低，读之间并不阻塞
- 存储文件
    - `InnoDB` 表对应两个文件，一个 `.frm` 表结构文件，一个 `.ibd` 数据文件
    - `MyISAM` 表对应三个文件，一个 `.frm` 表结构文件，一个 `MYD` 表数据文件，一个 `.MYI` 索引文件
- 适用场景
    **InnoDB**
    - 需要事务支持（具有较好的事务特性）
    - 行级锁定对高并发有很好的适应能力
    - 数据更新较为频繁的场景
    - 数据一致性要求较高
    - 硬件设备内存较大，可以利用InnoDB较好的缓存能力来提高内存利用率，减少磁盘IO

    **MyISAM**
    - 不需要事务支持（不支持）
    - 并发相对较低（锁定机制问题）
    - 数据修改相对较少，以读为主
    - 数据一致性要求不高

#### 1.3.2 InnoDB 底层原理（不是很全面）

<div align="center" width="80%"><img src="./assets/InnoDB内存结构.png"></div>

##### 1. InnoDB 内存结构

内存结构主要包括 `Buffer Pool、Change Buffer、Adaptive Hash Index、Log Buffer`

- `Buffer Pool:` 缓冲池，简称BP。BP以Page为单位，默认大小为16K，BP的底层采用链表数据结构管理Page。在InnoDB访问表记录和索引时会在Page页中缓存，以后使用可以减少磁盘IO操作，提升效率。
    - `Page 管理机制`，Page 根据状态可以分为三种类型
        - `free page:` 空闲page，未被使用
        - `clean page:` 被使用page，数据没有被修改过
        - `dirty page:` 脏页，被使用page，数据被修改过，页中数据和磁盘的数据产生了不一致
        - `free list:` 表示空闲缓存区，管理free page
        - `flush list:` 表示需要刷新到磁盘的缓冲区，管理`dirty page`，内部page按修改时间排序，脏页即存在flush链表，也在LRU链表中，但是两种互不影响，LRU链表负责管理page的可用性和释放，而flush链表负责管理脏页的刷盘操作
        - `lru_list:` 表示正在使用的缓冲区，管理 `clean page` 和 `dirty page`，缓冲区以 `midpoint` 为基点，前面链表称为new列表区，存放经常访问的数据，占63%，后面的链表称为old区，存放使用较少的数据，占37%
    - 改进型LRU算法维护
        - 普通LRU: 末尾淘汰法，新数据从链表头部加入，释放空间时从末尾淘汰
        - 新型LRU: 链表分为new和old两部分，加入元素时并不是从表头加入，而是从中间midpoint位置加入，如果数据很快被访问，那么page就会向new列表头部移动，如果数据没有被访问，会逐步向old尾部移动，等待淘汰
        每当有新的page数据读到buffer pool时，InnoDB引擎会判断是否有空闲页，是否足够，如果有将free page 从free list 列表删除，放入到LRU列表中。没有空闲页，就会根据LRU算法淘汰LRU链表默认的页，将内存空间释放分配给新的页。
    - Buffer Pool配置参数
        ```sql
        show variables like "%innodb_page_size%"; // 查看 page 页大小
        show variables like "%innodb_old%"; // 查看 lru list 中 old 列表参数
        show variables like "%innodb_buffer%"; // 查看 buffer poll 参数
        ```
- `Change Buffer:` 写缓冲区，简称CB。在进行DML操作时，如果没有其相应的Page数据，并不会立刻将磁盘页加载到缓冲池，而是在CB记录缓冲变更，等未来数据被读取时，再将数据合并恢复到BP中
- `Adaptive Hash Index:` 自适应哈希索引，用于优化对BP数据的查询，InnoDB存储引擎会监控对表索引的查找，如果观察到建立哈希索引可以带来速度的提升，则建立哈希索引，所以称之为自适应。InnoDB存储引擎会自动根据访问的频率和模式来为某些页建立哈希索引
- `Log Buffer:` 日志缓冲区，用于保存要写入磁盘上log文件（Redo/Undo）的数据，日志缓冲区的内容定期刷新到磁盘log文件中，日志缓冲区满时会自动将其刷新到磁盘，当遇到BLOB或多行更新的大事务操作时，增加日志缓冲区可以节省磁盘I/O
    - Log Buffe空间满了，会自动写入磁盘
    - `inoodb_flush_log_at_trx_commit` 参数控制日志刷新行为，默认为1
        - `0:` 每隔1s写日志文件和刷盘操作（写日志文件 LogBuffer-->OS cache，刷盘 OS cache-->磁盘文件）
        - `1:` 事务提交，立刻写日志文件和刷盘，数据不丢失，但是会频繁IO操作
        - `2:` 事务提交，立刻写日志文件，每隔1s进行刷盘操作

##### 2. InnoDB 磁盘结构
##### 3. InnoDB 后台线程

<div align="center" width="80%"><img src="./assets/InnoDB线程模型.png"></div>

##### 4. InnoDB 数据存储结构

分为一个ibd数据文件 -> Segment (段) —> Exent (区) -> Page (页) -> Row (行)

- TableSpace 表空间，用于存储多个ibd数据文件，用于存储表的记录和索引。一个文件包含多个段
- Segment 用于管理多个Extent，分为数据段、索引段、回滚段。一个表至少会有两个Segment，一个管理数据，一个管理索引。每多创建一个索引，会多两个Segment
- Extent 一个区固定包含64个连续的页，大小为1M。当表空间不足，需要分配新的页资源，不会一页一页分，直接分配一个区
- Page 用于存储多个Row行记录，大小为16K

##### 5. Undo Log

**Undo Log 介绍**

数据库事务开始之前，会将要修改的记录存放到Undo日志里，当事务回滚时或者数据库崩溃时可以利用Undo日志，撤销未提交事务对数据库产生的影响

**Undo Log 产生和销毁**

Undo Log 在事务开始前产生；事务在提交时，并不会立刻删除undo log，innodb 会将该事务对应的undo log放入到删除列表中，后面会通过后台线程purge thread进行回收处理，Undo Log属于逻辑日志

**Undo Log 存储**

undo log采用段的方式管理和记录。在innodb数据文件中包含一种rollback segment回滚段，内部包含1024个undo log segment

**Undo Log 作用**
- 实现事物的原子性
- 实现多版本并发控制（MVCC）

##### 5. Redo Log 和 Binlog


**Redo Log 介绍**

指事务中修改的任何数据，将最新的数据备份存储的位置（Redo Log），被称为重做日志

**Redo Log 工作原理**

为了实现事物的持久性而出现的产物

```sql
show variables like '%innodb_log%';
```
**Binlog**

Redo Log属于InnoDB引擎所特有的日志，而MySQL Server也有自己的日志，即Binary Log（二进制日志），简称Binlog。Binlog时记录所有数据库表结构变更以及表数据修改的二进制日志，不会记录SELECT和SHOW这类操作。Binlog日志是以时事件形式记录，还包含语句所执行的消耗时间。开启Binlog日志有以下两个最重要的使用场景。
- 主从复制: 在主库中开启Binlog功能，这样主库就可以把Binlog传递给从库，从库拿到Binlog后实现数据恢复达到主从数据一致性
- 数据恢复: 通过mysqlbinlog工具来恢复数据



- Binlog写入机制

    - 根据记录模式和操作触发 event 事件生成 Log event（事件触发执行机制）
    - 将事务执行过程中产生 Log event 写入缓冲区，每个事务线程都有一个缓冲区
    - Log Event 保存在一个 binlog_cache_mngr 数据结构中，在该结构中有两个缓冲区，一个是 stmt_cache，用于存放不支持事务的信息；另一个是 trx_cache，用于存放支持事务的信息。
    - 事务在提交阶段会将产生的 Log event 写入到外部 Binlog 文件中。
    - 不同事务以串行方式将 Log event 写入 Binlog 文件中，所以一个事务包含的 Log event 信息在 Binlog 文件中是连续的，中间不会插入其他事务的 Log event。

```sql
show variables like 'log_bin';
```

```sql
-- 开启 Binlog 功能
mysql> set global log_bin=mysqllogbin;
ERROR 1238 (HY000): Variable 'log_bin' is a read only variable
```

**Redo Log 和 Binlog 区别**
- Redo Log 属于InnoDB引擎功能，Binlog属于MySQL Server自带功能并且以二进制文件记录
- Redo Log 属于物理日志，记录该数据页更新状态内容，Binlog是逻辑日志，记录更新过程
- Redo Log 日志是循环写，日志空间大小是固定， Binlog 是追加写入，写完一个写下一个，不会覆盖使用。
- Redo Log 作为服务器异常宕机后事务数据自动恢复使用， Binlog 可以作为主从复制和数据恢复使用。 Binlog 没有自动 crash-safe 能力

# 2. 优化

## 2.1 索引

### 2.1.1 索引类型

索引可以提升查询速度，会影响 where 查询，以及 order by 排序。MySQL 索引类型如下：

- 从索引存储结构划分：B Tree 索引、Hash 索引、FULLTEXT 全文索引、R Tree 索引
- 从应用层次划分：普通索引、唯一索引、主键索引、复合索引
- 从索引键值类型划分：主键索引、辅助索引（二级索引）
- 从数据存储和索引键值逻辑关系划分：聚集索引（聚簇索引）、非聚集索引（非聚簇索引）

**普通索引**
这是最基本的索引类型，基于普通字段建立的索引，没有任何限制。

```sql
CREATE INDEX <索引的名字> ON tablename (字段名);
ALTER TABLE tablename ADD INDEX [索引的名字] (字段名);
CREATE TABLE tablename ( [...], INDEX [索引的名字] (字段名) );  
```

**唯一索引**
与"普通索引"类似，不同的就是：索引字段的值必须唯一，但 允许有空值 。在创建或修改表时追加唯一约束，就会自动创建对应的唯一索引。

```sql
CREATE UNIQUE INDEX <索引的名字> ON tablename (字段名);
ALTER TABLE tablename ADD UNIQUE INDEX [索引的名字] (字段名);
CREATE TABLE tablename ( [...], UNIQUE [索引的名字] (字段名) ;  
```

**主键索引**
它是一种特殊的唯一索引，不允许有空值。在创建或修改表时追加主键约束即可，每个表只能有一个主键。
```sql
CREATE TABLE tablename ( [...], PRIMARY KEY (字段名) );
ALTER TABLE tablename ADD PRIMARY KEY (字段名);  
```

**复合索引**
单一索引是指索引列为一列的情况，即新建索引的语句只实施在一列上；用户可以在多个列上建立索引，这种索引叫做组复合索引（组合索引）。复合索引可以代替多个单一索引，相比多个单一索引复合索引所需的开销更小。

索引同时有两个概念叫做窄索引和宽索引，窄索引是指索引列为1-2列的索引，宽索引也就是索引列超过2列的索引，设计索引的一个重要原则就是能用窄索引不用宽索引，因为窄索引往往比组合索引更有效。
```sql
CREATE INDEX <索引的名字> ON tablename (字段名1，字段名2...);
ALTER TABLE tablename ADD INDEX [索引的名字] (字段名1，字段名2...);
CREATE TABLE tablename ( [...], INDEX [索引的名字] (字段名1，字段名2...) );
```

全文索引
查询操作在数据量比较少时，可以使用 like 模糊查询，但是对于大量的文本数据检索，效率很低。如果使用全文索引，查询速度会比 like 快很多倍。在MySQL 5.6 以前的版本，只有 MyISAM 存储引擎支持全文索引，从 MySQL 5.6 开始 MyISAM 和 InnoDB 存储引擎均支持。

```sql
CREATE FULLTEXT INDEX <索引的名字> ON tablename (字段名);
ALTER TABLE tablename ADD FULLTEXT [索引的名字] (字段名);
CREATE TABLE tablename ( [...], FULLTEXT KEY [索引的名字] (字段名) ;
```
和常用的 like 模糊查询不同，全文索引有自己的语法格式，使用 match 和 against 关键字，比如：

```sql
select * from user
where match(name) against('aaa');
```
全文索引使用注意事项：
- 全文索引必须在字符串、文本字段上建立。
- 全文索引字段值必须在最小字符和最大字符之间的才会有效。（innodb：3-84；myisam：4-84）
- 全文索引字段值要进行切词处理，按 syntax 字符进行切割（参数 ft_boolean_syntax，默认 + -><()~*:""&|），例如 b+aaa，切分成 b 和 aaa
- 全文索引匹配查询，默认使用的是等值匹配，例如 a 匹配 a，不会匹配 ab, ac。如果想匹配可以在布
尔模式下搜索 a*

### 2.1.1 索引原理

MySQL官方对索引定义：是存储引擎用于快速查找记录的一种数据结构。需要额外开辟空间和数据维护工作。

- 索引是物理数据页存储，在数据文件中（InnoDB，ibd文件），利用数据页（page）存储。
- 索引可以加快检索速度，但是同时也会降低增删改操作速度，索引维护需要代价。
索引涉及的理论知识：二分查找法、Hash 和 B+Tree

**Hash 结构**
Hash 底层实现是由 Hash 表来实现的，是根据键值 <key,value> 存储数据的结构。非常适合根据 key 查找 value 值，也就是单个 key 查询，或者说等值查询。

InnoDB 自适应哈希索引是为了提升查询效率， InnoDB 存储引擎会监控表上各个索引页的查询，当 InnoDB 注意到某些索引值访问非常频繁时，会在内存中基于 B+Tree 索引再创建一个哈希索引，使得内存中的 B+Tree 索引具备哈希索引的功能，即能够快速定值访问频繁访问的索引页。

InnoDB 自适应哈希索引：在使用 Hash 索引访问时，一次性查找就能定位数据，等值查询效率要优于 B+Tree 。

自适应哈希索引的建立使得 InnoDB 存储引擎能自动根据索引页访问的频率和模式自动地为某些热点页建立哈希索引来加速访问。另外 InnoDB 自适应哈希索引的功能，用户只能选择开启或关闭功能，无法进行人工干涉

```sql
show engine innodb status \G;
show variables like '%innodb_adaptive%';
```

**B+Tree 结构**

- B-Tree 结构
    - 索引值和 data 数据分布在整棵树结构中
    - 每个节点可以存放多个索引值及对应的 data 数据
    - 树节点中的多个索引值从左到右升序排列
    - B树的搜索：从根节点开始，对节点内的索引值序列采用二分法查找，如果命中就结束查找。没有命中会进入子节点重复查找过程，直到所对应的的节点指针为空，或已经是叶子节点了才结束。
- B+Tree结构

    - 非叶子节点不存储 data 数据，只存储索引值，这样便于存储更多的索引值
    - 叶子节点包含了所有的索引值和 data 数据
    - 叶子节点用指针连接，提高区间的访问性能
    - 相比 B 树，B+ 树进行范围查找时，只需要查找定位两个节点的索引值，然后利用叶子节点的指针进行遍历即可。而 B 树需要遍历范围内所有的节点和数据，显然 B+Tree 效率高。
# leveldb File format

```
    <beginning_of_file>
    [data block 1]
    [data block 2]
    ...
    [data block N]
    [meta block 1]
    ...
    [meta block K]
    [metaindex block]
    [index block]
    [Footer]        (fixed size; starts at file_size - sizeof(Footer))
    <end_of_file>
```

该文件包含内部指针。 每个这样的指针都称为BlockHandle，包含以下信息：

```
    offset:   varint64
    size:     varint64
```

参阅[varints](https://developers.google.com/protocol-buffers/docs/encoding#varints)

有关varint64格式的说明。

1.文件中的键/值对序列按排序顺序存储，并分成一系列数据块。 这些块在文件开头一个接一个地出现。 每个数据块都根据`block_builder.cc`中的代码进行格式化，然后可选地进行压缩。

2.在数据块之后，我们存储了一堆元数据块。 支持的元数据类型如下所述。 将来可能会添加更多元数据类型。 每个元块再次使用`block_builder.cc`格式化，然后可选地进行压缩。

3.“metaindex”块。 它包含每个其他元块的一个条目，其中键是元块的名称，值是指向该元块的BlockHandle。

4.“index”块。 该块包含每个数据块一个条目，其中键是该数据块中的字符串> =最后一个键，并且在连续数据块中的第一个键之前。 该值是数据块的BlockHandle。

5.在文件的最后是一个固定长度的页脚，它包含metaindex和索引块的BlockHandle以及一个魔数。

```
metaindex_handle: char[p];     // Block handle for metaindex
index_handle:     char[q];     // Block handle for index
padding:          char[40-p-q];// zeroed bytes to make fixed length        (40==2*BlockHandle::kMaxEncodedLength)
magic:            fixed64;     // == 0xdb4775248b80fb57 (little-endian)
```

## “过滤” 元块

如果在打开数据库时指定了“FilterPolicy”参数，则会在每个表中存储过滤器块。 “metaindex”块包含一个条目，它从`filter.<N>`映射到过滤块的BlockHandle，其中`<N>`是过滤策略的`Name（）`方法返回的字符串。

过滤器块存储一系列过滤器，其中过滤器i包含存储在块中的所有键的“FilterPolicy :: CreateFilter（）”输出，该块的文件偏移量在该范围内 :  [ i\*base ... (i+1)\*base-1 ]

目前，“base”是2KB。 因此，例如，如果块X和Y在“[0KB .. 2KB-1]”范围内开始，则X和Y中的所有键将通过调用“FilterPolicy :: CreateFilter（）”转换为过滤器，并且生成的过滤器将存储为过滤器块中的第一个过滤器。

过滤器块的格式如下：

```
    [filter 0]
    [filter 1]
    [filter 2]
    ...
    [filter N-1]

    [offset of filter 0]                  : 4 bytes
    [offset of filter 1]                  : 4 bytes
    [offset of filter 2]                  : 4 bytes
    ...
    [offset of filter N-1]                : 4 bytes

    [offset of beginning of offset array] : 4 bytes
    lg(base)                              : 1 byte
```

滤波器块末尾的偏移数组允许从数据块偏移到相应滤波器的有效映射。

## “status” 元块

这个元块包含一堆统计信息。 键是统计的名称。 值包含统计信息。

```
TODO(postrelease): record following stats.

    data size
    index size
    key size (uncompressed)
    value size (uncompressed)
    number of entries
    number of data blocks
```


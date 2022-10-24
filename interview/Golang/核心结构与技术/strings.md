## strings 和 strconv

**strings**

| 序号 | 命令                              | 解释                                      |
| ---- | --------------------------------- | ----------------------------------------- |
| 1    | HasPrefix() &nbsp;  `strings.HasPrefix(s, prefix string) bool`                       | 前缀                                            |
| 2    | HasSuffix()   &nbsp;    `strings.HasSuffix(s, suffix string) bool`              | 后缀         |
| 3    | Contains()  &nbsp;    `strings.Contains(s, substr string) bool`            | 包含关系 |
| 4    | Index() &nbsp;  `strings.Index(s, str string) int`| 返回字符串 `str` 在字符串 `s` 中的索引（`str` 的第一个字符的索引），`-1` 表示字符串 `s` 不包含字符串 `str` |
| 5    | LastIndex() &nbsp;  `strings.LastIndex(s, str string) int`| 返回字符串 `str` 在字符串 `s` 中最后出现位置的索引，`-1` 表示字符串 `s` 不包含字符串 `str` |
| 6    | Replace() &nbsp;  `strings.Replace(str, old, new string, n int) string`| 将字符串 `str` 中的前 `n` 个字符串 `old` 替换为字符串 `new`，并返回一个新的字符串，如果 `n = -1` 则替换所有字符串 `old` 为字符串 `new` |
| 7    | Count() &nbsp;  `strings.Count(s, str string) int`| 计算字符串 `str` 在字符串 `s` 中出现的非重叠次数 |
| 8    | Repeat() &nbsp;  `strings.Repeat(s, count int) string`| 重复 `count` 次字符串 `s` 并返回一个新的字符串 |
| 9    | ToLower() &nbsp;  `strings.ToLower(s) string`| 将字符串中的 Unicode 字符全部转换为相应的小写字符 |
| 10    | ToUpper() &nbsp;  `strings.ToUpper(s) string`| 将字符串中的 Unicode 字符全部转换为相应的大写字符 |
| 11    | TrimSpace()  | 该函数的第二个参数可以包含任何字符，如果你只想剔除开头或者结尾的字符串，则可以使用 `TrimLeft()` 或者 `TrimRight()` 来实现 |
| 12    | Fields() | 将会利用 1 个或多个空白符号来作为动态长度的分隔符将字符串分割成若干小块，并返回一个 slice，如果字符串只包含空白符号，则返回一个长度为 0 的 slice |
| 13    | Split() | 自定义分割符号来对指定字符串进行分割，同样返回 slice |
| 14    | Join() &nbsp;  `strings.Join(sl []string, sep string) string`| 将元素类型为 string 的 slice 使用分割符号来拼接组成一个字符串 |

**strconv** 

| 序号 | 命令                              | 解释                                      |
| ---- | --------------------------------- | ----------------------------------------- |
| 1    | Itoa() &nbsp;  `strconv.Itoa(i int) string`                       | 返回数字 `i` 所表示的字符串类型的十进制数      |
| 2    | FormatFloat() &nbsp;  `strconv.FormatFloat(f float64, fmt byte, prec int, bitSize int) string`                       | 将 64 位浮点型的数字转换为字符串，其中 `fmt` 表示格式（其值可以是 `'b'`、`'e'`、`'f'` 或 `'g'`），`prec` 表示精度，`bitSize` 则使用 32 表示 `float32`，用 64 表示 `float64`      |
| 3    | Atoi() &nbsp;  `strconv.Atoi(s string) (i int, err error)`                       | 将字符串转换为 `int` 型      |
| 4    | ParseFloat() &nbsp;  `strconv.ParseFloat(s string, bitSize int) (f float64, err error)`                       | 将字符串转换为 `float64` 型     |

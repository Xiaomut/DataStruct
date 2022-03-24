## 1. redis 安装与配置

下载地址：下载zip压缩包 [https://github.com/MicrosoftArchive/redis/releases](https://github.com/MicrosoftArchive/redis/releases)

解压后打开 `cmd` 窗口并到其路径下

1. 使用该指令将redis注册为windows服务, `redis.windows-service.conf` 该文件就是注册服务使用的配置文件，在里面也可以更改设置密码，对应字段为 `requirepass`

```sh
redis-server --service-install redis.windows-service.conf --loglevel verbose
```

2. 启动redis服务

```sh
redis-server --service-start
```

3. python 链接

安装使用 `pip install redis`，我采用的是哈希存储，并设置过期时间进行测试。

```py
import redis

INFO_EXISTS = 'redis_temp'

r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)

for i in range(10):
    r.hset(INFO_EXISTS, f'name{i}', f'h{i}')
    r.expire(INFO_EXISTS, 10)

ret1 = r.hget(INFO_EXISTS, 'name2')
print(ret1)
```



## 2. mysql 安装与配置

我之前安装的是按照这个教程 [mysql 8.0.20 安装配置详细教程](https://www.jb51.net/article/186571.htm)，所以以这个为例

####　1. 配置mysql 
1. 解压后建一个 `my.ini` 的配置文件，修改其中的路径

2. 把 `bin` 目录添加到环境变量，管理员方式打开 `cmd`

3. 执行下面句子可以得到 `root` 对应的密码
```sh
mysqld --initialize --console
```

4. 启动服务 

```sql
net start mysql
```

5. 登录并修改密码

```sql
mysql -u root -p
ALTER USER root@localhost IDENTIFIED BY '123456';
```


#### 2. 如果root密码忘掉了解决方式（不需要强制进入数据库，这样失败了好几次没找到原因）

如果重新初始化，会不再显示密码信息；强制进入数据库，到更改密码的时候失败了，因此我按照错误信息尝试了一下

**找到与`bin`同级目录下的`data`文件夹，删除掉里面的所有内容，然后重新按照初始化的步骤来一遍就好了**

#### 3. py链接

安装：`pip install pymysql`

```py
import pymysql

db = pymysql.connect( host='localhost',
                              user='root',
                              password='123456',
                              db='world',
                              )

cur = db.cursor()
sql = 'select * from VERSION()'
cur.execute(sql)
data = cur.fetchall()
print(data)
```
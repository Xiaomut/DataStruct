
<font color="#f29e8e">**写在前面的话：**</font> 很久没有发博客了，其实写了很多文档，但都是很基础的一些内容，所以也没有发出来，而且被实验搞得焦头烂额，偶尔整点自己真正想做的东西。近期舍友告诉我他的服务器总是断网，想让我帮他写个脚本。我寻思这很容易，就花了十多分钟写了一个解决方案。


- 1. 服务器的网连接的是校园网，有固定域名，如果断开了登录即可
- 2. 加个定时任务

ok, 解决问题!

## 1. `selenium` 方式实现登录

界面比较简单，因此使用xpath也很容易定位

<div align="center"><img src="https://img-blog.csdnimg.cn/6363cc97b39e4e839463efc53cdc8759.png
" width="50%" alt=""></div>

找到对应的标签，并填入相应信息，登录即可（其中用的隐式等待）

<div align="center"><img src="https://img-blog.csdnimg.cn/102048c61ca742ca9cbd0cb59dcb61d8.png
" width="50%" alt=""></div>

```py

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   run.py
@Time    :   2021/12/15 10:32:57
@Author  :   LittleMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests

class NetAutoLink:
    def __init__(self, url='http://10.10.43.3/', username='', passwd='') -> None:
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.url = url
        self.username = username
        self.passwd = passwd

    def send_message(self):
        self.browser.get(self.url)
        try:
            logout_btn = WebDriverWait(self.browser, 3, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//form[@name="f1"]/input[@name="logout"]'))
            )
            if logout_btn:
                self.browser.close()
                return True
        except:
            pass

        try:
            username_btn = WebDriverWait(self.browser, 3, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//form[@name="f1"]/input[@name="DDDDD"]'))
            )
            username_btn.send_keys(self.username)

            passwd_btn = WebDriverWait(self.browser, 3, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//form[@name="f1"]/input[@name="upass"]'))
            )
            passwd_btn.send_keys(self.passwd)

            click_btn = WebDriverWait(self.browser, 1, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//form[@name="f1"]/input[@name="0MKKey"]'))
            )
            click_btn.click()
        except:
            self.browser.close()
            return False
        if self.browser:
            self.browser.close()
        return True
```

验证一下登录是否成功。在 `NetAutoLink` 类内如果处于连接状态会返回True，再去请求一下百度。

```py
def test_net(username, passwd, times=10):
    for i in range(times):
        spider = NetAutoLink(username=username, passwd=passwd)
        flag = spider.send_message()
        if flag:
            break
    print(flag)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    res = requests.get('https://www.baidu.com/', headers=headers)   # 请求一次百度判断连接是否成功
    if res.status_code == 200:
        print('Net Linked!') 
    else:
        print('Sending Message Failed!')

if __name__ == "__main__":
    username = ''
    passwd = ''
    # 默认重复请求10次
    test_net(username, passwd, 10)
```

## 2. 定时任务

crontab用法的精华就在这张表了

<div align="center"><img src="https://img-blog.csdnimg.cn/ae354f7183694268b3d22de6fbad95a9.png
" width="50%" alt=""></div>


我将脚本传到服务器上后，设置为每天运行一次，在早上8点0分运行。

```sh
crontab -e
```

```sh
0 8 */1 * * /绝对路径/python /绝对路径/run.py
```

保存后重启服务，再查看一下定时任务

```sh
service crond restart
crontab -l
```

---

<font color="#f29e8e">**结语：**</font> 最近没有太多时间做一些有意思的事情，我搞不来学术，不适合搞学术。思考的东西很多，也静不下心来搞学术，有很多想学的东西，也有很多有意思的东西等待我去创造。近期在刷题了，为实习和找工作做准备。
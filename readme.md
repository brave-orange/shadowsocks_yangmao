## 抓取注册SSR网站的试用账号
> 项目仅供爬虫学习测试之用，请勿挪作他用

注册邮箱使用的是10分钟快捷邮箱
## 原理
使用ssr网站的体验账号进行无限薅羊毛
+ 利用临时邮箱，注册网站账号
+ 登录注册的账号抓取ss服务器的信息
+ 使用`os.system()`运行`shadowsocks.exe`

## 使用
编辑`config.py`修改`shadowsocks_path`为你的shadowsocks.exe所在目录
装好相应的库直接运行run.py即可执行抓取

## 附：
本项目抓取的是基于shadowsocks-manager项目的网站，总是抓取一个容易把羊毛薅完，可以考虑使用 [钟馗之眼](https://www.zoomeye.org/) 搜索多找一些网站进行薅羊毛。


### 试用站点 http://brave-orange.cn/ssr 


### config.py内容

 ```python
 
import json,random
f = open('hosts/hosts.json','r')
res = f.read()
hosts = json.loads(res)
if len(hosts) <= 0:
    api_host = ""
else:
    api_host = hosts[random.randint(0,len(hosts)-1)]

config = {
"apply_url":"https://bccto.me/applymail",
"getmail_url":"https://bccto.me/getmail",
"mail_content_url":"https://bccto.me/win/",
"mail_host":["1766258.com","esoumail.com","juyouxi.com","a7996.com"], #@hotmail.cn
#"vpn_sign_vpn":"https://mmpvpn.com/api/home/signup"  #vpn网站注册地址http://176.119.29.45/home/signup
"vpn_sign_vpn":api_host+"/api/home/signup" ,
"vpn_api_url":api_host,
"account_page_url":"/api/public/views/user/account",
"account_signup_url":"/api/home/signup",
"redis":{ 
        "host":"127.0.0.1",
        "port":6379,
        "password":"abcdefg"
    },
'zoomeyAccount':'465486@qq.com',
'zoomeyPassword':'1654864186'

}
user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]
shadowsocks_path = "D:/shadowsocks" 
 ```

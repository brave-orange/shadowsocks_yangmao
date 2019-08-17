import requests,random,json,time,re
from pyquery import PyQuery
from config import *
# from get_free_email import *

class vpnAccount:   #注册vpn账号
    def __init__(self,email):
        self.email = email
        self.password = "www123456"
        self.session = requests.session()
    def sendCode(self):
        url = "https://mmpvpn.com/api/home/code"
        header = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'https://mmpvpn.com/home/signup',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        res = self.session.post(url, data=json.dumps({"email":self.email}), headers=header)
        if res.text == "success":
            return True
        else:
            return False
    def signUp(self,verifyCode):   #注册账号
        url = "https://mmpvpn.com/api/home/signup"
        header = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'https://mmpvpn.com/home/signup',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        postdata = {
            'code' : verifyCode,
            'email' : self.email,
            'password' : self.password
        }
        res = self.session.post(url, data=json.dumps(postdata), headers=header)
        if res.text == "normal":
            return True
        else:
            return False

    def getVpn(self):#获取ss账号
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://mmpvpn.com/user/index',
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        url = "https://mmpvpn.com/public/views/user/account"
        self.session.get(url)
        api_url = "https://mmpvpn.com/api/user/account" 
        res = self.session.get(api_url,headers=header)     #获取端口和密码
        print(res.text)
        result = json.loads(res.text)
        password = result[0]['password']
        port = result[0]['port']

        host_api = "https://mmpvpn.com/api/user/server"   #获取服务器域名
        res1 = self.session.get(host_api)     #获取端口和密码
        host = json.loads(res1.text)
        hosts = []
        for i in hosts:
            hosts.append(i["host"])

        return {"password":password,"port":port,"hosts":hosts}

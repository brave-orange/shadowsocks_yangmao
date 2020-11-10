import requests,random,json,time,re
from requests import exceptions
from pyquery import PyQuery
from config import *
# from get_free_email import *

class vpnAccount:   #注册vpn账号
    def __init__(self,email,host=""):
        self.email = email
        self.password = "www123456"
        self.session = requests.session()
        if host == "":
            self.baseurl = config["vpn_api_url"]
        else:
            self.baseurl = host
    def sendCode(self):
        url = self.baseurl+"/api/home/code"
        print("发送验证码:"+url)
        header = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'https://mmpvpn.com/home/signup',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        try:
            res = self.session.post(url, data=json.dumps({"email":self.email}), headers=header, timeout=8,verify=False)
        except exceptions.Timeout as e:     #超时了
            print("发送验证码失败"+str(e))
            return False
        if res.text == "success":
            return True
        else:
            print("发送验证码失败")
            return False
    def signUp(self,verifyCode):   #注册账号
        
        url = self.baseurl+config["account_signup_url"]
        print("拿到验证码,开始注册 %s, url:%s"%(verifyCode,url))
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
        try:
            res = self.session.post(url, data=json.dumps(postdata), headers=header,timeout=8,verify=False)
        except exceptions.Timeout as e:     #超时了
            print("连接超时:"+url)
            return False
        print(res.text)
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
        url = self.baseurl+config["account_page_url"]
        self.session.get(url)
        api_url = self.baseurl+"/api/user/account" 
        try:
            res = self.session.get(api_url,headers=header)     #获取端口和密码
            result = json.loads(res.text)
        except:
            print("出现错误:"+res.text)
            return False
        if len(result) == 0:
            return False
        password = result[0]['password']
        port = result[0]['port']
        endTime = result[0]['data']['to']
        expireTime = result[0]['data']['expire']
        timeArray = time.localtime(expireTime/1000)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
         

        host_api = self.baseurl+"/api/user/server"   #获取服务器域名python36 /website/goods/good_shap/server.py
        res1 = self.session.get(host_api)     #获取地址
        host = json.loads(res1.text)
        hosts = []
        for i in host:
            hosts.append({"host":i["host"],"method":i["method"]})
        return {"password":password,"port":port,"hosts":hosts,'end_time':otherStyleTime,'end_time_step':expireTime}

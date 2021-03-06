#!/usr/bin/env python
# encoding=utf-8
# 得到节点,写入redis脚本
from get_free_email import *
from getVpnAccount import *
from myRedis import *
from config import *
import time,socket,re
from ping3 import ping
#"https://47.75.188.161","https://34.92.160.214:443", "http://47.102.111.56:8005", "http://144.34.168.135:18080", "https://47.75.188.161:443", "http://129.226.168.109:80",

HOSTSKEY = "check_ware"
redis = RedisDb(config['redis']['host'],config['redis']['port'],config['redis']['password'])

def pingHost(ip):
    """
    获取节点的延迟的作用
    :param node:
    :return:
    """
    ip_address  = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", ip)
    response = ping(ip_address[0])
    if response is not None:
        delay = int(response * 1000)
        return delay
    else:
        return 30000
        # 下面两行新增的
#     
print("先刷一遍数据")
count = redis.llen(HOSTSKEY)
for item in range(count):
    oldData = redis.lpop(HOSTSKEY)
    now = time.time()*1000
    second = round((json.loads(oldData)['end_time_step'] - now))
    if not second < 0-(600):
        redis.rpush(HOSTSKEY,oldData)
hostsFile = open('hosts/hosts.json','r')
hosts = json.loads(hostsFile.read())
print(hosts)
i=0
newEmail = email()  #先生成一个邮箱

for hostItem in hosts:
    relay = pingHost(hostItem)
    print(hostItem,"延迟:",relay)
    if relay > 1500:
        continue
    account = vpnAccount(newEmail.getMailAddr(),hostItem)  #准备开始申请账号
    if account.sendCode():  #发送验证码
        print("验证码已发送")
        now  = time.time()
        error = False
        code = ""
        print("开始等邮件")
        while True:
            eml = newEmail.getmail()
            if eml:
                print("收到验证码邮件")
                time.sleep(3)
                code = newEmail.getMailContent(eml)
                break
            time.sleep(6)
            if time.time()-now > 120.0:   #超时未收到验证码，出错
                error = False
                break
        if error:
            print("程序异常了")
            continue
        if code == "":
            print("验证码获取错误")
            continue
        else:
            if account.signUp(code):
                print('注册的账号为：',newEmail.getMailAddr())
                host = account.getVpn()
                hosts = []
                # print("ss服务器信息：",host)
                if not host:   #这个站点没提供服务器
                    continue
                for x in host['hosts']:
                    if x['host'] == "127.0.0.1" or x['host'] == "0.0.0.0":
                        print("代理IP为127.0.0.1")
                        continue
                    ttt = int(pingHost(x['host']))
                    if ttt > 3000:
                        print(x['host']+ "延迟达到%d淘汰"%ttt)
                        continue
                    x['password'] = host['password']
                    x['port'] = host['port']
                    x['end_time'] = host['end_time']
                    x['end_time_step'] = host['end_time_step']
                    print("push to redis:%s"%(json.dumps(x)))
                    redis.lpush(HOSTSKEY,json.dumps(x))
                






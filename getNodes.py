#!/usr/bin/env python
# encoding=utf-8
# 得到节点,写入redis脚本
from get_free_email import *
from getVpnAccount import *
from myRedis import *
from config import *
import time


HOSTSKEY = "check_ware"
redis = RedisDb(config['redis']['host'],config['redis']['port'],config['redis']['password'])
email = email()  #先生成一个邮箱

print("先刷一遍数据")
count = redis.llen(HOSTSKEY)
for item in range(count):
    oldData = redis.lpop(HOSTSKEY)
    now = time.time()*1000
    if not (json.loads(oldData)['end_time_step'] - now)/1000 > (5*3600):
        redis.rpush(HOSTSKEY,oldData)

hostsFile = open('hosts/hosts.json','r')
hosts = json.loads(hostsFile.read())
print(hosts)
i=0
for hostItem in hosts:
    account = vpnAccount(email.getMailAddr(),hostItem)  #准备开始申请账号
    if account.sendCode():  #发送验证码
        print("验证码已发送")
        now  = time.time()
        error = False
        code = ""
        print("开始等邮件")
        while True:
            eml = email.getmail()
            if eml:
                print("收到验证码邮件")
                time.sleep(3)
                code = email.getMailContent(eml)
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
                print('注册的账号为：',email.getMailAddr())
                host = account.getVpn()
                hosts = []
                print("ss服务器信息：",host)
                for x in host['hosts']:
                    x['password'] = host['password']
                    x['port'] = host['port']
                    x['end_time'] = host['end_time']
                    x['end_time_step'] = host['end_time_step']
                    print("push to redis:%s"%(json.dumps(x)))
                    redis.lpush(HOSTSKEY,json.dumps(x))
                
             






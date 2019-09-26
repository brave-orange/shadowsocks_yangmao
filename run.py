from get_free_email import *
from getVpnAccount import *
import os

def connectSSR(host):   ##连接ss服务器
    with open(shadowsocks_path+"/gui-config.json","r+", encoding="utf-8") as f:
        res = f.read()
        config = json.loads(res)
        config["configs"] = []
        for item in host["hosts"]:
            config["configs"].append({
              "server": item["host"],
              "server_port": host["port"],
              "password": host["password"],
              "method": item["method"],
              "plugin": "",
              "plugin_opts": "",
              "remarks": "",
              "timeout": 5
             })
        config_str = json.dumps(config)
        f.seek(0)
        f.truncate()
        f.write(config_str)
        print(config)
    os.system("taskkill /F /IM shadowsocks.exe")   #终止shadowsocks进程
    os.system(shadowsocks_path+"/shadowsocks.exe")

email = email()  #先生成一个邮箱
print(config["vpn_sign_vpn"])

account = vpnAccount(email.getMailAddr())  #准备开始申请账号
if account.sendCode():  #发送验证码
    print("验证码已发送")
else:
    print("验证码发送错误")
    exit()
now  = time.time()
error = False
code = ""
while True:
    eml = email.getmail()
    if eml:
        print("收到验证码邮件")
        time.sleep(3)
        code = email.getMailContent(eml)
        break
    time.sleep(6)
    if time.time()-now > 60.0:   #超时未收到验证码，出错
        error = False
        break
if error:
    print("程序异常了")
    exit()
if code == "":
    print("验证码获取错误")
    exit()
else:
    if account.signUp(code):
        print('注册的账号为：',email.getMailAddr())
        host = account.getVpn()
        print("ss服务器信息：",host)
        connectSSR(host)
     






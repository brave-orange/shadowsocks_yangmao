from get_free_email import *
from getVpnAccount import *


email = email()  #先生成一个邮箱
account = vpnAccount(email.getMailAddr())  #准备开始申请账号
account.sendCode()  #发送验证码
print("验证码已发送")
now  = time.time()
error = False
code = ""
while True:
    eml = email.getmail()

    if eml:
        time.sleep(10)
        code = email.getMailContent(eml)
        break
    time.sleep(6)
    if time.time()-now > 60.0:   #超时未收到验证码，出错
        error = False
        break
if error:
    print("程序异常了")
if code == "":
    print("验证码获取错误")
else:
    if account.signUp(code):
        print('注册的账号为：',email.getMailAddr())

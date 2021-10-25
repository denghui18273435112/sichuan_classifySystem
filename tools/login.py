from tools.verification_code import *
import requests
from configs.path import *

#识别验证码登录
res=requests.get("https://platform.giiatop.com/sc/base/home/VerificationCode?height=40&width=128&fontsize=20&rnd=0.7109143157674591")
if res.status_code==200:
    imgname  = file_data+os.sep+'code.jpg'
    with open(imgname,"wb") as fd:
        fd.write(res.content)
headers= {"cookie":"vcode={0}".format(res.cookies["vcode"])}

data = {"type":"I","Name":"zhudan","Vcode":"tjym","Pwd":"a9b124a391f34eb28d3543d35b8044fb"}
data["Vcode"] = verification_code("code.jpg")
body = requests.post(url="https://platform.giiatop.com/sc/base/home/Login",json=data,headers=headers)

print(data)
print(headers)
print(body.cookies)
print(body.json()["msg"])

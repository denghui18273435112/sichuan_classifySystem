#-*- conding:utf-8 -*-
#@File      :login.py
#@Time      : 23:06
#@Author    :denghui
#@Email     :314983713@qq.com
#@Software  :PyCharm
import requests
from configs.conf import url
from tools.allureUitl import alluer_new
import json
from configs.conf import *
from tools.md5Uitl import get_md5
from configs.conf import *

class login:

    def login(inData,conftest=True):
        """
        账号登录
        :param token:
        :return:
        """
        new_url = url+inData["url"]
        data = json.loads(inData["params"])
        session = requests.session()
        body = session.post(url=new_url,json=data)
        cookies=requests.utils.dict_from_cookiejar(session.cookies)
        token = cookies[cookie_name]
        return token
import pytest
from configs.path import *
from lib.all import *
from tools.ExcelData import ExcelData
from tools.verification_code import verification_code
import json
import os
import requests
from configs.conf import *
from configs.path import test_xlsx
from tools.update_data import update_data
import datetime
from tools.allureUitl import alluer_new
from tools.md5Uitl import get_md5
from tools.commonly_method import *
from tools.Base import *


def login(case_id="login-001"):
    """
    获取登录token
    省公司登陆
    :return:
    """
    token = ""
    while True:
        #付费的
        res=requests.get("{}/base/home/VerificationCode?".format(url))
        if res.status_code==200:
            imgname  = data_path+os.sep+'code.jpg'
            with open(imgname,"wb") as fd:
                fd.write(res.content)
        vcode = res.cookies["vcode"]
        headers= {"cookie":"{0}={1}".format(vcode_name,vcode)}
        data = json.loads(ExcelData(case_id)[0]["params"])
        data["vcode"] = verification_code("code.jpg")
        body = requests.post(url="{}/base/home/Login".format(url),json=data,headers=headers)
        if body.json()["msg"]=="登录成功":
            token = "{0}={1};{2}={3}".format(cookie_name,body.cookies[cookie_name],vcode_name,vcode)
            break
    return token

def  requests_zzl(case_id,token_1=None,company_id_1=None,year=None,file=None):
    """
接口请求
    :return:
    """
    table_data = ExcelData(case_id)[0]
    url_new = url+table_data["url"]
    data_new = json.loads(table_data["params"])
    for key in data_new.keys():
        if key == "plan_year" or key == "training_year" or key == "year":
            data_new[key] = year
        if key == "company_id" or key == "companyId":
            data_new[key] = company_id_1
        if key == "pageNum":
            data_new[key] = 1
        if key == "pageSize":
            data_new[key] = 20
        if key == "start_date":
            data_new[key] = "{}-01-01".format(date_YmdHMS(5))
        if key == "end_date":
            data_new[key] = "{}".format(date_YmdHMS(4))
        if key == "date" or key == "created_time":
                if "test_GetTrendChart_01"  in table_data["case_id"] or "test_GetStatisList"  in table_data["case_id"]:
                    pass
                else:
                    data_new[key][0] = "{}-01-01".format(date_YmdHMS(5))
                    data_new[key][1] = "{}".format(date_YmdHMS(4))
    if "evaluation_01" in case_id:
        header = {"Cookie":"vcode=denghui; cipcms.token=denghui; zzlvcode=denghui"}
    else:
        header = {"Cookie":"{0}".format(token_1)}

    if "case_PIQ_04" in case_id :
        return requests.post(url=url_new,headers=header,data=data_new,files=file).json()
    else:
        return requests.post(url=url_new, headers=header, json=data_new).json()





if __name__ == '__main__':
    #print(login("login-001"))
    data = requests_zzl(case_id="evaluation_01")
    print(data)



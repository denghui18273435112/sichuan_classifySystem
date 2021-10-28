import pytest
from configs.path import *
from lib.all import *
from lib.login import login
from tools.ExcelData import ExcelData
from selenium import webdriver
from configs.path import *
import time
import imageio
import pytest
import os
from tools.verification_code import *
import requests
from configs.path import *
from configs.conf import *

@pytest.fixture(scope="session",autouse=True)
def empty_report_file():
    """清空report-result文件夹,除environment.properties以外的其它所有文件"""
    try:
        for one in os.listdir(result_path):
            if "environment.properties" not in one:
                os.remove(result_path+os.sep+"{}".format(one))
    except:
        pass

@pytest.fixture(scope="session")
def token():
    """获取登录token"""
    token = ""
    while True:
        res=requests.get("{}/base/home/VerificationCode?".format(url))
        if res.status_code==200:
            imgname  = file_data+os.sep+'code.jpg'
            with open(imgname,"wb") as fd:
                fd.write(res.content)
        vcode = res.cookies["vcode"]
        headers= {"cookie":"{0}={1}".format(vcode_name,vcode)}
        data = json.loads(ExcelData("login-001")[0]["params"])
        data["Vcode"] = verification_code("code.jpg")
        body = requests.post(url="{}/base/home/Login".format(url),json=data,headers=headers)
        token = "{0}={1};{2}={3}".format(cookie_name,body.cookies["cipcms.token"],vcode_name,vcode)
        if body.json()["msg"]=="登录成功":
            break
    return token

@pytest.fixture(scope="session")
def Index(token):
    """最核心的接口"""
    data = all(token=token,inData=ExcelData("case_Index")[0],conftest=False).ParameterlessAdjustment()[1].json()
    return data

@pytest.fixture(scope="session")
def GetYear(token):
    """获取年份"""
    data = all(token=token,inData=ExcelData("case_GetYear")[0],conftest=False).ParameterlessAdjustment()[1].json()["data"]
    return data[len(data)-1]

@pytest.fixture(scope="session")
def role(token):
    """获取角色列表"""
    return all(token=token,inData=ExcelData("case_role_All")[0],conftest=False).ParameterlessAdjustment()[1].json()

@pytest.fixture(scope="session")
def company(token):
    """获取当前账号登录的所属公司id"""
    return all(token=token,inData=ExcelData("case_GetCurrentCompany")[0],conftest=False).ParameterlessAdjustment()[1].json()["data"]["id"]

@pytest.fixture(scope="session")
def member_id(token,company,GetYear):
    """获取成员的member_id"""
    return all(token=token,inData=ExcelData("case_GetDetailList-01")[0],conftest=False).ParameterlessAdjustment(company=company,year=GetYear)[1].json()["data"]["list"][0]["member_id"]

@pytest.fixture(scope="session")
def courseId(token):
    """courseId"""
    return all(token=token,inData=ExcelData("case_GetCurrentCourse")[0],conftest=False).ParameterlessAdjustment()[1].json()["data"][1]["id"]

@pytest.fixture(scope="session")
def module(token,courseId):
    """module"""
    return all(token=token,inData=ExcelData("case_GetFrameModuleByCourse")[0],conftest=False).ParameterlessAdjustment(courseId=courseId)[1].json()["data"][1]

@pytest.fixture(scope="session")
def module(token,courseId):
    """module"""
    return all(token=token,inData=ExcelData("case_GetFrameModuleByCourse")[0],conftest=False).ParameterlessAdjustment(courseId=courseId)[1].json()["data"][1]

@pytest.fixture(scope="session")
def name_id_number(token,company,GetYear):
    """name_id_number"""
    data =  all(token=token,inData=ExcelData("case_membertraining_GetRecord-01")[0],conftest=False).ParameterlessAdjustment(company=company,year=GetYear)[1].json()["data"]["list"][0]
    return data["name"],data["id_number"]

@pytest.fixture(scope="session")
def GetMemberTriningOffline_id(token,company,GetYear):
    """GetMemberTriningOffline_id"""
    data =  all(token=token,inData=ExcelData("case_GetMemberTriningOffline_01")[0],conftest=False).ParameterlessAdjustment(company=company,year=GetYear)[1].json()["data"]["list"][0]
    return data["id"]

@pytest.fixture(scope="session")
def GetTestDetail_id_name(token,company,GetYear):
    """GetTestDetail_id_name"""
    data =  all(token=token,inData=ExcelData("case_GetTestDetail_01")[0],conftest=False).ParameterlessAdjustment(company=company,year=GetYear)[1].json()["data"]["list"][0]
    return data["name"],data["id_number"]

@pytest.fixture(scope="session")
def companyId(token,company,GetYear):
    """companyId"""
    data =  all(token=token,inData=ExcelData("case_GetCompanyTestSum_01")[0],conftest=False).ParameterlessAdjustment(company=company,year=GetYear)[1].json()["data"]["list"][0]
    return data["companyId"]

@pytest.fixture(scope="session")
def GetListOnJobCurrent_name_id(token,company):
    """在职人员管理；第一行的姓名 身份证"""
    data =  all(token=token,inData=ExcelData("case_GetListOnJobCurrentt_01")[0],conftest=False).ParameterlessAdjustment(company=company)[1].json()["data"]["list"][0]
    return data["memberName"],data["idNumber"]

@pytest.fixture(scope="session")
def account_nameOrNickName(token,company):
    """账号管理-列表数据-获取一条数据；姓名、昵称"""
    data =  all(token=token,inData=ExcelData("case_adminuserList_01")[0],conftest=False).ParameterlessAdjustment(company=company)[1].json()["data"]["list"][1]
    return data["name"],data["nickName"]

@pytest.fixture(scope="session")
def delete_id(token,company):
    """账号管理-列表数据-获取一条数据；姓名、昵称"""
    res =  all(token=token,inData=ExcelData("case_adminuserList_01")[0],conftest=False).ParameterlessAdjustment(company=company)[1].json()
    del_list = []
    for x in range(int(len(res["data"]["list"]))):
        name = res["data"]["list"][x]["name"]
        nickName = res["data"]["list"][x]["nickName"]
        if  name!=None  or nickName!=None:
            if "denghuidenghui" in name and  "denghuidenghui" in nickName:
                del_list.append(res["data"]["list"][x]["id"])
    return  del_list


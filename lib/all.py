#-*- conding:utf-8 -*-
#@File      :all.py
#@Time      : 18:44
#@Author    :denghui
#@Email     :314983713@qq.com
#@Software  :PyCharm
import json
import os
import requests
from configs.conf import *
from configs.path import test_xlsx
from tools.update_data import update_data
import datetime
from tools.allureUitl import alluer_new
from tools.md5Uitl import get_md5
from configs.path import *
import time
import win32gui
import allure
import win32con
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from tools.ExcelData import ExcelData
from tools.commonly_method import *
import traceback
from tools.Base import *
class all:
    """
    所有模块
    """
    def __init__(self,association_token,association_company_id, #协会token、公司id
                        province_token,province_company_id,     #省公司token、公司id
                        inData,GetYear,                         #表格数据、当前年份
                        conftest=True):

        self.proxies = {"https":"http://127.0.0.1:8888"}
        self.new_url= url+inData["url"]
        self.data = json.loads(inData["params"])
        self.conftest=conftest
        self.token = association_token
        self.company=association_company_id

        self.association_token =association_token
        self.association_company_id= association_company_id
        self.province_token = province_token
        self.province_company_id = province_company_id
        self.inData = inData
        self.GetYear = GetYear
        case_id = self.inData["case_id"]
        #根据接口不同选择不同的token  省协会 省公司
        if "case_PD_01" in inData["case_id"] or "case_PS_02"in inData["case_id"] or "case_TRE_04"in inData["case_id"]:
            self.header = {"Cookie":"{0}".format(province_token)}
        else:
            self.header = {"Cookie":"{0}".format(association_token)}
        #替换字段
        if "case" in case_id:
            for key  in self.data:
                #公司id
                if key == "company_id":
                    if "case_PS_02" in  case_id:
                        self.data["company_id"] = province_company_id
                    elif "case_PIC_04" in case_id:
                        pass
                    else:
                        self.data["company_id"] = association_company_id
                #时间、日期
                elif key == "created_time" or  key == "date"  or key == "updated_time" or key=="date_end":
                    if "case_HP_04" in case_id or "case_HP_05" in case_id or "case_TRS_01" in case_id or "case_TRS_01" in case_id \
                            or  "case_PCIT" in case_id or "case_IPM" in  case_id or "case_ESE" in  case_id:
                        pass
                    elif "case_TPC_04" in  case_id:
                         self.data[key] = "{}".format(date_YmdHMS(2))
                    elif  "case_PIC_04" in case_id or "case_MFS_01" in case_id or "case_MFS_02" in case_id:
                        self.data[key] = "{}".format(date_YmdHMS(4))
                    else:
                        self.data[key][0] = "{}-01-01".format(GetYear)
                        self.data[key][1] = "{}".format(date_YmdHMS(4))
                elif key == "class_date_end":
                    self.data[key] = "{}".format(date_YmdHMS(2))
                elif key == "class_date_begin":
                    self.data[key] = "{}-01-01 01:01:01".format(GetYear)
                elif key == "start_date" or  key == "bdate" or key=="date_begin":
                    if "case_TRS_01"  in case_id:
                        pass
                    else:
                        self.data[key] = "{}-01-01".format(GetYear)
                elif key == "end_date" or  key == "edate" or key == "date_end":
                    if "case_TRS_01" in case_id or "case_ESE" in  case_id:
                        pass
                    else:
                        self.data[key] = "{}".format(date_YmdHMS(4))
                elif key == "dateRange":
                    self.data[key][0] = "{}-01-01".format(GetYear)
                    self.data[key][1] = "{}".format(date_YmdHMS(4))
                #年份
                elif key == "plan_year" or key == "training_year" or key == "year":
                    self.data[key] = GetYear

    def case_ALL(self):
        """所有"""
        try:
            case_id = self.inData["case_id"]
            #文件参数
            if "case_PD_01" in case_id:
                self.request_file = {'file':('05四川培训记录汇总表导入模板(寿险).xlsx',open(file_path_06,"rb"),file_type)}
            if "case_PD_04" in case_id:
                self.request_file = {'file':('02四川在职人员导入模板.xlsx',open(file_path_03,"rb"),file_type)}
            if "case_PD_05" in case_id:
                self.request_file = {'file':('03四川离职人员导入模板.xlsx',open(file_path_04,"rb"),file_type)}
            if "case_PIQ_04" in case_id:
                self.request_file = {'file':('01入职前诚信级别批量查询模板.xlsx',open(file_path_02,"rb"),file_type)}
            #接口依赖
            if "case_PD_03" in case_id:
                data = requests_zzl("PD_02",self.token,self.company,self.GetYear)
                new_list=[]
                for key in range(int(len(data["data"]["list"]))):
                    if data["data"]["list"][key]["class_name"] == "审核数据20138":
                        new_list.append(data["data"]["list"][key]["id"])
                self.data["ids"] = new_list
            if "case_TRE_04" in case_id:
                data = requests_zzl("case_TRE_03",self.token,self.company,self.GetYear)["data"]["list"][0]["id"]
                self.data["id"] =data
            if "case_TPC_04" in case_id:
                body = requests_zzl("case_TPC_03",self.token,self.company,self.GetYear)["data"]["list"][0]
                self.data["id"] =body["id"]
                self.data["company_id"] = self.province_company_id
                self.data["commpanyArr"][1] = self.province_company_id
                self.data["member_id"]  =body["member_id"]
            if "case_PIQ_06" in case_id:
                body = requests_zzl("case_PIQ_01",self.token,self.company,self.GetYear)["data"]["list"][0]
                self.data["id"]  =body["member_id"]
            if "case_PIQ_05" in case_id:
                file = {'file':('01入职前诚信级别批量查询模板.xlsx',open(file_path_02,"rb"),file_type)}
                body = requests_zzl("case_PIQ_04",self.token,self.company,self.GetYear,file=file)["data"]
                self.data["id_number_array"] = body
            if "case_PIC_04" in case_id:
                body = requests_zzl("case_PIC_01",self.token,self.company,self.GetYear)["data"]["list"][0]
                self.data["id"]  = int(body["id"])
                self.data["member_id"]  = body["member_id"]
            if "case_MFS_03" in case_id:
                body = requests_zzl("case_PIC_01",self.token,self.company,self.GetYear)["data"]["list"][0]
                self.data["id"]  = int(body["id"])
                self.data["departure_date"] ==date_YmdHMS(4)

            #请求参数是否上传文件
            if "case_PD_01" in case_id or "case_PD_04" in case_id or "case_PD_05" in case_id or "case_PIQ_04" in case_id:
                body = requests.post(url=self.new_url,headers=self.header,data=self.data,files=self.request_file)
            else:
                body = requests.post(url=self.new_url,headers=self.header,json=self.data)
        except BaseException:
            traceback.print_exc()
            self.data["actual_result"] = traceback.format_exc()
        finally:
            print(self.inData["case_id"]+"-"+self.inData["case_name"])
            print(self.new_url)
            print(self.header)
            print(self.data)
            print(body.json())
            print("\n")
            inData = update_data(self.inData,self.data,self.new_url,self.header,body.json(),json.loads(self.inData["response_expect_result"]),self.conftest)
            return inData,body
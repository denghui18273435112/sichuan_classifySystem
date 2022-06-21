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

#分页所需
pageNum= 1
pageSize= 5
count=0


class all:
    """
    所有模块
    """
    def __init__(self,association_token,association_company_id, #协会token、公司id
                        province_token,province_company_id,     #省公司token、公司id
                        inData,GetYear,                         #表格数据、当前年份
                        conftest=True):
        self.proxies = {"http":"http://127.0.0.1:8888"}
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
        ##############################根据接口不同选择不同的token;支持：省协会、省公司、非空cookie、测评##############################
        if "case_PD_01" in inData["case_id"] or "case_PS_02"in inData["case_id"] or "case_TRE_04"in inData["case_id"]\
                or "case_FPR_02"in inData["case_id"] or "case_FPR_03"in inData["case_id"]:
            self.header = {"Cookie":"{0}".format(province_token)}
        elif "case_H5_" in   inData["case_id"]:
            self.header = {"Cookie":""}
        elif "case_evaluation_" in   inData["case_id"]:
            self.header = {"token":"{0}".format(requests_zzl(case_id="evaluation_01")["data"]["token"])}
        else:
            self.header = {"Cookie":"{0}".format(association_token)}
        ##############################替换字段-根据id替换##############################
        if "case_HP_" in case_id:
            if "case_HP_01" in case_id:
                self.data["company_id"] = association_company_id
                self.data["plan_year"] = date_YmdHMS(5)
            elif "case_HP_02" in case_id:
                self.data["plan_year"] = date_YmdHMS(5)
            elif "case_HP_03" in case_id:
                self.data["company_id"] = association_company_id
                self.data["plan_year"] = date_YmdHMS(5)
            elif "case_HP_04" in case_id:
                self.data["plan_year"] = date_YmdHMS(5)
            elif "case_HP_05" in case_id:
                self.data["company_id"] = association_company_id
                self.data["plan_year"] = date_YmdHMS(5)
            elif "case_HP_06" in case_id:
                self.data["plan_year"] = date_YmdHMS(5)
                self.data["date"] = date_YmdHMS(6)

        elif "case_ASE_" in case_id:
            self.data["company_id"] = association_company_id
            self.data["date_end"] = date_YmdHMS(4)
            self.data["statistical_date"] = date_YmdHMS(4)
            self.data["company"][0] = association_company_id
        elif "case_FSE_" in case_id:
            self.data["company_id"] = association_company_id
            self.data["company"][0] = association_company_id
        elif "case_FPR_" in case_id:
            self.data["companyId"] = association_company_id
        elif "case_PRIS_" in case_id:
            self.data["companyId"] = association_company_id
        elif "case_IP_" in case_id:
            self.data["year"] = date_YmdHMS(5)
        elif "case_AM_02" in case_id:
            self.data["companyId"] = association_company_id
        elif "case_ED_06" in case_id:
            self.data["plan_year"] = GetYear
        elif "case_PD_01" in case_id:
            self.data["class_date_end"] = date_YmdHMS(2)
        elif "case_GTOHNQ_" in case_id:
            self.data["companyId"] = association_company_id
            self.data["historyTrainingYear"] = GetYear-1
            self.data["pageNum"] = pageNum
            self.data["pageSize"] = pageSize
            self.data["count"] =count
        elif "case_AS_" in case_id:
            self.data["inst_id"] = association_company_id
            self.data["year"] = GetYear
            self.data["pageNum"] = pageNum
            self.data["pageSize"] = pageSize
            self.data["count"] =count
            self.data["date_begin"] ="{}-01-01".format(date_YmdHMS(5))
            self.data["date_end"] =date_YmdHMS(4)
        elif "case_CR_" in case_id:
            if "case_CR_01"==case_id:
                self.data["CompanyId"] = association_company_id
                self.data["trainingyear"] = GetYear
            if "case_CR_02"==case_id:
                self.data["AuditStatus"] = 15
                self.data["trainingyear"] = GetYear
            if "case_CR_03"==case_id:
                pass
            self.data["pageNum"] = pageNum
            self.data["pageSize"] = pageSize



        #比较乱的替换字段
        elif "case" in case_id:
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
                            or  "case_PCIT" in case_id or "case_IPM" in  case_id or "case_ESE" in  case_id or "case_ASE" in  case_id\
                            or "case_TRE" in case_id:
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
                    if "case_TRS_01"  in case_id or "case_ASE"  in case_id:
                        pass
                    else:
                        self.data[key] = "{}-01-01".format(GetYear)
                elif key == "end_date" or  key == "edate" or key == "date_end" or key == "statistical_date":
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

    def case_ALL(self, data_storage=None):
        """所有"""
        try:
            case_id = self.inData["case_id"]
            """
            需要传入表格用来
            """
            if "case_PD_01" in case_id:
                self.request_file = {'file':('03-培训记录导入-有在职记录.xlsx',open(file_path_06,"rb"),file_type)}
            if "case_PD_04" in case_id:
                self.request_file = {'file':('01-四川在职人员导入模板.xlsx',open(file_path_03,"rb"),file_type)}
            if "case_PD_05" in case_id:
                self.request_file = {'file':('04-四川离职人员导入模板.xlsx',open(file_path_04,"rb"),file_type)}
            if "case_PIQ_04" in case_id:
                self.request_file = {'file':('02-入职批量查询.xlsx',open(file_path_02,"rb"),file_type)}
            """
            接口依赖
            """
            if "case_TPC_03" in case_id:
                TPC = data_storage["case_TPC_02"]["data"]
                self.data["auth_type"] =TPC["auth_type"]
                self.data["kw_id_number"] =TPC["id_number"]
                self.data["kw_name"] =TPC["name"]
            elif "case_PIQ_06" in case_id:
                PIQ = data_storage["case_PIQ_01"]["data"]
                self.data["id"]  =PIQ["member_id"]
            elif "case_TRE_04" in case_id:
                TRE = data_storage["case_TRE_02"]["data"]
                self.data["id"] =TRE["id"]
            elif "case_PIQ_05" in case_id:
                PIQ = data_storage["case_PIQ_04"]["data"]
                self.data["id_number_array"] =PIQ
            elif "case_PIC_04" in case_id:
                PIC = data_storage["case_PIC_01"]["data"]
                self.data["id"]  = int(PIC["id"])
                self.data["member_id"]  = PIC["member_id"]
            elif "case_MFS_03" in case_id:
                MFS = data_storage["case_PIC_01"]["data"]
                self.data["id"]  = int(MFS["id"])
                self.data["departure_date"] ==date_YmdHMS(4)
            elif "case_AM_12" in case_id or "case_AM_09" in case_id or "case_AM_10" in case_id \
                    or "case_AM_11" in case_id:
                AM = data_storage["case_AM_05"]["data"]
                self.data["ids"].append(int(AM["id"]))
            elif "case_AM_08" in case_id:
                AM = data_storage["case_AM_05"]["data"]
                self.data["id"]=int(AM["id"])
            elif "case_H5_03" in case_id:
                H5 = data_storage["case_H5_02"]["data"]
                self.data["p"] = "{}=".format(H5["data"]["qrcode"].split("=")[1])
            elif "case_HP_09" in case_id:
                HP = data_storage["case_HP_07"]["data"]
                self.data["member_id"] = HP["member_id"]
            elif "case_PD_03" in case_id:
                HP = data_storage["case_PD_02"]["data"]
                new_list=[]
                for key in range(int(len(HP["data"]["list"]))):
                    if HP["data"]["list"][key]["class_name"] == "审核数据20138":
                        new_list.append(HP["data"]["list"][key]["id"])
                self.data["ids"] = new_list
            """
            请求接口;是否上传文件
            """
            if "case_PD_01" in case_id or "case_PD_04" in case_id or "case_PD_05" in case_id or "case_PIQ_04" in case_id:
                body = requests.post(url=self.new_url,headers=self.header,data=self.data,files=self.request_file)
            else:
                body = requests.post(url=self.new_url,headers=self.header,json=self.data)
            """
            获取需要的数据,用于接口依赖部分
            """
            if "case_HP_07" in case_id:
                data_storage["case_HP_07"] = {}
                data_storage["case_HP_07"]["data"] = body.json()["data"]["list"][0]
            elif "case_TPC_02" in case_id:
                data_storage["case_TPC_02"] = {}
                data_storage["case_TPC_02"]["data"] =body.json()["data"]["list"][0]
            elif "case_PIQ_01" in case_id:
                data_storage["case_PIQ_01"] = {}
                data_storage["case_PIQ_01"]["data"] =body.json()["data"]["list"][0]
            elif "case_TRE_02" in case_id:
                data_storage["case_TRE_02"]={}
                data_storage["case_TRE_02"]["data"] =body.json()["data"]["list"][0]
            elif "case_PIQ_04" in case_id:
                data_storage["case_PIQ_04"]={}
                data_storage["case_PIQ_04"]["data"] =body.json()["data"]
            elif "case_PIC_01" in case_id:
                data_storage["case_PIC_01"]={}
                data_storage["case_PIC_01"]["data"] =body.json()["data"]["list"][0]
            elif "case_AM_05" in case_id:
                data_storage["case_AM_05"]={}
                data_storage["case_AM_05"]["data"] =body.json()["data"]["list"][0]
            elif "case_H5_02" in case_id:
                data_storage["case_H5_02"]={}
                data_storage["case_H5_02"]["data"] =body.json()
            elif "case_PD_02" in case_id:
                data_storage["case_PD_02"]={}
                data_storage["case_PD_02"]["data"] =body.json()
        except BaseException:
            traceback.print_exc()
            self.data["actual_result"] = traceback.format_exc()
        finally:
            print(self.inData["case_id"]+"-"+self.inData["case_name"])
            # print(self.new_url)
            # print(self.header)
            # print(self.data)
            # print(body.json())
            #print("\n")
            inData = update_data(self.inData,self.data,self.new_url,self.header,body.json(),json.loads(self.inData["response_expect_result"]),self.conftest)
            return inData,body
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

from tools.Base import *
class all:
    """
    所有模块
    # print(self.inData["case_id"]+"-"+self.inData["case_name"])
    # print(self.new_url)
    # print(self.header)
    # print(self.data)
    # print(body.json())
    # print("\n")
    """
    def __init__(self,association_token,association_company_id, #协会token、公司id
                        province_token,province_company_id,     #省公司token、公司id
                        inData,GetYear,                         #表格数据、当前年份
                        conftest=True):
        self.proxies = {"https":"http://127.0.0.1:8888"}
        self.inData = inData
        self.new_url= url+inData["url"]
        self.data = json.loads(inData["params"])
        self.conftest=conftest
        self.token = association_token
        self.company=association_company_id
        self.GetYear = GetYear
        self.province_token = province_token
        #根据接口不同选择不同的token  省协会 省公司
        if "case_PD_01" in inData["case_id"]\
                or "case_PS_02"in inData["case_id"]:
            self.header = {"Cookie":"{0}".format(province_token)}
        else:
            self.header = {"Cookie":"{0}".format(association_token)}
        #替换字段
        if "case" in self.inData["case_id"]:
            for key  in self.data:
                if key == "company_id":
                    if "case_PS_02" in  self.inData["case_id"]:
                        self.data["company_id"] = province_company_id
                    else:
                        self.data["company_id"] = association_company_id
                elif key == "plan_year":
                    self.data["plan_year"] = GetYear
                elif key == "training_year":
                    self.data["training_year"] = GetYear
                elif key == "start_date":
                    self.data["start_date"] = "{}-01-01".format(GetYear)
                elif key == "end_date":
                    self.data["end_date"] = "{}".format(date_YmdHMS(4))
                elif key == "date":
                    if "case_HP_04" in self.inData["case_id"] or "case_HP_05" in self.inData["case_id"]:
                        print("请求参数 date不替换")
                    else:
                        self.data["date"][0] = "{}-01-01".format(GetYear)
                        self.data["date"][1] = "{}".format(date_YmdHMS(4))

    def case_ALL(self):
        """处理文件上传；依赖接口"""
        try:
            #上传文件参数;接口依赖
            if "case_PD_01" in self.inData["case_id"]:
                self.request_file = {'file':('05四川培训记录汇总表导入模板(寿险).xlsx',open(file_path_06,"rb"),"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            if "case_PD_03" in self.inData["case_id"]:
                data = requests_zzl("PD_02",self.token,self.company,self.GetYear)
                print(data)
                new_list=[]
                for key in range(int(len(data["data"]["list"]))):
                    print(data["data"]["list"][key]["class_name"])
                    if data["data"]["list"][key]["class_name"] == "审核数据20138":
                        new_list.append(data["data"]["list"][key]["id"])
                self.data["ids"] = new_list
            #请求参数是否上传文件
            if "case_PD_01" in self.inData["case_id"]:
                body = requests.post(url=self.new_url,headers=self.header,data=self.data,files=self.request_file)
            else:
                body = requests.post(url=self.new_url,headers=self.header,json=self.data)
        except BaseException:
            traceback.print_exc()
            self.data["actual_result"] = traceback.format_exc()
        finally:
            inData = update_data(self.inData,self.data,self.new_url,self.header,body.json(),json.loads(self.inData["response_expect_result"]),self.conftest)
            return inData,body



    def ParameterlessAdjustment(self,company=None,year=None,member_id=None,Index=None,courseId=None,module=None,name_id_number=None,
                                GetMemberTriningOffline_id=None,GetTestDetail_id_name=None,companyId=None,
                                GetListOnJobCurrent_name_id=None,account_nameOrNickName=None,delete_id=None):
        """所有测试用例集合"""
        #替换字段
        if "case_train_type" in self.inData["case_id"]\
            or "case_GetSum" in self.inData["case_id"]\
            or "case_GetDate" in self.inData["case_id"]\
            or "case_GetTrendChart" in self.inData["case_id"]\
            or "case_GetCompanyTypeStatisticsList" in self.inData["case_id"]\
            or "case_GetTypeStatistics" in self.inData["case_id"]\
            or "case_GetPlanList" in self.inData["case_id"]\
            or "case_GetDetailList" in self.inData["case_id"]:
            self.data["company_id"] = company
            self.data["plan_year"] = year
        if "case_GetRecordForMember" in self.inData["case_id"]:
            self.data["member_id"] = member_id
        if "case_GetFrameModuleByCourse" in self.inData["case_id"]:
            self.data["courseId"] = courseId
        if "case_GetFrameItem" in self.inData["case_id"]:
            self.data["courseId"] = courseId
            self.data["module"].append(module)
        if "case_membertraining_GetRecord" in self.inData["case_id"]:
            self.data["company_id"] = company
            self.data["training_year"] = year
            self.data["start_date"] = "{}-01-01".format(year)
            self.data["end_date"] = "{}-12-29".format(year)
            self.data["date"][0] = "{}-01-01".format(year)
            self.data["date"][1] = "{}-12-29".format(year)
            if "case_membertraining_GetRecord-02" in self.inData["case_id"]:
                self.data["kw_name"] = name_id_number[0]
            if "case_membertraining_GetRecord-03" in self.inData["case_id"]:
                self.data["kw_id_number"] = name_id_number[1]
        if "case_GetRecordForStudy" in self.inData["case_id"]\
            or "case_GetStatisList" in self.inData["case_id"]\
            or "case_GetMemberTriningOffline_01" in self.inData["case_id"]:
            self.data["company_id"] = company
            self.data["training_year"] = year
            if "case_GetRecordForStudy-02" in self.inData["case_id"]:
                self.data["kw_name"] = name_id_number[0]
            if "case_GetRecordForStudy-03" in self.inData["case_id"]:
                self.data["kw_id_number"] = name_id_number[1]
            if "case_GetMemberTriningOffline_01" in self.inData["case_id"]:
                self.data["created_time"][0] = "{}-01-01".format(year)
                self.data["created_time"][1] = "{}-12-29".format(year)
        if "case_GetImportantRecordForOffline" in self.inData["case_id"]:
            self.data["offline_id"] = GetMemberTriningOffline_id
        if "case_GetTempOfflineFrames" in self.inData["case_id"]:
            self.data["offlineId"] = GetMemberTriningOffline_id
        if "case_GetTestDetai" in  self.inData["case_id"]:
            self.data["company_id"] = company
            self.data["year"] = year
            if "case_GetTestDetail_02" in self.inData["case_id"]:
                self.data["name"] = GetTestDetail_id_name[0]
            if "case_GetTestDetail_03" in self.inData["case_id"]:
                self.data["id_number"] = GetTestDetail_id_name[1]
            if "case_GetTestDetail_04" in self.inData["case_id"]:
                file = file_data+os.sep+"04培训测评批量查询模板.xlsx"
                self.request_file = {'file':('04培训测评批量查询模板.xlsx',open(file,"rb"),"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        if "case_GetCompanyTestSum"  in  self.inData["case_id"]:
            self.data["companyId"] = company
            self.data["year"] = year
        if "case_GetTreeCompanyById_01"  in  self.inData["case_id"]:
            self.data["id"] = companyId
        if "case_GetLiziRecord"  in  self.inData["case_id"]:
            self.data["start_date"] = "{}-01-01".format(year)
            self.data["end_date"] = "{}-12-29".format(year)
            self.data["date"][0] = "{}-01-01".format(year)
            self.data["date"][1] = "{}-12-29".format(year)
            self.data["training_year"] = year
            if "case_GetLiziRecord_02"  in  self.inData["case_id"]:
                 self.data["kw_name"] =GetTestDetail_id_name[0]
            if "case_GetLiziRecord_03"  in  self.inData["case_id"]:
                self.data["kw_id_number"] =GetTestDetail_id_name[1]
        if "case_GetListOnJobCurrentt" in self.inData["case_id"]\
            or "case_GetListEntry_" in self.inData["case_id"]\
            or "case_GetListOnJobNotCurrent_" in self.inData["case_id"]\
            or "case_GetListDepartureNotCurrent_" in self.inData["case_id"]   :
            self.data["company_id"] =company
            self.data["company"].append(company)
        if "case_memberpracticefiling_list_" in self.inData["case_id"]\
                or "case_statistics_" in self.inData["case_id"]\
                or "case_adminuserList_" in self.inData["case_id"]:
             self.data["companyId"] =company
        if "case_companyimportauditGetList_"  in  self.inData["case_id"]:
            self.data["year"] = year
        if "case_adminuserAdd_" in self.inData["case_id"]:
            self.data["companyId"] =company
            if "case_adminuserAdd_02" in self.inData["case_id"]:
                self.data["name"] = account_nameOrNickName[0]
                self.data["nickName"] = account_nameOrNickName[1]
        if "case_adminuserDelete_01" in self.inData["case_id"]:
            data=ExcelData("case_adminuserList_01")[0]
            json_s =json.loads(data["params"])
            json_s["companyId"] = company
            res = requests.post(url=url+data["url"],json=json_s,headers=self.header).json()
            del_list = []
            for x in range(int(len(res["data"]["list"]))):
                name = res["data"]["list"][x]["name"]
                nickName = res["data"]["list"][x]["nickName"]
                if  name!=None  or nickName!=None:
                    if "denghuidenghui"==name and  "denghuidenghui"==nickName:
                        del_list.append(res["data"]["list"][x]["id"])
            self.data["ids"]=del_list
        if "case_adminuserUpdate_01" in self.inData["case_id"]:
            data=ExcelData("case_adminuserList_01")[0]
            json_s =json.loads(data["params"])
            json_s["companyId"] = company
            res = requests.post(url=url+data["url"],json=json_s,headers=self.header).json()
            print(res)
            del_list = ""
            for x in range(int(len(res["data"]["list"]))):
                name = res["data"]["list"][x]["name"]
                nickName = res["data"]["list"][x]["nickName"]
                if  name!=None  or nickName!=None:
                    if "denghuidenghui"==name and  "denghuidenghui"==nickName:
                        del_list=res["data"]["list"][x]["id"]
            self.data["id"]=del_list

        #导入模板操作
        if "case_EntryImport" in self.inData["case_id"]\
            or "case_BatchList_01" in self.inData["case_id"]\
            or "case_DepartureImport_01" in self.inData["case_id"]:
            if "case_EntryImport_01" in self.inData["case_id"]:
                file = file_data+os.sep+"02四川在职人员导入模板.xlsx"
            if "case_BatchList_01" in self.inData["case_id"]:
                file = file_data+os.sep+"01入职前诚信级别批量查询模板.xlsx"
            if "case_DepartureImport_01" in self.inData["case_id"]:
                file = file_data+os.sep+"03四川离职人员导入模板.xlsx"
            self.request_file = {'file':('01入职前诚信级别批量查询模板.xlsx',open(file,"rb"),"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}

        #接口请求;更新inData的数据;并生成allure报告
        if "case_GetTestDetail_04" in self.inData["case_id"]\
            or "case_EntryImport" in self.inData["case_id"]\
            or "case_BatchList_01" in self.inData["case_id"]\
            or "case_DepartureImport_01" in self.inData["case_id"]:
            body = requests.post(url=self.new_url,headers=self.header,data=self.data,files=self.request_file)
        else:
            body = requests.post(url=self.new_url,headers=self.header,json=self.data)
        print(self.inData["case_id"]+"-"+self.inData["case_name"])
        print(self.new_url)
        print(self.header)
        print(self.data)
        print(body.json())
        print("\n")
        inData = update_data(self.inData,self.data,self.new_url,self.header,body.json(),json.loads(self.inData["response_expect_result"]),self.conftest)
        return inData,body






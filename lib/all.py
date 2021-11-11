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

from tools.Base import *
class all:

    """
    所有模块
    """
    def __init__(self,token,inData,conftest=True):
        self.header = {"Cookie":"{0}".format(token)}
        self.proxies = {"https":"http://127.0.0.1:8888"}
        self.inData = inData
        self.new_url= url+inData["url"]
        self.data = json.loads(inData["params"])
        self.conftest=conftest

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
            or "case_GetDetailLis" in self.inData["case_id"]:
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
                file = file_data+os.sep+"培训测评批量查询模板.xlsx"
                self.request_file = {'file':('培训测评批量查询模板.xlsx',open(file,"rb"),"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
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
            self.data["ids"]=delete_id

        #导入模板操作
        if "case_EntryImport" in self.inData["case_id"]\
            or "case_BatchList_01" in self.inData["case_id"]\
            or "case_DepartureImport_01" in self.inData["case_id"]:
            if "case_EntryImport_01" in self.inData["case_id"]:
                file = file_data+os.sep+"四川在职人员导入模板.xlsx"
            if "case_BatchList_01" in self.inData["case_id"]:
                file = file_data+os.sep+"入职前诚信级别批量查询模板.xlsx"
            if "case_DepartureImport_01" in self.inData["case_id"]:
                file = file_data+os.sep+"四川离职人员导入模板.xlsx"
            self.request_file = {'file':('入职前诚信级别批量查询模板.xlsx',open(file,"rb"),"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}

        #接口请求;更新inData的数据;并生成allure报告
        if "case_GetTestDetail_04" in self.inData["case_id"]\
            or "case_EntryImport" in self.inData["case_id"]\
            or "case_BatchList_01" in self.inData["case_id"]\
            or "case_DepartureImport_01" in self.inData["case_id"]:
            body = requests.post(url=self.new_url,headers=self.header,data=self.data,files=self.request_file)
        else:
            body = requests.post(url=self.new_url,headers=self.header,json=self.data)
        print("初始化参数；company={0}；year={1}；member_id={2}；Index={3}；courseId={4}；module={5},name_id_number={6},GetMemberTriningOffline_id={7},GetTestDetail_id_name={8},companyId={9},GetListOnJobCurrent_name_id={10},account_nameOrNickName={11},delete_id={12}"
              .format(company,year,member_id,Index,courseId,module,name_id_number,GetMemberTriningOffline_id,GetTestDetail_id_name,companyId,GetListOnJobCurrent_name_id,account_nameOrNickName,delete_id))
        print(self.inData["case_id"]+"-"+self.inData["case_name"])
        print(self.new_url)
        print(self.header)
        print(self.data)
        print(body.json())
        print("\n")
        inData = update_data(self.inData,self.data,self.new_url,self.header,body.json(),json.loads(self.inData["response_expect_result"]),self.conftest)
        return inData,body
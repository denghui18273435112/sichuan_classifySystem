import pytest
from tools.ExcelData import ExcelData
import allure
from tools.caseCheck import caseCheck
from lib.all import all
import requests
import json

def setup_module():
    allure.attach(body="TEST-01", name="所有用例执行前，执行一次", attachment_type=allure.attachment_type.TEXT)
def teardown_module():
    #清空导入数据
    allure.attach(body="TEST-06", name="所有用例执行完，执行一次", attachment_type=allure.attachment_type.TEXT)
    #登录
    data = {"type":"I","Name":"admin","Vcode":"denghui","Pwd":"c6c861c435a1e98caba3bf1cd594c48f"}
    url = "http://sc.maintain.giiatop.com/base/home/Login"
    header = {"Content-Type": "application/json"}
    body = requests.post(url=url,json=data,headers=header)
    token = "{0}={1}".format("sc.maintain.token",body.cookies["sc.maintain.token"])
    allure.attach(body=token, name="登录后拼接的token", attachment_type=allure.attachment_type.TEXT)

    #身份证查询个人信息 删除
    for x in ["431225199212061818","431226199009250134","431226199009250150","431226199009250177","431226199009250193","440101198803123654"]:
        url1 = "http://sc.maintain.giiatop.com/api/member/DeleteMember"
        data1= {"idNumber":"{}".format(x)}
        header1 = {"Cookie":token}
        body1 = requests.post(url=url1,json=data1,headers=header1)
        body1.json()
        allure.attach(body=json.dumps(body1.json()), name="身份证查询个人信息查询返回的数据", attachment_type=allure.attachment_type.TEXT)

    #获取列表档案信息档案
    url2 = "http://sc.maintain.giiatop.com/api/member/GetMemberTriningOffline"
    data2= {"year":2022,"className":"","pageNum":1,"pageSize":20,"total":5,"createdTime":[]}
    header2 = {"Cookie":token}
    body2 = requests.post(url=url2,json=data2,headers=header2)
    body2.json()
    allure.attach(body=json.dumps(body2.json()), name="获取档案的列表数据", attachment_type=allure.attachment_type.TEXT)

    #获取需要删除的数据id
    delete_id = []
    len_s= body2.json()["data"]["list"]
    for x  in range(len(len_s)):
        if  len_s[x]["className"] == "审核数据20138":
            delete_id.append(len_s[x]["id"])

    #删除档案数据
    for x  in delete_id:
        url3 = "http://sc.maintain.giiatop.com/api/home/TrainingClear"
        data3= {"ids":[x]}
        header3 = {"Cookie":token}
        body3 = requests.post(url=url3,json=data3,headers=header3)
        body3.json()
        allure.attach(body=json.dumps(body3.json()), name="删除档案数据", attachment_type=allure.attachment_type.TEXT)

@allure.epic("四川分类系统")
class Test_all(object):

    #@pytest.mark.skip
    @pytest.mark.run(order=1001)
    @pytest.mark.parametrize("inData",ExcelData("case_ED"))
    def test_ED(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """essential data（基础数据）"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1002)
    @pytest.mark.parametrize("inData",ExcelData("case_PD_"))
    def test_PD(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """preposition data（前置数据）"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1003)
    @pytest.mark.parametrize("inData",ExcelData("case_HP"))
    def test_HP(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """home page(首页)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1004)
    @pytest.mark.parametrize("inData",ExcelData("case_PS"))
    def test_PS(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Plan  submit(培训计划报送)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1005)
    @pytest.mark.parametrize("inData",ExcelData("case_TRI"))
    def test_TRI(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Training record import(培训记录导入)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1006)
    @pytest.mark.parametrize("inData",ExcelData("case_TRE"))
    def test_TRE(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Training Record Enquiry(培训记录查询)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1007)
    @pytest.mark.parametrize("inData",ExcelData("case_TCI"))
    def test_TCI(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Training Credit Inquiry(培训学分查询)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1008)
    @pytest.mark.parametrize("inData",ExcelData("case_TRS"))
    def test_TRS(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Training Record statistics(培训记录统计)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1009)
    @pytest.mark.parametrize("inData",ExcelData("case_Trecords"))
    def test_Trecords(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Training records(培训档案管理)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1010)
    @pytest.mark.parametrize("inData",ExcelData("case_TE"))
    def test_TE(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Training evaluation(培训测评)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1011)
    @pytest.mark.parametrize("inData",ExcelData("case_TPC"))
    def test_TPC(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Third Party company(第三方公司)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1012)
    @pytest.mark.parametrize("inData",ExcelData("case_PIQ"))
    def test_PIQ(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Personal Information Query(个人信息查询)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1013)
    @pytest.mark.parametrize("inData",ExcelData("case_PIC"))
    def test_PIC(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Personal information correction(个人信息修正)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1014)
    @pytest.mark.parametrize("inData",ExcelData("case_PCIT"))
    def test_PCIT(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Practice certificate import tracking(执业证导入追踪)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1015)
    @pytest.mark.parametrize("inData",ExcelData("case_IPM"))
    def test_IPM(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """In-service personnel management(在职人员管理)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])



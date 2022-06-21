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
    for x in ["431226198011280012",
                "431226198011280039",
                "431226198011280055",
                "431226198011280071",
                "431226198011280098",
                "431226198011280119",
                "431226198011280135",
                "431226198011280151",
                "431226198011280178",
                "431226198011280194",
                "120619860916001X",
                "1206198609160036",
                "1206198609160052",
                "1206198609160079",
                "1206198609160095",
                "1206198609160116",
                "1206198609160132",
                "1206198609160159",
                "1206198609160175",
                "1206198609160191"]:
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

    @pytest.mark.run(order=1001)
    @pytest.mark.parametrize("inData",ExcelData("case_ED"))
    def test_ED(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """essential data（基础数据）"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

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

    # #@pytest.mark.skip
    # @pytest.mark.run(order=1005)
    # @pytest.mark.parametrize("inData",ExcelData("case_TRI"))
    # def test_TRI(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
    #     """Training record import(培训记录导入)"""
    #     res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
    #     caseCheck().case_Check(res[0])

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

    #@pytest.mark.skip
    @pytest.mark.run(order=1016)
    @pytest.mark.parametrize("inData",ExcelData("case_MFS"))
    def test_MFS(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Management of former staff(离职人员管理)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1017)
    @pytest.mark.parametrize("inData",ExcelData("case_ESE"))
    def test_ESE(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Entry staff enquiries(入职人员查询)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1018)
    @pytest.mark.parametrize("inData",ExcelData("case_ASE"))
    def test_ASE(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Active Staff Enquiries(在职人员查询)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1019)
    @pytest.mark.parametrize("inData",ExcelData("case_FSE"))
    def test_FSE(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Former Staff Enquiries(离职人员查询)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1020)
    @pytest.mark.parametrize("inData",ExcelData("case_FPR"))
    def test_FPR(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Filing of Practice Record(执业备案报送)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1021)
    @pytest.mark.parametrize("inData",ExcelData("case_PRIS"))
    def test_PRIS(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Practice record information statistics(执业备案报送统计)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1022)
    @pytest.mark.parametrize("inData",ExcelData("case_IP"))
    def test_IP(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Import Permission Management(导入权限管理)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1023)
    @pytest.mark.parametrize("inData",ExcelData("case_IP"))
    def test_IP(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """Import Permission Management(导入权限管理)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1024)
    @pytest.mark.parametrize("inData",ExcelData("case_AM"))
    def test_IP(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """account management (账号管理)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1025)
    @pytest.mark.parametrize("inData",ExcelData("case_H5"))
    def test_H5(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """H5(单独的H5查询页面)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1026)
    @pytest.mark.parametrize("inData",ExcelData("case_evaluation"))
    def test_evaluation(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """evaluation(移动端测评)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1027)
    @pytest.mark.parametrize("inData",ExcelData("case_GTOHNQ"))
    def test_GTOHNQ(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """case_GTOHNQ(历史未完成职业培训)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1028)
    @pytest.mark.parametrize("inData",ExcelData("case_AS"))
    def test_AS(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """case_AS(各类人数汇总统计)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1029)
    @pytest.mark.parametrize("inData",ExcelData("case_CR"))
    def test_CR(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """case_CR(课程报备审核)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])

    #@pytest.mark.skip
    @pytest.mark.run(order=1030)
    @pytest.mark.parametrize("inData",ExcelData("case_CCR_"))
    def test_CCR(self,association_token,association_company_id,province_token,province_company_id,inData,GetYear):
        """case_CCR_(课程报备提交)"""
        res =all(association_token,association_company_id,province_token,province_company_id,inData,GetYear).case_ALL()
        caseCheck().case_Check(res[0])
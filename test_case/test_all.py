import pytest
from tools.ExcelData import ExcelData
import allure
from tools.caseCheck import caseCheck
from lib.all import all

@allure.epic("山东分类系统")
class Test_all(object):

    @pytest.mark.parametrize("Data",ExcelData("case"))
    def test_ParameterlessAdjustment(self,token,Data,GetYear,company,member_id,Index,courseId,module,name_id_number,GetMemberTriningOffline_id,
                                     GetTestDetail_id_name,companyId,GetListOnJobCurrent_name_id):
        """所有测试用例集合"""
        res =all(token,Data).ParameterlessAdjustment(year=GetYear,company=company,
                member_id=member_id,Index=Index,courseId=courseId,module=module,name_id_number=name_id_number,GetMemberTriningOffline_id=GetMemberTriningOffline_id,
                GetTestDetail_id_name=GetTestDetail_id_name,companyId=companyId,GetListOnJobCurrent_name_id=GetListOnJobCurrent_name_id)
        caseCheck().case_Check(res[0])
from lib.all import *
from tools.ExcelData import ExcelData
import pytest
from configs.path import *
from tools.commonly_method import *

@pytest.fixture(scope="session",autouse=True)
def empty_report_file():
    """清空report-result文件夹,除environment.properties以外的其它所有文件"""
    try:
        for one in os.listdir(result_path):
            if "environment.properties" not in one:
                os.remove(result_path+os.sep+"{}".format(one))
    except:
        pass

#############################默认传入的5个参数###########################################################################
@pytest.fixture(scope="session")
def association_token():
    """省协会token"""
    return login("login-001")

@pytest.fixture(scope="session")
def province_token():
    """省公司token"""
    return login("login-002")

@pytest.fixture(scope="session")
def association_company_id(association_token):
    """省协会登录账号公司id"""
    return  requests_zzl("case_ED_03",association_token)["data"][0]["id"]

@pytest.fixture(scope="session")
def province_company_id(province_token):
    """省公司登录账号公司id"""
    return  requests_zzl("case_ED_03",province_token)["data"][0]["id"]

@pytest.fixture(scope="session")
def GetYear(association_token):
    """获取最新年份"""
    year = requests_zzl("case_ED_02",association_token)["data"]
    return  year[len(year)-1]
########################################################################################################

@pytest.fixture(scope="session")
def Index(association_token):
    """最核心的接口"""
    return requests_zzl("case_ED_01",association_token)

@pytest.fixture(scope="session")
def company(association_token):
    """某人的人员id"""
    return  requests_zzl("case_ED_03",association_token)["data"][0]["id"]




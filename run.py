#主运行
import pytest
from configs.path import result_path,allure_reportt_path
import os
if __name__ == '__main__':
    a =True
    if a==True:
        pytest.main(["-s","test_case","--alluredir", result_path])
    elif a==False:
        pytest.main(["-s","test_case/test_all.py","--alluredir", result_path])
    os.system("allure generate {0} -o {1} --clean".format(result_path, allure_reportt_path))
    # os.system("allure serve {}".format(result_path))




#主运行
import pytest
from configs.path import result_path,allure_reportt_path
import socket
import os
if __name__ == '__main__':
    pytest.main(["-s","test_case","--alluredir", result_path])
    compute_name = socket.getfqdn(socket.gethostname())
    print(os.path.dirname(os.path.abspath(__file__)))
    if os.path.dirname(os.path.abspath(__file__))=="G:\pycharm\script\sichuan_classifySystem":
        os.system("allure generate {0} -o {1} --clean".format(result_path, allure_reportt_path))
        #os.system("allure serve {}".format(result_path))



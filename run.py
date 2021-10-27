#主运行
import pytest
from configs.path import result_path,allure_reportt_path
import socket
import os
if __name__ == '__main__':
    pytest.main(["-s","test_case","--alluredir", result_path])
    compute_name = socket.getfqdn(socket.gethostname())
    if compute_name == "SZPC065.zzldomain.com" or socket.gethostbyname(compute_name) == "192.168.1.66":
        os.system("allure generate {0} -o {1} --clean".format(result_path, allure_reportt_path))
        #os.system("allure serve {}".format(result_path))


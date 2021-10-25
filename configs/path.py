#-*- conding:utf-8 -*-
#@File      :path.py
#@Time      : 14:32
#@Author    :denghui
#@Email     :314983713@qq.com
#@Software  :PyCharm
import os
current =os.path.abspath(__file__)                          #当前文件的路径
BASE_DIR = os.path.dirname(os.path.dirname(current))        # 当前项目的绝对路径

#文件夹路径
config_path = BASE_DIR +os.sep+"config"
log_path = BASE_DIR +os.sep+"logs"
data_path =BASE_DIR +os.sep+"docs"
file_path =BASE_DIR +os.sep+"file"
report_path =BASE_DIR +os.sep+"report"
testcase_path =BASE_DIR +os.sep+"test_case"
file_data =BASE_DIR +os.sep+"data"
result_path = report_path+os.sep+"result"
allure_reportt_path = report_path+os.sep+"allure_report"
screenshots_path = file_path+os.sep+"screenshots"

#文件路径
_config_file = config_path +os.sep+"conf.yaml"            #定义conf.yaml的路径
_yonglie_file = config_path +os.sep+"yonglie.yaml"            #定义conf.yaml的路径
_db_config_file = config_path +os.sep+"db_conf.yaml"     #定义db_conf.yaml的路径
test_xlsx = data_path+os.sep+"ctest.xlsx"
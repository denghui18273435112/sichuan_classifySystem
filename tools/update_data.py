#-*- conding:utf-8 -*-
#@File      :update_data.py
#@Time      : 10:42
#@Author    :denghui
#@Email     :314983713@qq.com
#@Software  :PyCharm
from tools.allureUitl import alluer_new

def update_data(inData,params,URL,params_type,actual_result,response_expect_result,conftest=None):
    """
    更新inData的数据;并生成allure报告
    :param inData:表格中读取的inData数据
    :param params:请求参数
    :param URL:URL
    :param params_type: 请求头header
    :param actual_result: 请求响应
    :param response_expect_result:预期结果
    :param conftest: 用于标识调用的位置；主要用于区分conftest文件调用
    :return:
    """
    inData["params"] = params
    inData["URL"] = URL
    inData["params_type"] = params_type
    inData["actual_result"] = actual_result
    inData["response_expect_result"] =response_expect_result
    if conftest ==True:
        alluer_new(inData)
    return inData
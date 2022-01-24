# coding=utf-8
import pprint
from datetime import datetime
import allure
from configs.conf import *

def alluer_new(inData):
        """allure报告自定义拼接"""
        allure.dynamic.feature(inData["case_model"])
        allure.dynamic.story(inData["case_name"]+"-\n-"+inData["title"])
        desc = "<font color='red'>当前执行时间: </font> {}<Br/>" \
                "<font  color='red'>用例编号: </font> {}<Br/>" \
               "<font color='red'>模块: </font>{}<Br/>" \
                "<font color='red'>接口名称: </font>{}<Br/>" \
                "<font color='red'>优先级: </font>{}<Br/>" \
               "<font color='red'>标题: </font>{}<Br/>" \
               "<font color='red'>URL: </font>{}<Br/>"\
                "<font color='red'>前置条件: </font>{}<Br/>"\
                "<font color='red'>请求方式: </font>{}<Br/>" \
               "<font color='red'>请求参数: </font>{}<Br/>" \
               "<font color='red'>预期结果的状态: </font>{}<Br/>"\
                "<font color='red'>表格-响应预期结果: </font>{}<Br/>"\
                "<font color='red'>备注信息: </font>{}<Br/>"\
                "<font color='red'>请求头: </font>{}<Br/>" \
                "<font color='red'>接口请求-实际结果: </font>{}<Br/>"\
            .format(
                    str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    inData["case_id"],
                    inData["case_model"],
                    inData["case_name"],
                    inData["priority"],
                    inData["title"],
                    url+inData["url"],
                    inData["pre_exec"],
                    inData["method"],
                    pprint.pformat(inData["params"]),
                    inData["expect_result"],
                    pprint.pformat(inData["response_expect_result"]),
                    inData["remark"],
                    pprint.pformat(inData["params_type"]),
                    pprint.pformat(inData["actual_result"])

                    )
        allure.dynamic.description(desc)


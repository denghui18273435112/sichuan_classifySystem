import jsonpath
import traceback
import allure
class caseCheck:
    def case_Check(self,res=None):
        """校验实际结果与预期结果是否一致或者是否包含
        第一步：先获取表中的数据，以字典方式返回（ "$.data.statistics[*]": 1,）
        第二步：把字典的key取出，与接口响应数据进行数据获取，使用jsonpath提供的方法
        第三步：取出来的jsonpath值与字典值做比较；
        第四步：比较数据支持：列表长度比较、数字大小比较、字符串相同比较"""
        try:
            response_expect_result = res["response_expect_result"] #表格中response_expect_result字段
            actual_result = res["actual_result"] #接口响应数据
            for key in response_expect_result:
                for values in jsonpath.jsonpath(actual_result,key):
                    #列表长度比较
                    if  isinstance(values,list):
                        if len(values) < response_expect_result[key]:
                            assert  True==False,"对比类型列表;系统呈现:{0}>=表格获取:{1};接口校验失败".format(len(values),response_expect_result[key])
                        allure.attach(body="对比类型列表;系统呈现:{0}>=表格获取:{1};".format(len(values),response_expect_result[key]), name="数据对比情况", attachment_type=allure.attachment_type.TEXT)
                    #浮点大小比较
                    elif isinstance(values, float):
                        if values < response_expect_result[key]:
                            assert  True==False,"对比类型浮点;系统呈现:{0}>=表格获取:{1};接口校验失败".format(values,response_expect_result[key])
                        allure.attach(body="对比类型数字;系统呈现:{0}>=表格获取:{1};".format(values,response_expect_result[key]), name="数据对比情况", attachment_type=allure.attachment_type.TEXT)
                    #数字大小比较
                    elif isinstance(values, int):
                        if values < response_expect_result[key]:
                            assert  True==False,"对比类型数字;系统呈现:{0}>=表格获取:{1};接口校验失败".format(values,response_expect_result[key])
                        allure.attach(body="对比类型数字;系统呈现:{0}>=表格获取:{1};".format(values,response_expect_result[key]), name="数据对比情况", attachment_type=allure.attachment_type.TEXT)
                    #字符串相同比较
                    else:
                        if values != response_expect_result[key]:
                            assert  True==False,"对比类型字符串;系统呈现:{0}!=表格获取:{1};接口校验失败".format(values,response_expect_result[key])
                        allure.attach(body="对比类型字符串;系统呈现:{0}==表格获取:{1};".format(values,response_expect_result[key]), name="数据对比情况", attachment_type=allure.attachment_type.TEXT)
        except Exception as ERROR_NEW:
            traceback.print_exc()
            raise  ERROR_NEW
# coding=utf-8
from tools.logUtil import my_log


class AssertUitl:
    def __init__(self):
        self.my_log = my_log("AssertUilt")

    def assert_code(self,code,expected_code):
        """
        code 断言
        #预期和实际是否一致;#抛出异常；如果相等返回ture;如果不相等抛出异常
         有关于python里raise显示引发异常的方法:
        当程序出错时,python会自动触发异常,也可以通过raise显示引发异常
        一旦执行了raise语句,raise之后的语句不在执行
        如果加入了try,except,那么except里的语句会被执行
        :param code: 接口请求所返回的状态码
        :param expected_code: 需要对比的状态码
        :return:
        """
        try:
            assert  int(code) == int(expected_code)
            return True
        except:
            self.my_log.error("code error; code is {0},expected_code is {1}".format(code,expected_code))
            raise

    def assert_body(self,body,expected_body):
        """
        验证返回结果内容相等
        :param body:  接口请求所返回的body
        :param expected_body:需要对比的body
        :return:
        """
        try:
            assert  body == expected_body
            return  True
        except:
            self.my_log.error("body error; body is {0},expected_body is {1}".format(body,expected_body))
            raise

    def assert_int_body(self,body,expected_body):
        """
        验证返回结果是否包含
        :param body:            接口请求所返回的body
        :param expected_body:  表格取的需要对比的body
        :return:
        """
        try:
            assert  expected_body in body
            return  True
        except:
            self.my_log.error("不包含或者body错误; 接口请求所返回的bodybody is {0}, 需要对比的bodyexpected_body is {1}".format(body,expected_body))
            raise

    def assert_int_body_dict(self,expected_body,body):
        """
        结果断言验证
        #只接收字典类型数据
        # 验证返回结果 body是否包含expected_body
        # :param body:            接口请求所返回的body
        # :param expected_body:  表格取的需要对比的body
        # :return:
        """
        try:
            count=0
            for body_key in body.keys():
                for expected_body_key in expected_body.keys():
                    if body_key==expected_body_key :
                        if body[body_key]==expected_body[expected_body_key] or expected_body[expected_body_key]=="":
                            count+=1
            assert  len(expected_body)==count
            return  True
        except:
            self.my_log.error("不包含或者body错误; 接口请求所返回的bodybody is {0}, 需要对比的bodyexpected_body is {1}".format(body,expected_body))
            raise


if __name__ == '__main__':

    expected_body= {}
    body=  {'order_id': '20200824063500000000001'}

    AssertUitl().assert_int_body_dict(expected_body,body)




#-*- conding:utf-8 -*-
#@File      :Base.py
#@Time      : 15:36
#@Author    :denghui
#@Email     :314983713@qq.com
#@Software  :PyCharm
import datetime
import json
import os
import  re
import subprocess
from configs.path import  report_path
from tools.YamlUtil import YamlReaber

"""
常用的方式
"""


def time_YmdHMS(YmdHMS=True):
    """
    返回当前时间，支持两个格式
    True：%Y%m%d%H%M%S
    False：%Y%m%d
    :return:current_time
    """
    now_time = datetime.datetime.now()
    if YmdHMS:
        current_time = now_time.strftime("%Y%m%d%H%M%S")
    else:
        current_time = now_time.strftime("%Y%m%d")
    return   current_time




p_data = '\\${(.*)}\\$'
#log = my_log()


#
# def init_db(db_alias='db_1'):
#     """
#     :param db_alias: # 默认db_1  数据库
#     :return: sql的光标对象
#     """
#     db_info = ConfigYaml().get_db_conf_info(db_alias)
#     host  = db_info["db_host"]
#     user  = db_info["db_user"]
#     password  = db_info["db_password"]
#     database  = db_info["db_database"]
#     port  = int(db_info["db_port"])
#     charse  = db_info["db_charset"]
#     conn =  Mysql(host,user,password,database,port,charse)
#     return  conn

def json_parse(data):
    """
    转换json格式
    :param data:需要格式转译格式化字符
    :return: 转译后的数据
    不晓得有啥用
    """
      # 1.判断headers是否存在，json转义，无需
        # if headers:
        #     header = json.loads(headers)
        # else:
        #     header = headers
        #header = Base.json_parse(headers)
        # 3.增加cookies
        # if cookies:
        #     cookie = json.loads(cookies)
        # else:
        #     cookie = cookies
    return json.loads(data) if data else data

def res_find(data,pattern_data=p_data):
    """
    查询
    :param data:需要提取的原数据
    :param pattern_data: 正则表达提取格式
    :return:
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    return re_res

def res_sub(data,replace,pattern_data=p_data):
    """
    替换
    :param data:原内容
    :param replace: 替换内容
    :param pattern_data:正则表达提取格式
    :return: 替换后实际内容
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    if re_res:
        return re.sub(pattern_data,replace,data)
    return re_res

def params_find(headers,cookies):
    """
    验证请求中是否有${}$需要结果关联
    不晓得怎么用
    :param headers:
    :param cookies:
    :return:
    """
    if "${" in headers:
        headers = res_find(headers)
    if "${" in cookies:
        cookies = res_find(cookies)
    return headers,cookies

def allure_report(report_path,report_html):
    """
    自动生成allure 报告
    :param report_path: pytest.main运行 生成文件的存放位置
    :param report_html: allure生成报告存放位置
    :return:
    """
    allure_cmd ="allure generate %s -o %s --clean"%(report_path,report_html)
    try:
        subprocess.call(allure_cmd,shell=True)
        my_log().info("自动生成allure 报告成功")
    except:
        log.error("执行用例失败，请检查一下测试环境相关配置")
        raise

def send_mail(report_html_path="",content="测试",title="测试"):
    """
    自动化发送邮件方法；初始化 发送邮件的相关参数
    :param report_html_path:
    :param content:  邮件内容;默认为测试
    :param title:  邮件标题;默认为测试
    :return:
    """
    email_info = read_yamlFile(level_1="email")
    smtp_addr = email_info["smtpserver"]
    username = email_info["username"]
    password = email_info["password"]
    recv = email_info["receiver"]
    email = SendEmail(                  #初始化 发送邮件的相关参数
        smtp_addr=smtp_addr,            #邮箱的服务器地址
        username=username,              #发送账号
        password=password,              #发送密码 pp3
        recv=recv,                      #接口账号
        title=title,                    #邮件标题
        content=content,                #邮件内容
        file=report_html_path)          #附件
    email.send_mail()

def assert_db(result,db_verify):
    """
    数据库结果断言验证
    数据库比较
    :param db_name:  数据库名称
    :param result:  返回的结果 body
    :param db_verify: sql语句
    :return:
    """
    # print("result输入的内容:"+result)
    # print("db_verify输入的内容:"+db_verify)
    assert_util =  AssertUitl()
    sql = Mysql("211.103.136.242",
                  "test",
                  "test123456",
                  "meiduo",
                  7090,
                  charset="utf8")
    db_res = sql.fetchone(str(db_verify))

    #print("db_verify信息:"+db_verify)
    # for i in db_res:
    #     print(db_res[i])
    #
    # print(type(db_res))

    #log.debug("数据库查询结果：{}".format(str(db_res)))
    # 3、数据库的结果与接口返回的结果验证
    # 获取数据库结果的key
    verify_list = list(dict(db_res).keys())
    # 根据key获取数据库结果，接口结果
    for line in verify_list:
        #res_line = res["body"][line]
        res_line = result[line]
        res_db_line = dict(db_res)[line]
        # 验证
        assert_util.assert_body(res_line, res_db_line)


def Yaml_file_path(Yaml_name, filePath="configs"):
    """
    :param Yaml_name：yaml的文件夹名称
    :param filePath: 默认configs文件夹下
    :return: 返回当前yaml文件的绝对路径+文件名称
    """
    _config_path = Conf.get_FolderPath(filePath)
    return _config_path +os.sep+Yaml_name



def read_yamlFile(yaml_name="conf.yaml",level_1=None, level_2=None,filePath=None,location=None):
    """
    支持yaml的单文档、多文档遍历
    :param yaml_name:  yaml的文件名称
    :param level_1: yaml文件第一级的名称
    :param level_2: yaml文件第二级的名称
    :param filePath:文件夹名称
    :param location:读取多个文档的下标
    :return:   1、支持返回所有的yaml文件；2、第一级下的所有数据；3、固定某位置的值
    """
    if filePath!=None:
        if location!=None:
            login = YamlReaber(Yaml_file_path(yaml_name,filePath)).data_all()
        else:
            login = YamlReaber(Yaml_file_path(yaml_name,filePath)).data()
    else:
        if location!=None:
            login = YamlReaber(Yaml_file_path(yaml_name)).data_all()
        else:
            login = YamlReaber(Yaml_file_path(yaml_name)).data()
    if level_1==None and level_2==None:
        if location!=None:
            return  login[location]
        else:
            return  login
    elif level_1!= None and level_2==None:
        if location!=None:
            return  login[location][level_1]
        else:
            return  login[level_1]
    elif level_1!=None and level_2!=None:
        if location!=None:
            return  login[location][level_1][level_2]
        else:
            return login[level_1][level_2]


def JSON_turn_dict(json_str):
    """
    JSON转字典
    :param JSON:
    :return:
    """
    return json.loads(json_str)

def dict_turn_JSON(dict):
    """
    字典转JSON
    :param dict:
    :return:
    """
    return json.dumps(dict)



if __name__ == '__main__':
    print(read_yamlFile("testlogin.yaml","data","password",filePath="data"))
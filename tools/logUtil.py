import logging
from tools import Base
from configs.Conf import *
import datetime
import time

class Logger:
    def __init__(self,log_file,log_Logger_name,log_level):                 #2定义参数；想想需要有哪些參數；生成日志文件名称、Logger名称、日志级别
        self.log_file = log_file                                            #扩展名；在配置文件写
        self.log_Logger_name = log_Logger_name                              #Logger名称，不在配置文件写
        self.log_level = log_level                                          #日志级别；在配置文件写
        log_l={"info":logging.INFO,"debug":logging.DEBUG,                    #定义日志级别的映射
               "warning":logging.WARNING,"error":logging.ERROR}

        #输入到日志文件中
        self.logger_name = logging.getLogger(self.log_Logger_name)                      #第一步：设置logger名称
        self.logger_name.setLevel(log_l[self.log_level])                                #第二步：设置log级别
        fh_file = logging.FileHandler(self.log_file,encoding='utf-8')                   #第三步：写入文件的handler
        fh_file.setLevel(log_l[self.log_level])                                         #第四步：设置日志级别
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        fh_file.setFormatter(formatter)                                                 #第五步：定义格式
        self.logger_name.addHandler(fh_file)                                            #第六步：添加handler

        #输出控制台
        self.logger = logging.getLogger(self.log_Logger_name)
        self.logger.setLevel(log_l[self.log_level])
        fh_stream = logging.StreamHandler()
        fh_stream.setLevel(log_l[self.log_level])
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s ')
        fh_stream.setFormatter(formatter)
        self.logger.addHandler(fh_stream)

def generate_file():
    """
    在logs文件夹下生成以时间命名的.log日志
    1 #日志存放的文件夹 G:\pycharm\script\api_frame\logs
    2 #生成时间          20200407
    3 #获取日志文件的后缀 .log
    :return:  合并（log目录+当前时间+扩展名）并创建*.log文件,生成的日志文件名称
    """
    log_path = get_logs_path()
    current_time = Base.time_YmdHMS(YmdHMS=True)
    log_extensiong = Base.read_yamlFile("conf.yaml","LOG","log_extensiong")
    return os.path.join(log_path,current_time+log_extensiong)

def my_log(log_Logger_name = __file__):
    """
    生成日志
    :param log_Logger_name: log名称
    :return
        log_file            日志文件名称
        log_level           日志文件级别
        log_Logger_name     日志文件打印部分
        logger_name         logger名称
    """
    return Logger(log_file=generate_file(),
                  log_Logger_name=log_Logger_name,
                  log_level=Base.read_yamlFile("conf.yaml", "LOG", "log_level")
                  ).logger_name

def logger(name=__name__):# __name__  当前模块名
    #1- 日志的名称：路径+名字(时间)+后缀名(.log)
    logName = "{0}/{1}.log".format(get_logs_path(),datetime.datetime.now().strftime('%Y%m%d%H%M'))
    #2- 创建日志对象
    logObject = logging.getLogger(name)
    #3- 日志级别
    logObject.setLevel(logging.INFO)
    #4- 封装日志的属性
    rHandler = logging.FileHandler(logName,mode='w',encoding='utf-8')
    #5- 日志内容格式
    #时间 等级 文件名[代码报错行号] 信息
    formater = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[%(lineno)d]: %(message)s")
    rHandler.setFormatter(formater)
    logObject.addHandler(rHandler)
    return logObject




if __name__ == '__main__':
    #my_log().info("邮件发送成功")
     #print(time.time())
    #print(datetime.datetime.now())#当前时间
    # print(datetime.datetime.now().strftime('%Y%m%d%H%M'))  # 当前时间--设置格式
    log = logger()
    log.info("调试信息！")






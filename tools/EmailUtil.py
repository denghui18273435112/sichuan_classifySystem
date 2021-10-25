import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tools.logUtil import *
from tools import Base

class SendEmail:
    def __init__(self,smtp_addr,username,password,recv,
                 title,content=None,file=None):
        """
        :param smtp_addr: smtp地址
        :param username: 用户名
        :param password: 密码
        :param recv: 接收邮件者
        :param title: 邮件标题
        :param content: 邮件内容
        :param file: 邮件附件
        :return:
        """
        self.smtp_addr = smtp_addr
        self.username = username
        self.password = password
        self.recv = recv
        self.title = title
        self.content = content
        self.file = file

    def send_mail(self):
        """
        发送邮件方法
        :return:
        """
        msg = MIMEMultipart()                                                   #MIME
        msg.attach(MIMEText(self.content,_charset="utf-8"))                     #初始化邮件信息
        msg["Subject"] = self.title                                             #标题
        msg["From"] = self.username                                             #发送者账号
        msg["To"] = self.recv                                                   #接受者
        if self.file:                                                           #判断是否附件  #邮件附件
            att = MIMEText(open(self.file).read())                              #MIMEText读取文件
            att["Content-Type"] = 'application/octet-stream'                    #设置内容类型
            att["Content-Disposition"] = 'attachment;filename="%s"'%self.file   #设置附件头
            msg.attach(att)                                                     #将内容附加到邮件主体中
        self.smtp = smtplib.SMTP(self.smtp_addr,port=25)                        #登录邮件服务器
        self.smtp.login(self.username,self.password)
        self.smtp.sendmail(self.username,self.recv,msg.as_string())             #发送邮件
        my_log().info("邮件发送成功")


if __name__ == "__main__":
    email_info = Base.read_yamlFile("conf.yaml","email")
    smtp_addr = email_info["smtpserver"]
    username = email_info["username"]
    password = email_info["password"]
    recv = email_info["receiver"]
    content = "邮件发送内容"+Base.time_YmdHMS()
    SendEmail(smtp_addr,username,password,recv,content).send_mail()





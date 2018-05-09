# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/7 14:57
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : configEmail.py
# @Software: PyCharm
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import threading
from socket import gaierror, error
from utils import configBase
from utils.configBase import Config
from utils.log import logger, MyLog
import zipfile
import glob


class Email:
    def __init__(self):
        '''
        初始化email
        '''
        config = Config().get('email')
        self.server = config.get('email_server', 2)
        self.sender = config.get('email_sender', 2)
        self.password = config.get('email_password', 2)
        self.content = config.get('email_content', 2)

        # 邮件收件人列表
        self.receiver = config.get('email_receiver', 2)

        # 邮件主题
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = config.get('email_subject', 2) + " " + date

        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.msg = MIMEMultipart('related')

    def config_header(self):
        """
        配置邮件头：主题，发件人，收件人
        :return:
        """
        self.msg['subject'] = self.subject
        self.msg['from'] = self.sender
        self.msg['to'] = self.receiver

    def config_content(self):
        """
        设置邮件主题
        :return:
        """
        f = open(configBase.EMAIL_STYLE)
        content = f.read()
        f.close()
        content_plain = MIMEText(content, 'html', 'UTF-8')
        self.msg.attach(content_plain)
        self.config_image()

    def config_image(self):
        """
        配置邮件正文中的图片
        :return:
        """
        # defined image path
        image1_path = configBase.EMAIL_IMAGE
        fp1 = open(image1_path, 'rb')
        msgImage1 = MIMEImage(fp1.read())
        # self.msg.attach(msgImage1)
        fp1.close()

        # defined image id
        msgImage1.add_header('Content-ID', '<image1>')
        self.msg.attach(msgImage1)

    def config_file(self):
        """
        配置邮件附件
        :return:
        """

        # if the file content is not null, then config the email file
        if self.check_file():

            reportpath = self.log.get_result_path()
            zippath = configBase.EMAIL_FILE

            # zip file
            files = glob.glob(reportpath + '\*')
            f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
            for file in files:
                # 修改压缩文件的目录结构
                f.write(file, '/report/' + os.path.basename(file))
            f.close()

            reportfile = open(zippath, 'rb').read()
            filehtml = MIMEText(reportfile, 'base64', 'utf-8')
            filehtml['Content-Type'] = 'application/octet-stream'
            filehtml['Content-Disposition'] = 'attachment; filename="test.zip"'
            self.msg.attach(filehtml)

    def check_file(self):
        """
        配置测试报告
        :return:
        """
        reportpath = self.log.get_report_path()
        if os.path.isfile(reportpath) and not os.stat(reportpath) == 0:
            return True
        else:
            return False

    def send_email(self):
        """
        send email
        :return:
        """
        self.config_header()
        self.config_content()
        self.config_file()
        # 连接服务器并发送
        try:
            smtp_server = smtplib.SMTP(self.server)  # 连接sever
        except (gaierror and error) as e:
            logger.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(
                    self.sender,
                    self.receiver.split(';'),
                    self.msg.as_string())  # 发送邮件
            finally:
                smtp_server.quit()  # 断开连接
                logger.info(
                    '邮件"{0}"发送成功! 收件人：{1}'.format(
                        self.subject, self.receiver))


class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():

        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()
        return MyEmail.email


if __name__ == "__main__":
    email = MyEmail.get_email()
    email.send_email()

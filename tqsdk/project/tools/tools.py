# -*- coding:utf-8 -*- 
# author: limm_666
import time
from configparser import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import threading



order_id_list = []
trade_id_list = []


def createKey(instrumentId):
    date = time.strftime("%Y-%m-%d", time.localtime())
    key = date + "::" + instrumentId
    return key

'''
邮件提醒交易服务
1. 提醒下单信息
2. 提醒成交信息
3. 提醒风险信息
'''
def EmailService(subject):
    cp = ConfigParser()
    cp.read("../../config.conf")

    # 第三方 SMTP 服务
    mail_stmp = cp.get("Email", "mail_smtp")  # 设置服务器
    mail_host = cp.get("Email", "mail_host")  # 用户名
    mail_pass = cp.get("Email", "mail_pwd")  # 口令
    mail_receiver = cp.get("Email", "mail_receiver")  #收件人

    sender = mail_host
    receivers = [mail_receiver]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')


    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = Header("AutoTradeProcess", 'utf-8')
    message['To'] = Header("TraderReceiver", 'utf-8')


    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_stmp, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_host, mail_pass)
        smtpObj.sendmail(mail_host, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)

'''
新开一个线程，进行数据的存储，
1. 下场下单信息
2. 下场成交信息
'''
def RecordTradeInfo(api):
    while True:
        api.wait_update()
        order_id_list = api.get_order()
        trade_id_list = api.get_trade()


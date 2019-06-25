import datetime
import smtplib
import time
import configparser
import json
import pytz
from email.mime.text import MIMEText
from email.header import Header
from util.Logger import logger

# read config
config = configparser.ConfigParser()
config.read("config.ini")
receivers = [config.get("trade", "email")]


def has_attr(_dict, args):
    return args in _dict.keys()


def from_dict(_dict, *args):
    for a in args:
        _dict = _dict[a]
    return _dict


def from_time_stamp(seconds=0):
    # remark: int(time.time()) 不能放到参数默认值，否则会初始化为常量
    if seconds == 0:
        seconds = int(time.time())
    return datetime.datetime.fromtimestamp(seconds, pytz.timezone('Asia/Shanghai')).strftime(
        '%Y-%m-%d %H:%M:%S')


def get_day_bj():
    return int(datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%d'))


def send_email(content, _subtype='plain', _subject="bitcoinrobot"):
    # 第三方 SMTP 服务
    mail_host = "smtp.gmail.com"  # 设置服务器
    mail_user = "controlservice9@gmail.com"  # 用户名
    mail_pass = "pupso7-waXtuz-qitceh"  # 口令

    message = MIMEText(content, _subtype, 'utf-8')
    message['From'] = Header(mail_user)
    message['To'] = Header(",".join(receivers))
    message['Subject'] = Header(_subject)
    try:
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.ehlo()
        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, receivers, message.as_string())
        server.close()
        logger.info("邮件发送成功")
        return True
    except smtplib.SMTPException as err:
        logger.error("Error: 邮件发送失败,{}".format(err))
        return False


def write_log(text=""):
    with open('log.txt') as f:
        s = f.read()
    mm = str(from_time_stamp())[0:7]
    if s.find(mm) != -1:
        with open(r'log.txt', 'w') as f:
            f.write(text + "\n" + s)
    else:
        with open(r'log.txt', 'a') as f:
            f.writelines("\n")
        # write old logs
        with open(str(from_time_stamp(int(time.time()) - 86400 * 10))[0:7] + '.txt', 'w') as old_f:
            with open('log.txt') as f:
                old_f.writelines(f.readlines()[::-1])
            # write count
            config.read("config.ini")
            symbols = json.loads(config.get("trade", "symbol"))
            for symbol in symbols:
                cfg_field = symbol + "-stat"
                sum_count = 0
                try:
                    sum_count = sum(json.loads(config.get(cfg_field, "count")))
                except Exception as err:
                    logger.error("Error: write_log,{}".format(err))
                old_f.writelines(symbol + " [" + str(sum_count) + "]")
        with open(r'log.txt', 'w') as f:
            f.write(text)

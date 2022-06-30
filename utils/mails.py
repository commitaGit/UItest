import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from utils.times import dt_strftime
from config.conf import cm
from utils.logger import log

def send_mail():
    """
    发送邮件
    :param sendto:收件人列表
   """
    mail_host = cm.EMAIL_INFO["smtp_host"]  # 邮箱服务器地址
    mail_port = cm.EMAIL_INFO["smtp_port"]
    username = cm.EMAIL_INFO["username"]   # 邮箱用户名
    password = cm.EMAIL_INFO["password"]  # 邮箱密码
    receivers = cm.ADDRESSEE  # 收件人

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header(r'UI自动化', 'utf-8')
    message['subject'] = Header(r'UI自动化测试结果', 'utf-8')  # 邮件标题
    message.attach(MIMEText(r'测试结果详见附件', 'plain', 'utf-8'))# 邮件正文
    # 构造附件
    report_root = cm.REPORT_PATH  # 获取报告路径
    report_file = "/{}.html".format(dt_strftime("%Y%m%d"))  # 报告文件名称
    att1 = MIMEText(open(report_root + report_file, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename={}'.format(report_file)
    message.attach(att1)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host, mail_port)  # 25为 SMTP 端口号
        smtp.login(username, password)
        smtp.sendmail(username, receivers, message.as_string())
        log('邮件发送成功')
    except Exception as e:
        log.error(r'邮件发送失败')
        log.error("错误信息：{0}".format(e))

if __name__ == "__main__":
    send_mail()
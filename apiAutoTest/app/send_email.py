import time
from email.mime.application import MIMEApplication
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from get_all_data import make_data_list, save_xlsx_test
from jmx_creater import data_create
from config import config_read
import logging
class QQMail:
    def __init__(self, smtp_sender, smtp_passwd,
                 smtp_receiver):
        self.nickName = None
        self.msg = None
        self.smtp = None
        self.smtp_server_host = 'smtp.qq.com'
        self.smtp_sender = smtp_sender
        self.smtp_passwd = smtp_passwd
        self.smtp_receiver = smtp_receiver

    def login(self):
        self.smtp = SMTP_SSL(self.smtp_server_host)
        try:
            self.smtp.login(self.smtp_sender, self.smtp_passwd)
            return True
        except Exception as e:
            logging.info(e, "登录邮箱服务器失败！")
            return False

    def makeHeader(self, subject, sender_nick_name):
        self.msg = MIMEMultipart()
        self.msg["Subject"] = Header(subject, 'utf-8')
        self.nickName = Header(sender_nick_name, 'utf-8').encode()
        self.msg["From"] = f"{self.nickName} <{self.smtp_sender}>"
        self.msg['To'] = ";".join(self.smtp_receiver)

    def makeText(self, content, l_type="plain"):
        self.msg.attach(MIMEText(content, l_type, 'utf-8'))

    def makeHtml_table(self, content):
        self.makeText(content, "html")

    def addUploadFile(self, l_file_name, file_path):
        attachment = MIMEApplication(open(file_path, 'rb').read())
        # 为附件添加一个标题
        attachment.add_header('Content-Disposition', 'attachment', filename=l_file_name)
        self.msg.attach(attachment)

    def send(self):
        try:
            self.smtp.sendmail(self.smtp_sender, self.smtp_receiver, self.msg.as_string())
            self.smtp.quit()
            return True
        except Exception as e:
            logging.info(e, "发送邮件失败！")
            return False


if __name__ == "__main__":
    #读取配置文件信息
    config = config_read()
    logging.info('开始处理JMETER脚本')
    data_create(config)
    logging.info('完成处理JMETER脚本')

    # 读取配置文件
    # config.read('/app/app/config.ini', encoding='utf-8')

    # 获取邮箱部分的配置
    lsmtp_sender = config.get("'DEFAULT'", "'smtp_sender'")
    lsmtp_password = config.get("'DEFAULT'", "'smtp_password'")
    lsmtp_receiver = (config.get("'DEFAULT'", "'smtp_receiver'")).split(',')
    api_number = config.get("'DEFAULT'", "'api_number'")
    case_num = config.get("'DEFAULT'", "'case_num'")

    # 处理文件头表头
    html_table = "<table style='border-collapse: collapse;  margin: auto;'>\n"
    date = time.localtime()
    html_table += "<tr style='background-color: #f2f2f2;'>\n"
    html_table += "<th colspan='4' style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format(
        f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告")
    html_table += "</tr>\n"
    already_data = make_data_list(config)
    logging.info('读取完毕，当前数据为：', already_data)
    logging.info('开始组装数据')
    apis_list = []
    for apis in already_data[0].values():
        for api in apis:
            if type(api)!=list or len(api)<=4:
                continue
            for j in api:
                if '?' in j[3]:
                    t = j[3].split('?')[0]
                else:
                    t = j[3]
                if t not in apis_list:
                    apis_list.append(t)
    # 报告总览表格
    html_table += "<tr text-align: center;'>\n"
    html_table += "<th colspan='1', style='width: 40%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format("接口总数")
    html_table += "<th colspan='1', style='width: 20%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format(
        "已覆盖接口数量")
    html_table += "<th colspan='2', style='width: 40%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format("覆盖率")
    html_table += "</tr>\n"

    html_table += "<tr text-align: center;'>\n"
    html_table += (
        "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
        " padding: 8px;'>{}</td>").format(api_number)
    html_table += (
        "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
        " padding: 8px;'>{}</td>").format(len(apis_list))
    html_table += (
        "<td text-align: center; colspan='2'; style='text-align: center;border: 1px solid #ddd;"
        f" padding: 8px;'>{(len(apis_list) / int(api_number)*100):.2f}%</td>").format(len(apis_list) / int(api_number)*100)
    html_table += "</tr>\n"

    html_table += "<tr text-align: center;'>\n"
    html_table += "<th colspan='1', style='width: 40%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format(
        "关键场景总数")
    html_table += "<th colspan='1', style='width: 20%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format(
        "已覆盖场景数量")
    html_table += "<th colspan='2', style='width: 40%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format("覆盖率")
    html_table += "</tr>\n"

    html_table += "<tr text-align: center;'>\n"
    html_table += (
        "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
        " padding: 8px;'>{}</td>").format(case_num)
    html_table += (
        "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
        " padding: 8px;'>{}</td>").format(already_data[0]['总计'][0])
    html_table += (
        "<td text-align: center; colspan='2'; style='text-align: center;border: 1px solid #ddd;"
        f" padding: 8px;'>{(already_data[0]['总计'][0] / int(case_num)*100):.2f}%</td>")
    html_table += "</tr>\n"
    # 报告总览表格
    html_table += "<tr text-align: center;'>\n"
    html_table += "<th colspan='1', style='width: 40%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format("模块名称")
    html_table += "<th colspan='1', style='width: 20%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format("调用次数")
    html_table += "<th colspan='1', style='width: 20%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format("失败次数")
    html_table += "<th colspan='1', style='width: 20%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format("通过率")
    html_table += "</tr>\n"
    # 使用glob获取所有.jtl文件
    logging.info('开始读取所有jtl，xml文件')
    already_data = make_data_list(config)
    logging.info('读取完毕，当前数据为：', already_data)
    logging.info('开始组装数据')
    for key in already_data[0].keys():
        if key != '总计':
            html_table += "<tr text-align: center;'>\n"
            html_table += (
                "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
                " padding: 8px;'>{}</td>").format(key)
            html_table += (
                "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
                "padding: 8px;'>{}</td>").format(already_data[0][key][0][0])
            html_table += (
                "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
                "padding: 8px;'>{}</td>").format(already_data[0][key][0][1])
            html_table += (
                "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
                "padding: 8px;'>{}</td>").format(already_data[0][key][0][2])
            html_table += "</tr>\n"
    html_table += "<tr text-align: center;'>\n"
    html_table += (
        "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
        " padding: 8px;'>{}</td>").format('总计')
    html_table += (
        "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
        "padding: 8px;'>{}</td>").format(already_data[0]['总计'][0])
    html_table += (
        "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
        "padding: 8px;'>{}</td>").format(already_data[0]['总计'][1])
    html_table += (
        "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
        "padding: 8px;'>{}</td>").format(already_data[0]['总计'][2])
    html_table += "</tr>\n"
    html_table += "</table>"
    date = time.localtime()
    qq = QQMail(lsmtp_sender, lsmtp_password, lsmtp_receiver)
    logging.info('数据组装完成，开始写入excel')
    save_xlsx_test(already_data[0], already_data[1])
    logging.info('excel组装完成,准备发送邮件')
    if qq.login():
        qq.makeHeader(f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告",
                      f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告")
        qq.makeHtml_table(html_table)
        qq.addUploadFile(f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告.xlsx",fr"/app/apiAutoTest/app/test_records/{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告.xlsx")
                         #fr"/app/app/test_records/{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告.xlsx")

        qq.send()
    logging.info('邮件发送成功！')
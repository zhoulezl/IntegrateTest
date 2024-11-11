import time
from email.mime.application import MIMEApplication
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from data_excel import make_excel
from config import YamlHandler
import os
import zipfile

running_home = r"D:\pythonPro\IntegrateTest"


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
        #

    def login(self):
        self.smtp = SMTP_SSL(self.smtp_server_host)
        try:
            self.smtp.login(self.smtp_sender, self.smtp_passwd)
            return True
        except Exception as e:
            print(e, "登录邮箱服务器失败！")
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
            print(e, "发送邮件失败！")
            return False


def send_mail(test_data, big_key):
    config_list = YamlHandler(rf'{running_home}\本地play_UI _easySoftWare\config\config.yaml').read_yaml()
    # 读取发件邮箱信息
    lsmtp_sender = '2126744957@qq.com'
    lsmtp_password = 'qqvynwenzdimhjcj'
    test_data = test_data
    false_count = 0

    # 获取收件部分的配置
    lsmtp_receiver = config_list[big_key]['lsmtp_receivers'].replace(' ', '').split(',')
    case_nums = config_list[big_key]['case_numbers']

    # 处理文件头表头
    html_table = "<table style='border-collapse: collapse;  margin: auto;'>\n"
    date = time.localtime()
    html_table += "<tr style='background-color: #f2f2f2;'>\n"
    html_table += "<th colspan='4' style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format(
        f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日UI自动化测试执行报告")
    html_table += "</tr>\n"

    # 报告总览表格
    case_num = len(test_data)
    html_table += "<tr text-align: center;'>\n"
    html_table += "<th colspan='1', style='width: 25%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format(
        "平台名称")
    html_table += "<th colspan='1', style='width: 25%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format(
        "关键场景总数")
    html_table += "<th colspan='1', style='width: 25%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format(
        "已覆盖场景数量")
    html_table += "<th colspan='1', style='width: 25%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format(
        "覆盖率")
    html_table += "</tr>\n"

    html_table += "<tr text-align: center;'>\n"
    html_table += (
        "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
        " padding: 8px;'>{}</td>").format(big_key)
    html_table += (
        "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
        " padding: 8px;'>{}</td>").format(case_nums)
    html_table += (
        "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
        " padding: 8px;'>{}</td>").format(case_num)
    html_table += (
        "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
        f" padding: 8px;'>{(case_num / int(case_nums) * 100):.2f}%</td>")
    html_table += "</tr>\n"

    html_table += "<tr text-align: center;'>\n"
    html_table += "<th colspan='1', style='width: 25%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format(
        "模块名称")
    html_table += "<th colspan='1', style='width: 25%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format(
        "测试用例数量")
    html_table += "<th colspan='1', style='width: 25%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format(
        "未通过用例数量")
    html_table += "<th colspan='1', style='width: 25%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format(
        "通过率")
    html_table += "</tr>\n"

    print('开始组装数据')
    excel_data = {}
    for model_name in config_list[big_key]['model_names'].replace(' ', '').split(','):
        excel_data[model_name] = []
        html_table += "<tr text-align: center;'>\n"
        # 统计各个模块用例总数
        count = 0
        pass_count = 0
        for case in test_data:
            # print(model_name)
            # print(case[2])
            if model_name in case[2]:

                excel_data[model_name].append(case)
                count += 1
                if '测试失败' not in case[-1]:
                    pass_count += 1
                else:
                    false_count += 1
        if count == 0:
            continue
        html_table += (
            "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
            " padding: 8px;'>{}</td>").format(model_name)
        html_table += (
            "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
            "padding: 8px;'>{}</td>").format(count)
        html_table += (
            "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
            "padding: 8px;'>{}</td>").format(count - pass_count)
        html_table += (
            "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
            "padding: 8px;'>{:.2f}%</td>").format(pass_count / count * 100)
        html_table += "</tr>\n"

    html_table += "<tr text-align: center;'>\n"
    html_table += (
        "<td text-align: center; colspan='1'; style='text-align: center;border: 1px solid #ddd;"
        " padding: 8px;'>{}</td>").format('总计')
    html_table += (
        "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
        "padding: 8px;'>{}</td>").format(len(test_data))

    html_table += (
        "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
        "padding: 8px;'>{}</td>").format(false_count)
    html_table += (
        "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
        "padding: 8px;'>{:.2f}%</td>").format((len(test_data) - false_count) / len(test_data) * 100)
    excel_data['总计'] = ['总计', len(test_data), false_count,
                          ((len(test_data) - false_count) / len(test_data) * 100)]
    html_table += "</tr>\n"
    html_table += "</table>"

    date = time.localtime()
    qq = QQMail(lsmtp_sender, lsmtp_password, lsmtp_receiver)
    print('数据组装完成，开始写入excel')
    make_excel(excel_data, big_key)
    print('excel组装完成,准备压缩全部报告文件')

    # folders_to_zip = ['records/videos', 'test_records']
    # zip_file_path = f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日UI自动化测试执行报告.zip"
    # with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    #     for folder in folders_to_zip:
    #         for root, dirs, files in os.walk(folder):
    #             for file in files:
    #                 # 获取文件的完整路径
    #                 file_path = os.path.join(root, file)
    #                 # 相对于文件夹的路径，用于在zip文件中保持文件结构
    #                 arcname = os.path.relpath(file_path, os.path.dirname(folder))
    #                 # 添加到zip文件中
    #                 zipf.write(file_path, arcname)
    print('文件压缩完成，准备发送邮件')
    if qq.login():
        qq.makeHeader(f"{config_list[big_key]['email_name']} {date.tm_year}年{date.tm_mon}月{date.tm_mday}日",
                      f"{config_list[big_key]['email_name']} {date.tm_year}年{date.tm_mon}月{date.tm_mday}日")
        qq.makeHtml_table(html_table)
        qq.addUploadFile(f"{big_key}-{date.tm_year}年{date.tm_mon}月{date.tm_mday}日UI自动化测试执行报告.xlsx",
                         fr"{running_home}\本地play_UI _easySoftWare/test_records/{big_key}-{date.tm_year}年{date.tm_mon}月{date.tm_mday}日UI自动化测试执行报告.xlsx")
        qq.addUploadFile(f"{big_key}平台{date.tm_year}年{date.tm_mon}月{date.tm_mday}日UI自动化测试.mp4",
                         fr"{running_home}\本地play_UI _easySoftWare/test_records/{big_key}/{big_key}平台{date.tm_year}年{date.tm_mon}月{date.tm_mday}日UI自动化测试.mp4")
        qq.send()
    for filename in os.listdir(fr"{running_home}\本地play_UI _easySoftWare\test_records\{big_key}"):
        os.remove(os.path.join(fr"{running_home}\本地play_UI _easySoftWare\test_records\{big_key}", filename))
    print('邮件发送成功！')

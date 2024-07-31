import copy
import time
from email.mime.application import MIMEApplication
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import jtl_html
import glob
from configparser import ConfigParser

from Auto_test_ly.autoTest.get_all_data import save_xlsx
from Auto_test_ly.autoTest.xml_to_dict import find_false


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


GETTING_INDEX = [0, 2, 3, 5, 7, 13]
data_dict = {'api_jmeter/openmind/model/basetest': 'openmind-模型模块-基本测试',
             'api_jmeter/openmind/oneid': 'openmind-oneid模块',
             'api_jmeter/openeuler/easysoftware': 'openeuler_软件市场'}
error_msg = find_false()
if __name__ == "__main__":
    config = ConfigParser()
    # 读取配置文件
    config.read('config.ini')
    # 获取邮箱部分的配置
    lsmtp_sender = config.get('DEFAULT', 'smtp_sender')
    lsmtp_password = config.get('DEFAULT', 'smtp_password')
    lsmtp_receiver = (config.get('DEFAULT', 'smtp_receiver')).split(',')

    # 处理文件头表头
    html_table = "<table style='border-collapse: collapse;  margin: auto;'>\n"
    date = time.localtime()
    html_table += "<tr style='background-color: #f2f2f2;'>\n"
    html_table += "<th colspan='5' style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format(
        f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告")
    html_table += "</tr>\n"
    # 报告总览表格
    html_table += "<tr text-align: center;'>\n"
    html_table += "<th colspan='2', style='width: 40%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format("模块名称")
    html_table += "<th colspan='1', style='width: 20%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format("调用次数")
    html_table += "<th colspan='1', style='width: 20%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format("失败次数")
    html_table += "<th colspan='1', style='width: 20%;border: 2px solid #ddd; padding: 8px;'>{}</th>".format("通过率")
    html_table += "</tr>\n"
    # 使用glob获取所有.jtl文件
    all_count = 0
    all_false_count = 0
    false_list = []
    html_table_inner = ''
    for directory in data_dict.keys():
        if glob.glob(f'{directory}/*.jtl'):
            # 开始处理数据
            if not glob.glob(f'{directory}/{date.tm_year}{date.tm_mon:02d}{date.tm_mday:02d}.jtl'):
                print(f'{directory}路径下没有{date.tm_year}{date.tm_mon:02d}{date.tm_mday:02d}.jtl文件，请检查')
            else:
                for file_name in glob.glob(f'{directory}/{date.tm_year}{date.tm_mon:02d}{date.tm_mday:02d}.jtl'):

                    table = jtl_html.make_table(file_name, GETTING_INDEX)
                    false_count = 0

                    for row in table.rows:
                        row[1], row[2], row[3], row[4], row[5] = row[3], row[1], row[5], row[2], row[4]
                        row.insert(4, (error_msg[row[1] + row[2] + 'request_way']))
                        print(row)
                        if row[-1] == 'false':
                            false_count += 1
                            row.append((error_msg[row[1] + row[2]+'error_msg']))
                            if row[1] + row[2]+'args' in error_msg.keys():
                                print(error_msg[row[1] + row[2]+'args'])
                                row.append((error_msg[row[1] + row[2]+'args']))
                            else:
                                row.append('-')
                            rew = copy.copy(row)
                            false_list.append(rew)
                            false_list[-1][0] = data_dict[directory]
                    pass_precent = "%0.2f" % ((len(table.rows) - false_count) / len(table.rows) * 100)
                    all_count += len(table.rows)
                    all_false_count += false_count

                    html_table += "<tr text-align: center;'>\n"
                    html_table += (
                        "<td text-align: center; colspan='2'; style='text-align: center;border: 1px solid #ddd;"
                        " padding: 8px;'>{}</td>").format(data_dict[directory])
                    html_table += (
                        "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
                        "padding: 8px;'>{}</td>").format(len(table.rows))
                    html_table += (
                        "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
                        "padding: 8px;'>{}</td>").format(false_count)
                    html_table += (
                        "<td text-align: center; colspan='1' style='text-align: center;border: 1px solid #ddd; "
                        "padding: 8px;'>{}%</td>").format(pass_precent)
                    html_table += "</tr>\n"

                    html_table_inner += (
                        "<tr>\n<th colspan='9' style='background-color: #f2f2f2; border: 1px solid #ddd; "
                        "padding: 8px;'>{}</th>").format(
                        f"{data_dict[directory]}接口测试详情如下：")
                    html_table_inner += "</tr>\n"
                    html_table_inner += "<tr style='background-color: #f2f2f2;'>\n"
                    html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("测试时间")
                    html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("测试场景")
                    html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("测试步骤")
                    html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("接口地址")
                    html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("请求方式")
                    html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("状态码")
                    html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("测试结果")
                    html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("错误信息")
                    html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("传入参数")
                    html_table_inner += "</tr>\n"

                    for row in table.rows:
                        html_table_inner += "<tr>\n"
                        for field in row:
                            if field == 'false':
                                html_table_inner += ("<td style='border: 1px solid #ddd;background-color: #ffa07a;"
                                                     " padding: 8px;'>{}</td>").format(field)
                            elif field == '-':
                                html_table_inner += ("<td style='text-align: center; border: 1px solid #ddd;"
                                                     " padding: 8px;'>{}</td>").format(field)
                            else:
                                html_table_inner += ("<td style='border: 1px solid #ddd;"
                                                     " padding: 8px;'>{}</td>").format(field)
                        html_table_inner += "</tr>\n"
    if all_count == 0:
        print('接口调用次数为零，请检查文件')
    else:
        html_table += "<tr text-align: center;'>\n"
        html_table += (
            "<td  colspan='2'; style='text-align: center; border: 1px solid #ddd; padding: 8px;'>{}</td>").format(
            '总计')
        html_table += "<td colspan='1' style='text-align: center; border: 1px solid #ddd; padding: 8px;'>{}</td>".format(
            all_count)
        html_table += "<td colspan='1' style='text-align: center; border: 1px solid #ddd; padding: 8px;'>{}</td>".format(
            all_false_count)
        html_table += "<td colspan='1' style='text-align: center; border: 1px solid #ddd; padding: 8px;'>{}</td>".format(
            f"{'%0.2f' % ((all_count - all_false_count) / all_count * 100)}%")
        html_table += "</tr>\n"

        html_table += "</tr>\n"
        # html_table += ("<tr>\n<th colspan='9' style='background-color: #f2f2f2; border: 1px solid #ddd;"
        #                " padding: 8px;'>{}</th>").format(f"出错接口详情如下：")
        # html_table += "</tr>\n"

        # html_table += "<tr style='background-color: #f2f2f2;'>\n"
        # html_table += "<tr >\n"
        # html_table += "<th style=' border: 1px solid #ddd; padding: 8px;'>{}</th>".format("模块名称")
        # html_table += "<th style=' border: 1px solid #ddd; padding: 8px;'>{}</th>".format("测试场景")
        # html_table += "<th style=' border: 1px solid #ddd; padding: 8px;'>{}</th>".format("测试步骤")
        # html_table += "<th style=' border: 1px solid #ddd; padding: 8px;'>{}</th>".format("接口地址")
        # html_table += "<th style=' border: 1px solid #ddd; padding: 8px;'>{}</th>".format("请求方式")
        # html_table += "<th style=' border: 1px solid #ddd; padding: 8px;'>{}</th>".format("状态码")
        # html_table += "<th style=' border: 1px solid #ddd; padding: 8px;'>{}</th>".format("测试结果")
        # html_table += "<th style=' border: 1px solid #ddd; padding: 8px;'>{}</th>".format("错误信息")
        # html_table += "<th style=' border: 1px solid #ddd; padding: 8px;'>{}</th>".format("传入参数")
        # html_table += "</tr>\n"

        # for row in false_list:
        #     html_table += "<tr>\n"
        #     for field in row:
        #         html_table += ("<td style='border: 1px solid #ddd;"
        #                        " padding: 8px;'>{}</td>").format(field)
        #     html_table += "</tr>\n"
        # html_table += html_table_inner
        html_table += "</table>"
        date = time.localtime()

        qq = QQMail(lsmtp_sender, lsmtp_password, lsmtp_receiver)
        save_xlsx()
        if qq.login():
            qq.makeHeader(f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告",
                          f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告")
            qq.makeHtml_table(html_table)
            # qq.addUploadFile(f"{date.tm_year}年{date.tm_mon}月{date.tm_day}日接口自动化测试执行报告.xlsx", "./test.html")
            qq.send()

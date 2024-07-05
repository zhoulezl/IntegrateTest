import copy
import time
from email.mime.application import MIMEApplication
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import jtl_html
import glob


class QQMail:
    def __init__(self, smtp_sender, smtp_passwd,
                 smtp_receiver):
        self.smtp_server_host = 'smtp.qq.com'
        self.smtp_sender = smtp_sender
        self.smtp_passwd = smtp_passwd
        self.smtp_receiver = smtp_receiver

    def login(self):
        self.smtp = SMTP_SSL(self.smtp_server_host)
        try:
            self.smtp.login(self.smtp_sender, self.smtp_passwd)
            return True
        except:
            print("登录邮箱服务器失败！")
            return False

    def makeHeader(self, subject, sender_nick_name):
        self.msg = MIMEMultipart()
        self.msg["Subject"] = Header(subject, 'utf-8')
        self.nickName = Header(sender_nick_name, 'utf-8').encode()
        self.msg["From"] = f"{self.nickName} <{self.smtp_sender}>"
        self.msg['To'] = ";".join(self.smtp_receiver)

    def makeText(self, content, type="plain"):
        self.msg.attach(MIMEText(content, type, 'utf-8'))

    def makeHtml_table(self, content):
        self.makeText(content, type="html")
        # self.makeText(content)

    def addUploadFile(self, file_name, file_path):
        attachment = MIMEApplication(open(file_path, 'rb').read())
        # 为附件添加一个标题
        attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
        self.msg.attach(attachment)

    def send(self):
        try:
            self.smtp.sendmail(self.smtp_sender, self.smtp_receiver, self.msg.as_string())
            self.smtp.quit()
            return True
        except:
            print("发送邮件失败！")
            return False


# 邮件发送者和接收者
# sender_email = "2126744957@qq.com"
# receiver_email = "2126744957@qq.com"
# receiver_email = "liuyu418@h-partners.com"

GETTING_INDEX = [0, 2, 3, 5, 7]
data_dict = {'api_jmeter/openmind/model/basetest': 'openmind-模型模块-基本测试',
             'api_jmeter/openmind/oneid': 'openmind-oneid模块',
             'api_jmeter/openeuler/easysoftware': 'openeuler_软件市场'}
if __name__ == "__main__":

    # 处理文件头表头
    html_table = "<table style='border-collapse: collapse; width: 100%; margin: auto;'>\n"
    date = time.localtime()
    html_table += "<tr style='background-color: #f2f2f2;'>\n"
    html_table += "<th colspan='5' style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format(
        f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告")
    html_table += "</tr>\n"
    # html_table += "<tr style='background-color: #f2f2f2;'>\n"
    # 报告总览表格
    html_table += "<tr text-align: center;'>\n"
    html_table += "<th colspan='2' style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("模块名称")
    html_table += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("调用次数")
    html_table += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("失败次数")
    html_table += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("通过率")
    html_table += "</tr>\n"
    # 使用glob获取所有.jtl文件
    all_count = 0
    all_false_count = 0
    false_list = []
    html_table_inner = ''
    for directory in data_dict.keys():
        if glob.glob(f'{directory}/*.jtl'):
            # 开始处理数据
            for file_name in glob.glob(f'{directory}/{date.tm_year}{(date.tm_mon):02d}{(date.tm_mday):02d}.jtl'):
                print(file_name)
                table = jtl_html.make_table(file_name, GETTING_INDEX)

                false_count = 0
                for row in table.rows:
                    if row[-1] == 'false':
                        false_count += 1
                        rew = copy.copy(row)
                        false_list.append(rew)
                        false_list[-1][0] = data_dict[directory]
                pass_precent = "%0.2f" % ((len(table.rows) - false_count) / len(table.rows) * 100)
                all_count += len(table.rows)
                all_false_count += false_count
                # html_table += "<tr text-align: center;'>\n"
                # html_table += "<th colspan='5'; text-align: center; style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format(
                #     f"{data_dict[directory]}接口测试情况：今日调用接口{len(table.rows)}次,其中有{false_count}次调用出错，"
                #     f"通过率：{pass_precent}%")
                # html_table += "</tr>\n"
                html_table += "<tr text-align: center;'>\n"
                html_table += ("<td text-align: center; colspan='2'; style='text-align: center;border: 1px solid #ddd; padding: 8px;'>{}</td>").format(data_dict[directory])
                html_table += ("<td text-align: center; style='text-align: center;border: 1px solid #ddd; padding: 8px;'>{}</td>").format(len(table.rows))
                html_table += ("<td text-align: center; style='text-align: center;border: 1px solid #ddd; padding: 8px;'>{}</td>").format(false_count)
                html_table += ("<td text-align: center; style='text-align: center;border: 1px solid #ddd; padding: 8px;'>{}%</td>").format(pass_precent)
                html_table += "</tr>\n"


                html_table_inner += "<tr>\n<th colspan='5' style='background-color: #f2f2f2; border: 1px solid #ddd; padding: 8px;'>{}</th>".format(
                    f"{data_dict[directory]}接口测试详情如下：")
                html_table_inner += "</tr>\n"
                html_table_inner += "<tr style='background-color: #f2f2f2;'>\n"
                html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("时间")
                html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("接口")
                html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("状态码")
                html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("名称")
                html_table_inner += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("测试结果")
                html_table_inner += "</tr>\n"

                for row in table.rows:
                    html_table_inner += "<tr>\n"
                    for field in row:
                        if row[-1] == 'false':
                            html_table_inner += ("<td style='border: 1px solid #ddd;background-color: #ffa07a;"
                                                 " padding: 8px;'>{}</td>").format(field)
                        else:
                            html_table_inner += ("<td style='border: 1px solid #ddd;"
                                                 " padding: 8px;'>{}</td>").format(field)
                    html_table_inner += "</tr>\n"


    # html_table += ("<th colspan='5' style='background-color: #f2f2f2; border: 1px solid #ddd; "
    #                "padding: 8px;'>{}</th>").format(
    #     f"今日共计调用接口{all_count}次,其中有{all_false_count}次调用出错，"
    #     f"总通过率：{"%0.2f" % ((all_count - all_false_count) / all_count * 100)}%")

    html_table += "<tr text-align: center;'>\n"
    html_table += ("<td  colspan='2'; style='text-align: center; border: 1px solid #ddd; padding: 8px;'>{}</td>").format(
        '总计')
    html_table += ("<td  style='text-align: center; border: 1px solid #ddd; padding: 8px;'>{}</td>").format(
        all_count)
    html_table += ("<td  style='text-align: center; border: 1px solid #ddd; padding: 8px;'>{}</td>").format(all_false_count)
    html_table += ("<td  style='text-align: center; border: 1px solid #ddd; padding: 8px;'>{}</td>").format(
        f"{'%0.2f' % ((all_count - all_false_count) / all_count * 100)}%")
    html_table += "</tr>\n"

    html_table += "</tr>\n"
    # html_table += "<table>"
    html_table += ("<tr>\n<th colspan='5' style='background-color: #f2f2f2; border: 1px solid #ddd;"
                   " padding: 8px;'>{}</th>").format(f"出错接口详情如下：")
    html_table += "</tr>\n"

    html_table += "<tr style='background-color: #f2f2f2;'>\n"
    html_table += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("模块名称")
    html_table += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("接口")
    html_table += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("状态码")
    html_table += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("名称")
    html_table += "<th style='border: 1px solid #ddd; padding: 8px;'>{}</th>".format("测试结果")
    html_table += "</tr>\n"

    for row in false_list:
        html_table += "<tr>\n"
        for field in row:
            html_table += ("<td style='border: 1px solid #ddd;background-color: #ffa07a;"
                               " padding: 8px;'>{}</td>").format(field)
        html_table += "</tr>\n"
    # html_table += "</table>\n"
    html_table += html_table_inner
    html_table += "</table>"
    date = time.localtime()
    # qq = QQMail('2126744957@qq.com', 'qqvynwenzdimhjcj', ['gaoxiaozhen1@h-partners.com',
    #                                                       'wangxiaoliang30@h-partners.com', 'liuyu418@h-partners.com',
    #                                                       '2126744957@qq.com', 'george.cao@huawei.com'])
    # qq = QQMail(
    # '2126744957@qq.com', 'qqvynwenzdimhjcj', ['790746421@qq.com','liuyu418@h-partners.com','2126744957@qq.com'])
    qq = QQMail('2126744957@qq.com', 'qqvynwenzdimhjcj', ['2126744957@qq.com'])
    if qq.login():
        qq.makeHeader(f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告",
                      f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告")
        # qq.makeText("smtplib模块主要负责发送邮件：是一个发送邮件的动作，连接邮箱服务器，登录邮箱，发送邮件（有发件人，收信人，邮件内容）。")
        # qq.makeHtml("<p><strong>smtplib模块主要负责发送邮件</strong></p>")
        qq.makeHtml_table(html_table)
        # qq.addUploadFile(f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告.html", "./test.html")
        qq.send()

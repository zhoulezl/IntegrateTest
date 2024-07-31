import copy
import glob
import time

import xmltodict
from prettytable import PrettyTable

from Auto_test_ly.autoTest.data_excel import make_excel

GETTING_INDEX = [0, 2, 3, 5, 7, 13]
data_dict = {r'api_jmeter/openmind/model/basetest': 'openmind-模型模块-基本测试',
             r'api_jmeter/openmind/oneid': 'openmind-oneid模块',
             r'api_jmeter/openeuler/easysoftware': 'openeuler_软件市场'}

date = time.localtime()
filepath = fr'api_jmeter\openmind\model\basetest\{date.tm_year}{date.tm_mon:02}{date.tm_mday:02}.xml'


def make_table(file_path: str, getting_index: list):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line[0] == '*' or line == '':
                continue
            line_data = line.strip().split(",")
            data.append(line_data)
    # 清洗数据
    for i in range(len(data)):
        if len(data[i]) == 1:
            data[i] = None

    table = PrettyTable()
    table.field_names = [data[0][i] for i in getting_index]

    for i in data[1::]:
        if i is not None and len(i) == len(data[0]):
            i[0] = time.strftime("%Y年%m月%d日%H:%M:%S", time.localtime(int(int(i[0]) / 1000)))
            list_ready = [i[j] for j in getting_index]
            table.add_row(list_ready)
    return table


def find_false(filepath):
    marking_result_list = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        xml_data = f.read()
    if xml_data:
        xml_dict = xmltodict.parse(xml_data)
        result_list = xml_dict['testResults']['httpSample']
        for result in result_list:
            marking_result = [result['@lb'], result['@tn'], result['method']['#text'], result['responseData']['#text']]
            if '#text' in result['queryString'].keys():
                marking_result.append(result["queryString"]['#text'])
                marking_result_list[marking_result[1] + marking_result[0] + 'error_msg'] = marking_result[-2].replace(
                    r'\n', '  ')
                marking_result_list[marking_result[1] + marking_result[0] + 'args'] = marking_result[-1].replace(r'\n',
                                                                                                                 ' ')
            else:
                marking_result_list[marking_result[1] + marking_result[0] + 'error_msg'] = marking_result[-1].replace(
                    r'\n', '  ')
            marking_result_list[marking_result[1] + marking_result[0] + 'request_way'] = marking_result[2]
    return marking_result_list


# if __name__ == '__main__':

def make_data_list():
    # 使用glob获取所有.jtl文件
    all_count = 0
    all_false_count = 0
    false_list = []
    html_table_inner = ''
    error_msg = find_false(filepath)
    date = time.localtime()
    data_list = {}
    for directory in data_dict.keys():
        if glob.glob(f'{directory}/*.jtl'):
            # 开始处理数据
            if not glob.glob(f'{directory}/{date.tm_year}{date.tm_mon:02d}{date.tm_mday:02d}.jtl'):
                pass
                # print(f'{directory}路径下没有{date.tm_year}{date.tm_mon:02d}{date.tm_mday:02d}.jtl文件，请检查')
            else:
                for file_name in glob.glob(f'{directory}/{date.tm_year}{date.tm_mon:02d}{date.tm_mday:02d}.jtl'):
                    table = make_table(file_name, GETTING_INDEX)
                    false_count = 0
                    for row in table.rows:
                        row[1], row[2], row[3], row[4], row[5] = row[3], row[1], row[5], row[2], row[4]
                        row.insert(4, (error_msg[row[1] + row[2] + 'request_way']))
                        if row[-1] == 'false':
                            false_count += 1
                            row.append((error_msg[row[1] + row[2] + 'error_msg']))
                            if row[1] + row[2] + 'args' in error_msg.keys():
                                row.append((error_msg[row[1] + row[2] + 'args']))
                            else:
                                row.append('-')
                            rew = copy.copy(row)
                            false_list.append(rew)
                            false_list[-1][0] = data_dict[directory]

                    # table.field_names = ['测试时间','测试场景','测试步骤','接口地址','请求方式','状态码','测试结果','错误信息','传入参数']
                    # table.add_column(fieldname='测试结果')
                    pass_precent = f"{"%0.2f" % ((len(table.rows) - false_count) / len(table.rows) * 100)}%"
                    all_count += len(table.rows)
                    all_false_count += false_count
                    data_list[data_dict[directory]] = [[len(table.rows), false_count, pass_precent], table.rows]
    data_list["总计"] = [all_count, all_false_count, f"{'%0.2f' % ((all_count - all_false_count) / all_count * 100)}%"]
    return [data_list, false_list]


def save_xlsx():
    all_data_list = make_data_list()
    data_list = all_data_list[0]
    false_list = all_data_list[1]
    make_excel(data_list, false_list)


def save_xlsx_test(data_list, false_list):
    make_excel(data_list, false_list)

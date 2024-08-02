import copy
import glob
import time
import xmltodict
from prettytable import PrettyTable
from data_excel import make_excel
import configparser

config = configparser.ConfigParser()
# 读取配置文件
# config.read(r'/app/app/config.ini', encoding='utf-8')
config.read('/app/app/config.ini', encoding='utf-8')
GETTING_INDEX = [0, 2, 3, 5, 7, 13]
data_dict = {}
# print(config.sections())
print(config.options("'DEFAULT'"))
data_dict_key = config.get("'DEFAULT'", "'data_dict_key'").split(',')
data_dict_value = config.get("'DEFAULT'", "'data_dict_value'").split(',')
for i in range(len(data_dict_key)):
    data_dict[data_dict_key[i]] = data_dict_value[i]
# print(data_dict)
date = time.localtime()
xml_filepath = []
for path in data_dict_key:
    xml_filepath.append(path + fr'{date.tm_year}{date.tm_mon:02}{date.tm_mday:02}.xml')
print('xml_filepath:', xml_filepath)


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
    table.field_names = []
    if len(data) == 0:
        return table
    for i in range(len(data[0])):
        if i in getting_index:
            table.field_names.append(data[0][i])
    while len(table.field_names) < 6:
        table.field_names.append('-')

    for i in data[1::]:
        if i is not None and len(i) == len(data[0]):
            i[0] = time.strftime("%Y年%m月%d日%H:%M:%S", time.localtime(int(int(i[0]) / 1000)))
            list_ready = [i[j] for j in getting_index]
            table.add_row(list_ready)
    return table


def find_false(filepath):
    print('filepath:', filepath)
    marking_result_list = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        xml_data = f.read()
    if xml_data:
        xml_dict = xmltodict.parse(xml_data)
        # print('xml_dict:', xml_dict)
        result_list = xml_dict['testResults']['httpSample']
        # print('result_list:', result_list)
        for result in result_list:
            # print('result:', result)
            marking_result = [result['@lb'], result['@tn'], result['method']['#text']]
            try:
                marking_result.append(result['responseData']['#text'])
            except Exception as e:
                marking_result.append('-')
            # print('marking_result:', marking_result)
            if '#text' in result['queryString'].keys():
                marking_result.append(result["queryString"]['#text'])
                marking_result_list[marking_result[1] + marking_result[0] + 'error_msg'] = marking_result[
                    -2].replace(
                    r'\n', '  ')
                marking_result_list[marking_result[1] + marking_result[0] + 'args'] = marking_result[-1].replace(
                    r'\n',
                    ' ')
            else:
                marking_result_list[marking_result[1] + marking_result[0] + 'error_msg'] = marking_result[
                    -1].replace(
                    r'\n', '  ')
            marking_result_list[marking_result[1] + marking_result[0] + 'request_way'] = marking_result[2]
    return marking_result_list


# if __name__ == '__main__':

def make_data_list():
    # 使用glob获取所有.jtl文件
    all_count = 0
    all_false_count = 0
    false_list = []
    error_msgs = {}
    for filepath in xml_filepath:

        error_msg = find_false(filepath)
        for key in error_msg.keys():
            error_msgs[key] = error_msg[key]

    # print('error_msgs:', error_msgs)
    date = time.localtime()
    data_list = {}
    for directory in data_dict.keys():
        if glob.glob(f'{directory}*.jtl'):
            # 开始处理数据
            if not glob.glob(f'{directory}{date.tm_year}{date.tm_mon:02d}{date.tm_mday:02d}.jtl'):
                pass
                # print(f'{directory}路径下没有{date.tm_year}{date.tm_mon:02d}{date.tm_mday:02d}.jtl文件，请检查')
            else:
                for file_name in glob.glob(f'{directory}{date.tm_year}{date.tm_mon:02d}{date.tm_mday:02d}.jtl'):
                    # try:
                    table = make_table(file_name, GETTING_INDEX)
                    # print('table:\n', table)
                    false_count = 0
                    for row in table.rows:
                        # print('修正前row:', row)
                        row[1], row[2], row[3], row[4], row[5] = row[3], row[1], row[5], row[2], row[4]
                        # print('修正后row:', row)
                        if row[1] + row[2] + 'request_way' in error_msgs.keys():
                            row.insert(4, (error_msgs[row[1] + row[2] + 'request_way']))
                        else:
                            row.insert(4, ('-'))

                        if row[-1] == 'false':
                            false_count += 1
                            row.append((error_msgs[row[1] + row[2] + 'error_msg']))
                            if row[1] + row[2] + 'args' in error_msgs.keys():
                                row.append((error_msgs[row[1] + row[2] + 'args']))
                            else:
                                row.append('-')
                            rew = copy.copy(row)
                            # print(rew)
                            false_list.append(rew)
                            false_list[-1][0] = data_dict[directory]
                            # print(false_list)

                    # table.field_names = ['测试时间','测试场景','测试步骤','接口地址','请求方式','状态码','测试结果','错误信息','传入参数']
                    # table.add_column(fieldname='测试结果')
                    if len(table.rows) == 0:
                        pass_precent = '-'
                    else:
                        pass_precent = f"{'%.2f' % ((len(table.rows) - false_count) / len(table.rows) * 100)}%"
                    all_count += len(table.rows)
                    all_false_count += false_count
                    data_list[data_dict[directory]] = [[len(table.rows), false_count, pass_precent], table.rows]
                    # except Exception as e:
                    #     print(e)
    if all_count != 0:
        data_list["总计"] = [all_count, all_false_count,
                             f"{'%0.2f' % ((all_count - all_false_count) / all_count * 100)}%"]
    else:
        data_list["总计"] = [all_count, all_false_count, '--']
    return [data_list, false_list]


def save_xlsx():
    all_data_list = make_data_list()
    data_list = all_data_list[0]
    false_list = all_data_list[1]
    make_excel(data_list, false_list)


def save_xlsx_test(data_list, false_list):
    make_excel(data_list, false_list)

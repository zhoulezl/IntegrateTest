import time
from prettytable import PrettyTable

# 存放jtl文件的路径；列表
data_dict = ['api_jmeter/openmind/model/basetest', 'api_jmeter/openmind/oneid', 'api_jmeter/openeuler/easysoftware']
# 指定列表中的元素序号（要获取的列）
GETTING_INDEX = [0, 2, 3, 5, 7]


def generate_html_table(data):
    date = time.localtime()

    headers = data[0]
    rows = data[1:]
    count = 0
    for row in rows:
        if not row:
            continue
        try:
            if row[7] == "true":
                count += 1
        except Exception:
            print(row)
        # 处理时间戳
        try:
            time.localtime(int(int(row[0]) / 1000))

        except Exception:
            continue
        row[0] = time.strftime("%Y年%m月%d日%H:%M:%S", time.localtime(int(int(row[0]) / 1000)))

    pass_precent = count / len(rows)
    caption_color = None
    if pass_precent >= 0.95:
        caption_color = 'black'
    else:
        caption_color = 'red'
    # 样式
    html = '<html>\n<head>\n<style>\n'
    html += ('table {\n'
             'width : 100%;\n'
             'white-space: nowrap;\n'
             'border-collapse :collapse;\n'
             # 'marginleft: auto;\n'
             # 'marginright: auto;\n'
             '}\n')
    html += ('table caption{\n'
             'font-size: 2em;\n'
             'font-weight: bold;\n'
             'margin: 0 0;\n'
             'border: 1px solid #999;\n'
             '}\n')
    html += ('th,td{\n'
             'border: 1px solid #999;\n'
             'max-width: 200px;\n'
             'text-align: center;\n'
             'padding: 1px 1px;\n'
             'overflow: hidden;\n'
             'text-overflow: ellipsis;\n'
             '}\n')
    html += ('table thead tr{\n'
             'background-color: #008c8c;\n'
             # 'display: table-header-group;\n'
             'color: #fff;\n'
             '}\n')
    html += ('table tbody tr:nth-child(odd){\n'
             'background-color: #eee;\n'
             '}\n')
    html += ('table tbody tr:hover{\n'
             'background-color: #ccc;\n'
             '}\n')
    html += '</style>\n'
    html += '<script>\n'
    html += '</script>\n' \
            '</head>\n'

    # 开始写入数据
    html += '<table>\n<thead>\n<tr>\n'
    for header in headers:
        html += f'<th>{header}</th>\n'
    html += ('</tr>\n</thead>\n'
             '<tbody>\n')
    html += f'<caption  >{date.tm_year}年{date.tm_mon}月{date.tm_mday}日接口自动化测试执行报告\n'
    html += (
        # f'<p style="background-color: #CCFFCC; color: {caption_color};font-size: 25px" >'
        # f'今日共计执行{len(rows)}条用例，通过率为{"%0.2f" % (pass_precent * 100)}%</p>\n'
        f'今日共计执行{len(rows)}条用例，通过率为{"%0.2f" % (pass_precent * 100)}%\n'
        '</caption>\n')

    for row in rows:
        if not row:
            continue
        if row[7] == "true":
            html += '<tr  >\n'
        else:
            html += '<tr  style="background-color: #ffa07a;">\n'
        for cell in row:
            # html += f'<td >{cell}</td>\n'
            html += f'<td >{cell}</td>\n'
        html += '</tr>\n'
    html += '</tbody>\n</table>\n'

    return html


def make_table(file_path: str, getting_index: list):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line[0] == '*' or line == '':
                continue
            line_data = line.strip().split(",")
            data.append(line_data)
    # 生成HTML表格
    for i in range(len(data)):
        if len(data[i]) == 1:
            data[i] = None

    table = PrettyTable()
    # print(data)
    table.field_names = [data[0][i] for i in getting_index]

    for i in data[1::]:
        if i is not None and len(i) == len(data[0]):
            i[0] = time.strftime("%Y年%m月%d日%H:%M:%S", time.localtime(int(int(i[0]) / 1000)))
            list_ready = [i[j] for j in getting_index]
            table.add_row(list_ready)
    return table

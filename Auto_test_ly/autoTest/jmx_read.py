import re
from xml.etree.ElementTree import parse

jmx_txt = parse(r'D:\PY_pros\pythonProject\autoTest\maoyan.jmx')
root = jmx_txt.getroot()

class_list = ['ArgumentsPanel', 'ThreadGroupGui', 'TestFragmentControllerGui', 'HttpDefaultsGui']
# 参数定义列表
arguments_panel = {}
# 测试组件列表
thread_group_gui_list = []
# 接口控件列表
test_fragment_controller_gui = {}
# http默认参数列表
HttpDefaultsGui = {}

model_list = [arguments_panel, thread_group_gui_list, test_fragment_controller_gui, HttpDefaultsGui]
ready_list = None
ready_name = None
ready_value = None
ready_domain = None
ready_protocol = None
ready_path = None
ready_method = None
class_flag = None
ready_test_name = None
token_name = None
token_value = None
cookie_name = None
cookie_value = None
# 用例临时存储处理器信息
ready_BoundaryExtractorGui = None

# 用于临时处理测试套件中的模型信息
ready_Module_dict = {}
module_count = 0
# 测试模型中的接口数据,数据结构如下
# test_fragment_controller_gui=[
#                   {
#                       module_name:{
#                           module_test_name:[
#                               "HTTPSampler.path":HTTPSampler.path
#                               "HTTPSampler.follow_redirects":HTTPSampler.follow_redirects
#                               "HTTPSampler.method":HTTPSampler.method
#                               "HTTPsampler.Arguments":
#                                   {
#                                   Arguments.name:"Argument.value"
#                                   }
#                               ]}}]
# temp_module_dict = []
module_name = None
module_test_name = None
HTTPSampler_path = None
HTTPSampler_postBodyRaw = None
HTTPSampler_follow_redirects = None
HTTPSampler_method = None
Arguments_name = None
Arguments_value = None

# 该变量用于获取JSON提取器
ready_jsonpostprocessor = {}
# 这个变量是因为在获取test_fragment_controller_gui的时候发现JSON的model_num竟然可以是空的，要区分过于扯淡了所以定义的
json_got_flag = False
# 该变量用于统计接口的固定定时器
constant_timer_gui = {}

# 该变量用于记录响应断言信息
assertion_gui = []

# 该变量用于在test_fragment_controller_gui的每个字典中，确定当前接口的位置
group_num = -1

for child in root.iter():
    def json_post_process(data, dict_json):

        if data.attrib.get('guiclass') is not None and data.attrib.get('guiclass') == "JSONPostProcessorGui":
            # print(data.attrib)
            dict_json = {}
            # print(dict_json)
            return dict_json
        if data.tag == 'stringProp' and data.attrib.get('name') == "JSONPostProcessor.referenceNames":
            # print(data.attrib)
            dict_json['referenceNames'] = data.text
            # print(dict_json)
            return dict_json
        if data.tag == 'stringProp' and data.attrib.get('name') == "JSONPostProcessor.jsonPathExprs":
            # print(data.attrib)
            dict_json['jsonPathExprs'] = data.text
            # print(dict_json)
            return dict_json
        if data.tag == 'stringProp' and data.attrib.get('name') == "JSONPostProcessor.match_numbers":
            # print(data.attrib)
            dict_json['match_numbers'] = data.text
            # print(dict_json)
            global json_got_flag
            json_got_flag = True
            return dict_json


    # 这里为了判断是不是一个要找的参数/接口的开始
    child_class = child.attrib.get('guiclass')
    # 如果这一行有class,且在列表中，那么就代表要找属性了
    if child_class is not None and child_class in class_list:
        ready_name = None
        ready_value = None
        if child_class == 'ArgumentsPanel':
            class_flag = 'ArgumentsPanel'
            ready_list = model_list[0]
        elif child_class == 'ThreadGroupGui':
            class_flag = 'ThreadGroupGui'
            ready_test_name = child.get('testname')
            ready_list = model_list[1]
            ready_list.append(ready_test_name)
        elif child_class == 'TestFragmentControllerGui':
            # if module_name is not None and module_name != child.attrib.get('testname'):
            #     ready_list[module_name] = temp_module_dict[module_name]
            module_name = child.attrib.get('testname')
            module_test_name = None
            HTTPSampler_path = None
            HTTPSampler_postBodyRaw = None
            HTTPSampler_follow_redirects = None
            HTTPSampler_method = None
            Arguments_name = None
            Arguments_value = None

            class_flag = 'TestFragmentControllerGui'
            ready_list = model_list[2]

            # print(module_name)
            # temp_module_dict = {module_name: []}
            ready_list[module_name] = []

            group_num = -1

        # elif child_class == 'HttpDefaultsGui':
        #     class_flag = 'HttpDefaultsGui'
        #     ready_list = model_list[3]
        continue

    # 开始存入ArgumentsPanel的部分
    if class_flag == 'ArgumentsPanel':
        if child.tag == 'stringProp' and ready_value is None:
            if child.get('name') == "Argument.name":
                ready_name = child.text
            if child.get('name') == "Argument.value":
                ready_value = child.text
        if ready_name is not None and ready_value is not None:
            ready_list[ready_name] = ready_value
            ready_name = None
            ready_value = None

    # 开始存入ThreadGroupGui的部分
    elif class_flag == 'ThreadGroupGui':
        if child.tag == 'stringProp' and child.get('name') in ["Argument.name", "Argument.value"]:
            if child.get('name') == "Argument.name":
                ready_name = child.text
            if child.get('name') == "Argument.value":
                ready_value = child.text
        if ready_name is not None and ready_value is not None:
            ready_list.append({ready_name: ready_value})
            ready_name = None
            ready_value = None

        if child.tag == 'stringProp' and child.get('name') == "Argument.value":
            if child.text is not None and child.text[0] == '{' and child.text[-1] == '}':
                ready_list.append({'payload': child.text.replace(' ', '').replace('/r', '').replace('/n', '')})

        if child.tag == 'stringProp' and child.get('name') == "HTTPSampler.domain":
            ready_domain = child.text
            ready_list.append({'HTTPSampler.domain': ready_domain})
            ready_domain = None
        if child.tag == 'stringProp' and child.get('name') == "HTTPSampler.protocol":
            ready_protocol = child.text
            ready_list.append({'HTTPSampler.protocol': ready_protocol})
            ready_protocol = None
        if child.tag == 'stringProp' and child.get('name') == "HTTPSampler.path":
            ready_path = child.text
            ready_list.append({'HTTPSampler.path': ready_path})
            ready_path = None
        if child.tag == 'stringProp' and child.get('name') == "HTTPSampler.method":
            ready_method = child.text
            ready_list.append({'HTTPSampler.method': ready_method})
            ready_method = None

        # 参数中加入token，cookie
        if child.tag == 'stringProp' and child.get('name') in ["Header.name", "Header.value"]:
            if child.text == "token":
                token_name = child.text
            elif child.text == "${token}":
                token_value = child.text
            elif child.text == "Cookie":
                cookie_name = child.text
            elif cookie_name is not None and cookie_value is None:
                cookie_value = child.text
        if token_name is not None and token_value is not None:
            ready_list.append({token_name: token_value})
            token_name = None
            token_value = None
        if cookie_name is not None and cookie_value is not None:
            ready_list.append({cookie_name: cookie_value})
            cookie_name = None
            cookie_value = None

        # 边界值提取器
        if child.attrib.get('guiclass') == "BoundaryExtractorGui":
            ready_BoundaryExtractorGui = {}
        if child.tag == 'stringProp' and child.get('name') == "BoundaryExtractor.useHeaders":
            ready_BoundaryExtractorGui['useHeaders'] = child.text
        if child.tag == 'stringProp' and child.get('name') == "BoundaryExtractor.refname":
            ready_BoundaryExtractorGui['refname'] = child.text
        if child.tag == 'stringProp' and child.get('name') == "BoundaryExtractor.lboundary":
            ready_BoundaryExtractorGui['lboundary'] = child.text
        if child.tag == 'stringProp' and child.get('name') == "BoundaryExtractor.rboundary":
            ready_BoundaryExtractorGui['rboundary'] = child.text
        if (ready_BoundaryExtractorGui is not None and ready_BoundaryExtractorGui.get('useHeaders') is not None
                and ready_BoundaryExtractorGui.get('refname') is not None
                and ready_BoundaryExtractorGui.get('lboundary') is not None
                and ready_BoundaryExtractorGui.get('rboundary') is not None):
            ready_list.append(ready_BoundaryExtractorGui)
            ready_BoundaryExtractorGui = None

        # JSON 提取器
        ready_jsonpostprocessor = json_post_process(child, ready_jsonpostprocessor)
        if (ready_jsonpostprocessor is not None
                and ready_jsonpostprocessor.get('referenceNames') is not None
                and ready_jsonpostprocessor.get('jsonPathExprs') is not None
                and ready_jsonpostprocessor.get('match_numbers') is not None):
            ready_list.append(ready_jsonpostprocessor)
            ready_jsonpostprocessor = {}

        # 模型测试套件管理
        if child.attrib.get('guiclass') is not None and child.get('guiclass') == 'ModuleControllerGui':
            if ready_Module_dict != {} and module_count == 4:
                ready_list.append({'Module': ready_Module_dict})
                module_count = 0
            ready_Module_dict = {}
            ready_test_name = child.get('testname')
            ready_Module_dict[ready_test_name] = child.get('name')
            module_count += 1
        if child.tag == 'stringProp' and child.get('name') is not None and re.match(pattern=r'^\d+$',
                                                                                    string=child.get('name')):
            ready_Module_dict[ready_test_name] = child.text
            module_count += 1

    elif class_flag == 'TestFragmentControllerGui':
        # print('child:', child.attrib, 'child.text:', child.text)
        if child.attrib.get('guiclass') is not None and child.attrib.get('guiclass') == 'HttpTestSampleGui':
            group_num += 1
            module_test_name = child.attrib.get('testname')
            if ready_list[module_name]:
                # ready_list[module_name].append(temp_module_dict[module_name])
                ready_list[module_name].append({module_test_name: []})
                # print('999', temp_module_dict)
            else:
                ready_list[module_name].append({module_test_name: []})
            # print('111', temp_module_dict)
        if child.tag == 'stringProp' and child.attrib.get('name') == "HTTPSampler.path":
            ready_list[module_name][group_num][module_test_name].append({"HTTPSampler.path": child.text})
            # print('222', temp_module_dict)
        if child.tag == 'boolProp' and child.attrib.get('name') == "HTTPSampler.follow_redirects":
            ready_list[module_name][group_num][module_test_name].append(
                {"HTTPSampler.follow_redirects": child.text})
            # print('333', temp_module_dict)
        if child.tag == 'stringProp' and child.attrib.get('name') == "HTTPSampler.method":
            ready_list[module_name][group_num][module_test_name].append({"HTTPSampler.method": child.text})
            # print('444', temp_module_dict)
        if child.tag == 'boolProp' and child.attrib.get('name') == "HTTPSampler.postBodyRaw":
            HTTPSampler_postBodyRaw = child.text.replace(' ', '').replace('\r', '').replace('\n', '')
            # print('555', temp_module_dict)
        if child.tag == 'stringProp' and child.attrib.get(
                'name') == "Argument.value" and HTTPSampler_postBodyRaw == 'true':
            ready_list[module_name][group_num][module_test_name].append(
                {"payload": child.text.replace(' ', '').replace('\r', '').replace('\n', '')})
            # print('666',temp_module_dict)
        elif (child.tag == 'stringProp' and child.attrib.get('name') in
              ["Argument.value", "Argument.name"] and HTTPSampler_postBodyRaw == 'false'):
            if child.attrib.get('name') == "Argument.value":
                Arguments_value = child.text
            elif child.attrib.get('name') == "Argument.name":
                Arguments_name = child.text
            if Arguments_value is not None and Arguments_name is not None:
                ready_list[module_name][group_num][module_test_name].append({Arguments_name: Arguments_value})
                Arguments_value = None
                Arguments_name = None

        # 固定定时器获取
        if child.attrib.get('guiclass') and child.attrib.get('guiclass') == "ConstantTimerGui":
            constant_timer_gui = {}
        if child.tag == 'stringProp' and child.attrib.get('name') == "ConstantTimer.delay":
            constant_timer_gui['固定定时器'] = [child.attrib.get('name'), child.text]
            ready_list[module_name][group_num][module_test_name].append(constant_timer_gui)
            constant_timer_gui = {}

        # 响应断言
        if child.attrib.get('guiclass') and child.attrib.get('guiclass') == "AssertionGui":
            assertion_gui.append(child.attrib.get('testname'))
        if child.tag == 'collectionProp' and child.attrib.get('name') and 'Assertion' in child.attrib.get('name'):
            assertion_gui.append(child.attrib.get('name'))
        if child.tag == 'stringProp' and child.attrib.get('name') and re.match(pattern=r'^\d+$',
                                                                               string=child.get('name')):
            assertion_gui.append(child.text)
        if child.tag == 'stringProp' and child.attrib.get('name') and child.attrib.get(
                'name') == 'Assertion.test_field':
            assertion_gui.append(child.text)
        if child.tag == 'boolProp' and child.attrib.get('name') and child.attrib.get(
                'name') == 'Assertion.assume_success':
            assertion_gui.append(child.text)
        if child.tag == 'intProp' and child.attrib.get('name') and child.attrib.get(
                'name') == 'Assertion.test_type':
            assertion_gui.append(child.text)
            ready_list[module_name][group_num][module_test_name].append(assertion_gui)
            assertion_gui = []

        # JSON 提取器
        ready_jsonpostprocessor = json_post_process(child, ready_jsonpostprocessor)
        if ready_jsonpostprocessor is not None and json_got_flag:
            ready_list[module_name][group_num][module_test_name].append(ready_jsonpostprocessor)
            ready_jsonpostprocessor = {}
            json_got_flag = False

    elif class_flag == 'HttpDefaultsGui':
        pass

#
# print('arguments_panel:')
# for i in arguments_panel:
#     print('\t', str(i) + ':', arguments_panel[i])
# print('====================================================')
# print('====================================================')
# print('thread_group_gui_list:')
# for i in thread_group_gui_list:
#     if type(i) is dict and 'HTTPSampler.domain' in i.keys():
#         print('     ===============================================')
#     print('\t', i)
# print('====================================================')
# print('====================================================')
# print('test_fragment_controller_gui:')
# print(test_fragment_controller_gui)
# for i in test_fragment_controller_gui.keys():
#     print(i)
# print(test_fragment_controller_gui[i])
# for j in test_fragment_controller_gui[i]:
#     print(j)
# if i == '数据集':
# for j in test_fragment_controller_gui[i]:
#     print(j)

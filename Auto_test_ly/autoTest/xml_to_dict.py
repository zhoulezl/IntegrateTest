import json

import xmltodict


def find_false():
    marking_result_list = {}
    with open(r'api_jmeter\openmind\model\basetest\20240727.xml', 'r', encoding='utf-8') as f:
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
                print(marking_result[-1])
                marking_result_list[marking_result[1] + marking_result[0] + 'args'] = marking_result[-1].replace(r'\n',
                                                                                                                 '  ')

            else:
                marking_result_list[marking_result[1] + marking_result[0] + 'error_msg'] = marking_result[-1].replace(
                    r'\n', '  ')
            marking_result_list[marking_result[1] + marking_result[0] + 'request_way'] = marking_result[2]
    print(marking_result_list)
    return marking_result_list


find_false()

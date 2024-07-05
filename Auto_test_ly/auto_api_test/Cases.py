import json

import requests


class Case:
    """
        todo
            self.case_name = case[0]
            self.case_id = case[1]
            self.case_pre_apis = 测试的接口列表
            self.case_pre_api_reqways = 每个接口的请求方式
            self.case_pre_api_resargs = 每个接口的请求参数
            self.case_sql_inneed = 是否需要执行sql
            self.case_sql_connection = 数据库连接信息
            self.case_sql_query = sql语句
            self.case_assert = 断言条件
            self.case_after_apis = 测后接口列表
            self.case_after_api_reqways = 测后接口请求方式
            self.case_after_api_resargs = 测后接口请求参数列表
            self.case_designer = 案例设计人
            self.case_design_time = 案例设计时间
            self.case_isdone = False    接口是否执行
            self.case_status = False    测试是否通过
    """

    def __init__(self, case):
        self.case_name = case[0]
        self.case_id = case[1]
        self.case_pre_apis = case[2]
        self.case_pre_api_reqways = case[3]
        self.case_pre_api_reqargs = case[4]
        # self.case_sql_inneed = case[5]
        # self.case_sql_connection = case[6]
        # self.case_sql_query = case[7]
        self.case_assert = case[5]
        self.case_after_apis = case[6]
        self.case_after_api_reqways = case[7]
        self.case_after_api_reqargs = case[8]
        self.case_designer = case[9]
        self.case_design_time = case[10]
        self.case_isdone = False
        self.case_status = False

    def __str__(self):
        return self.case_name

    def do_pre_request(case):
        request_list = []
        if len(case.case_pre_apis) == len(case.case_pre_api_reqways) == len(case.case_pre_api_reqargs):
            # 将case的请求进行整理
            for i in range(len(case.case_pre_apis)):
                request_list.append([])
                request_list[i].append(case.case_pre_apis[i])
                request_list[i].append(case.case_pre_api_reqways[i])
                request_list[i].append(case.case_pre_api_reqargs[i])
            # print(case.case_name,request_list)
            '''
            # 发送GET请求
            response = requests.get('https://api.example.com/data')
            print(response.json())

            # 发送POST请求
            payload = {'key1': 'value1', 'key2': 'value2'}
            response = requests.post('https://api.example.com/submit', data=payload)
            print(response.text)
            '''
            for res_test in request_list:
                if res_test[1] == 'POST':
                    payload = json.loads(res_test[2])
                    res_test_response = requests.post(res_test[0], json=payload, headers={})
                    res_test.append(res_test_response)
                    print(case.case_name, ":\n", res_test[0], "\n", res_test_response.text)
                elif res_test[1] == 'GET':
                    pass
                else:
                    print("请求方式编写有误")
        else:
            print("案例接口-请求方式-请求参数长度不一致!")
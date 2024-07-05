"""
    1.获取当前目录下的自动化测试文件，放置在文件列表：caseFiles[]
    2.在文件列表中依次获取页列表，放置在页列表 caseSheets中
    3.从第2行开始按行读取数据，每行读取的格式为：
        {
           用例名称:
           用例编号:
           前置条件:
                前置需要执行的接口，如涉及权限类的接口访问需要鉴权
           前置条件参数:
                {
                    XXX:XXX
                     .....
                }
           测试接口:
                待测接口的URL
           测试接口参数:
                {
                    XXX:XXX
                     .....
                }
           是否需要验证sql:
                是/否
           数据库连接信息:
                {
                    主机名:XXX
                    用户名:XXX
                    端口:XXX
                    口令:XXX
                }
           验证sql:
                查询类接口需要与直接执行sql的结果进行比对
           断言条件:
                不需要验证sql时，确定接口测试的结果
           用例设计人:
           用例设计时间:
        }
"""
import requests
import os




#todo 2.在文件列表中依次获取页列表，放置在页列表 caseSheets中
class AutoTestFile:
    def __init__(self, caseFlie):
        self.caseFlie = caseFlie

    #取得全部页
    def __getSheets(self, caseFlie):
        pass

    #计算通过率
    def __getPassRate(self):
        pass


#3.todo 通过页名，取得每页的全部case
class CaseSheet:
    def __init__(self, caseSheet):
        self.caseSheet = caseSheet

    #取得当前页全部case
    def __getCases(self):
        pass

    #取得当前页case数量
    def __getCaseNum(self):
        pass

    def __getPassNum(self):
        pass

    def __getPassRate(self):
        pass


#todo 每条case的执行
class Case:
    def __init__(self, caseList):
        self.caseName = caseList[0]
        self.caseID = caseList[1]
        self.casePreInterfaceList = caseList[2]
        self.caseSqlInNeed = caseList[3]
        self.caseSqlCondition = list(caseList[4])
        self.caseSql = caseList[5]
        self.caseAssert = caseList[6]
        self.caseAfterInterfaceList = caseList[7]
        self.caseDesigner = caseList[8]
        self.caseDesignTime = caseList[9]
        self.caseIsPass = False

        #初始化时直接执行，同时给caseIsPass字段赋值
        def __caseTesting(self):
            pass

        self.caseTesting()
if __name__ == '__main__':
    # todo 1.获取当前目录下的自动化测试文件，放置在文件列表：caseFiles[]
    caseFlies = []
    for root, dirs, files in os.walk('.', topdown=False):
        for name in files:
            str = os.path.join(root, name)
            if str.split('.')[-1] == 'xlsx':
                caseFlies.append(str.split('.\\')[1])
    print(caseFlies)
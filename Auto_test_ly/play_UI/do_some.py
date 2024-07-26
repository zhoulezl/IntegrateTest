import time

import operation_dict
from playwright.sync_api import sync_playwright
import case_list


# 这里是个类似反射的方法，用于按照名称来调用函数
def call_function_by_name(func_name, *args, **kwargs):
    module_name = __import__('operation_dict')
    be_called_function = getattr(module_name, func_name)
    be_called_function(*args, **kwargs)


if __name__ == '__main__':

    file_path = 'UI自动化测试案例.xlsx'
    # 启动 playwright driver 进程
    p = sync_playwright().start()
    # 启动浏览器，返回 Browser 类型对象
    executable_path = r'C:\Users\Administrator\AppData\Local\ms-playwright\chromium-1117\chrome-win\chrome.exe'
    browser = p.chromium.launch(headless=False, executable_path=executable_path)
    # 创建新页面，返回 Page 类型对象
    # 创建 BrowserContext对象
    context = browser.new_context()
    # 启动跟踪功能
    context.tracing.start(snapshots=True, sources=True, screenshots=True)

    case_list = case_list.get_case_list(file_path)
    for case in case_list:
        print(case)
        page = context.new_page()
        def_names = case[1]
        for def_name in def_names:
            print(' ', def_name)
            try:
                if type(def_name) is str:
                    call_function_by_name(operation_dict.def_dict[def_name].__name__, page)
                elif type(def_name) is list:
                    call_function_by_name(operation_dict.def_dict[def_name[0]].__name__, page, def_name[1].split(','))
            except Exception as e:
                print(e)
            finally:
                time.sleep(2)
        page.close()
    # 结束跟踪
    context.tracing.stop(path="trace.zip")

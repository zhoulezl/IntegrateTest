import os
import threading
import time

import modelers_operation_dict
import openSoftware_operation_dict
from playwright.sync_api import sync_playwright
import case_list
import openEuler_operation_dict
from config import YamlHandler
from send_email import send_mail
import video_maker

import tkinter as tk
import tkinter.messagebox

running_home = r"D:\pythonPro\IntegrateTest"
# 读取配置文件
config_list = YamlHandler(rf'{running_home}\本地play_UI _easySoftWare\config\config.yaml').read_yaml()


# 这里是个用于打印当前执行case的窗口方法
def show_message(content, delay=1500):
    # 创建根窗口（这里设置为不可见）
    root = tk.Tk()
    root.withdraw()
    # 创建一个顶层窗口来模拟消息框（因为标准的messagebox不支持自动关闭）
    top = tk.Toplevel(root)
    top.title("打印内容")
    top.geometry("800x200")  # 设置窗口大小
    # 创建一个Label来显示内容
    label = tk.Label(top, text=content, font=("Helvetica", 15), compound="center", justify="center")
    label.pack(pady=20)  # 添加一些内边距

    # 使用after方法安排窗口关闭
    def close_window():
        top.destroy()
        root.destroy()  # 同时销毁根窗口

    top.after(delay, close_window)  # 延迟delay毫秒后执行close_window
    # 进入事件循环（虽然这里我们不会手动干预它，因为窗口会自动关闭）
    root.mainloop()


# 这里是个类似反射的方法，用于按照名称来调用函数
def call_function_by_name(func_name, *args, **kwargs):
    module_name = __import__(config_list[key]['operation_dict'])
    be_called_function = getattr(module_name, func_name)
    return be_called_function(*args, **kwargs)


def do_test():
    # 开始先睡3秒，用于录制线程启动
    time.sleep(1)
    case_lists = case_list.get_case_list(running_home + config_list[key]['test_case'])

    page = context.new_page()
    # page.wait_for_load_state('domcontentloaded')
    page.set_default_timeout(20000)
    page.set_viewport_size({'width': 1880, 'height': 1000})
    i = 1

    for case in case_lists:
        context.clear_cookies()
        context.clear_permissions()
        print('-----开始执行测试-----')
        time_now = time.strftime("%H:%M:%S", time.localtime())
        # context.tracing.start_chunk(title=case[0], name=case[0])
        print(f'测试用例{i:03}', case)
        def_names = case[1]
        for def_name in def_names:
            print(' ', def_name)
            show_message((f'测试用例{i:03}', def_name))
            err = None
            try:
                page.set_viewport_size({'width': 1880, 'height': 1000})

                if key == 'openSoftware':
                    if type(def_name) is str:
                        page = call_function_by_name(openSoftware_operation_dict.def_dict[def_name].__name__, page)
                    elif type(def_name) is list:
                        page = call_function_by_name(openSoftware_operation_dict.def_dict[def_name[0]].__name__,
                                                     page,
                                                     def_name[1].split(','))
                elif key == 'modelers':
                    if type(def_name) is str:
                        page = call_function_by_name(modelers_operation_dict.def_dict[def_name].__name__, page)
                    elif type(def_name) is list:
                        page = call_function_by_name(modelers_operation_dict.def_dict[def_name[0]].__name__, page,
                                                     def_name[1].split(','))
                elif key == 'openEuler':
                    if type(def_name) is str:
                        page = call_function_by_name(openEuler_operation_dict.def_dict[def_name].__name__, page)
                    elif type(def_name) is list:
                        page = call_function_by_name(openEuler_operation_dict.def_dict[def_name[0]].__name__, page,
                                                     def_name[1].split(','))
            except Exception as e:
                err = e
            finally:
                time.sleep(1)
                if err is not None and "Call log:" in str(err):
                    # if err != "":
                    #     err = str(err).split('  -   ')[0:2]
                    #     err = err[0]
                    # elif str(err) == "\'\'":
                    #     pass
                    if type(def_name) is list:
                        case.append(f'{def_name[0]} 测试失败:{err}')
                        print(err)
                    elif type(def_name) is str:
                        case.append(f'{def_name} 测试失败:{err}')
                        print(err)
                    break
        if '测试失败' in case[-1]:
            pass
        else:
            case.append('测试通过')
        # 保存当前案例追踪截图
        case.insert(0, f'测试用例{i:03}')
        case.insert(0, time_now)
        # context.tracing.stop_chunk(path=f'records/traces/{case[1]}.zip')
        i += 1
        context.clear_cookies()
        context.clear_cookies()

        context.clear_permissions()
        context.clear_permissions()
    page.close()

    # 保存测试录像
    # page.video.save_as(f'records/videos/{video_name}' + '.mp4')
    # 结束跟踪
    # context.tracing.stop(path=f'records/traces/video_name.zip')

    for case in case_lists:
        operations = case[3]
        for i in range(len(operations)):
            if type(operations[i]) is list:
                # operations[i] = operations[i][0]
                operations[i] = str(operations[i][0] + '(' + operations[i][1] + ')')
            operations[i] += '\n'
        case[3] = operations
    return case_lists


if __name__ == '__main__':
    # print(config_list.keys())
    p = sync_playwright().start()
    # 启动浏览器，返回 Browser 类型对象
    # executable_path = browser_path
    # browser = await async_playwright().chromiun
    # browser = p.chromium.launch(headless=False)
    # 创建新页面，返回 Page 类型对象
    # 创建 BrowserContext对象
    date = time.localtime()
    video_name = f"{date.tm_year}年{date.tm_mon}月{date.tm_mday}日UI自动化测试"
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(record_video_size={"width": 1920, "height": 1080})
    for key in config_list.keys():
        # print(key)
        # continue

        # if key == 'openSoftware':
        #     continue

        # browser_path = config.get('DEFAULT', 'browser_path')
        # file_path = config.get('DEFAULT', 'file_path')
        # 启动 playwright driver 进程
        # 启动跟踪功能
        # context.tracing.start(snapshots=True, screenshots=True, title='测试记录',)
        # 测试案例路径
        # case_list = case_list.get_case_list(r'D:\PyPros\本地play_UI\test_cases\测试用例.xlsx')

        # 用于储存do_test方法返回的case_lists

        # 测试图片和视频保存路径
        test_result_folder = fr"{running_home}\本地play_UI _easySoftWare\test_records\{key}"
        # 初始化录制对象
        vm = video_maker.VideoMaker()
        vm.test_fini = False
        # 启动录制线程
        make_screenshot_args = (test_result_folder,)
        make_screenshot_thread = threading.Thread(target=vm.make_screenshot, args=make_screenshot_args)
        make_screenshot_thread.start()
        case_lists = do_test()
        vm.test_fini = True
        make_screenshot_thread.join()
        # 测试完毕，生成视频，发送邮件

        vm.make_video(test_result_folder,
                      fr"{test_result_folder}\{key}平台{date.tm_year}年{date.tm_mon}月{date.tm_mday}日UI自动化测试.mp4")
        send_mail(case_lists, key)
    context.close()
    browser.close()
    for filename in os.listdir(fr"{running_home}\本地play_UI _easySoftWare\test_records\modelers"):
        os.remove(os.path.join(fr"{running_home}\本地play_UI _easySoftWare\test_records\modelers", filename))
    for filename in os.listdir(fr"{running_home}\本地play_UI _easySoftWare\test_records\openSoftware"):
        os.remove(os.path.join(fr"{running_home}\本地play_UI _easySoftWare\test_records\openSoftware", filename))
    for filename in os.listdir(fr"{running_home}\本地play_UI _easySoftWare\test_records\openEuler"):
        os.remove(os.path.join(fr"{running_home}\本地play_UI _easySoftWare\test_records\openEuler", filename))

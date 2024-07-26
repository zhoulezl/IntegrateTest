import inspect
import time
import pyautogui
from playwright import sync_api
from playwright.sync_api import expect


def shot(page, name, count):
    local_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    shot_path = fr'D:\PY_pros\IntegrateTest\Auto_test_ly\test\shots\{local_date}OpenMind自动化测试截图'
    page.screenshot(path=fr'{shot_path}\{name}_{count}.png')


def tag_list_operation(arglist):
    res_list = []
    for arg in arglist:
        if ':' in arg:
            arg = arg.split(':')
            arg[1] = arg[1].replace('}', '').replace('{', '').split('|')
        res_list.append(arg)
    return res_list


def login_sh(page: sync_api.Page):
    # screenshot_count = 1
    # name = inspect.currentframe().f_code.co_name
    # expect(page.locator('#e2e_header_isLogined')).not_to_be_attached()
    page.goto("https://openmind.test.osinfra.cn/")
    # shot(page, name, screenshot_count)
    # screenshot_count += 1
    page.wait_for_selector('#e2e_login_account')
    page.locator('#e2e_login_account').fill('18801113053')
    # shot(page, name, screenshot_count)
    # screenshot_count += 1
    page.locator('#e2e_login_password').fill('66liuyu!')
    # shot(page, name, screenshot_count)
    # screenshot_count += 1
    page.click('#e2e_login_submit')
    page.wait_for_timeout(2000)
    if not page.locator('#e2e_header_isLogined'):
        login_sh(page)



def hover_user_img(page: sync_api.Page):
    screenshot_count = 1
    name = inspect.currentframe().f_code.co_name
    page.hover('#e2e_header_isLogined')
    page.wait_for_timeout(200)
    # shot(page, name, screenshot_count)


def hover_create_organization(page: sync_api.Page, arglist: list):
    screenshot_count = 1
    name = inspect.currentframe().f_code.co_name
    page.locator('#e2e_headerUser_newOrg').hover()
    # shot(page, name, screenshot_count)
    page.locator('#e2e_headerUser_newOrg').click()
    # shot(page, name, screenshot_count)
    page.locator('#e2e_newOrg_nameInput').fill(arglist[0])
    page.locator('#e2e_newOrg_fullnameInput').fill(arglist[1])
    page.locator('.o-upload-input').all()[0].set_input_files('favicon.png')
    page.locator('.o-textarea-textarea').fill(arglist[3])
    page.get_by_placeholder("关联组织官网或GitHub地址").fill(arglist[4])
    # shot(page, name, screenshot_count)
    page.locator('#e2e_newOrg_submitBtn').click()
    page.wait_for_timeout(500)


def hover_create_model(page: sync_api.Page, arglist: list):
    # name = inspect.currentframe().f_code.co_name
    page.locator('#e2e_headerUser_newModel').hover()
    page.locator('#e2e_headerUser_newModel').click()
    # 填入参数
    page.locator('#e2e_newModels_nameInput').fill(arglist[0])
    page.get_by_placeholder("请填写模型别名").fill(arglist[1])
    if arglist[2] == '私有模型':
        page.get_by_text('私有模型').click()
    elif arglist[2] == '公开模型':
        page.get_by_text('公开模型').click()
    page.locator('#e2e_newModels_licenseSelect').click()
    page.get_by_text(arglist[3], exact=True).click()
    page.locator('#e2e_newModels_submitBtn').click()
    page.wait_for_timeout(500)
    # input()


def enter_user_center(page: sync_api.Page):
    name = inspect.currentframe().f_code.co_name
    # 进入个人中心
    page.locator('#e2e_headerUser_center').hover()
    page.locator('#e2e_headerUser_center').click()
    page.wait_for_timeout(500)


def show_my_models(page: sync_api.Page):
    name = inspect.currentframe().f_code.co_name
    page.locator('#e2e_myAside_creation').click()
    page.get_by_text('我的模型').click()
    page.wait_for_timeout(500)


def show_point_model(page: sync_api.Page, arglist: list):
    print(arglist)
    name = inspect.currentframe().f_code.co_name
    page.locator('.title').get_by_text(arglist[0]).click()
    page.wait_for_timeout(500)


def delete_current_model(page: sync_api.Page):
    name = inspect.currentframe().f_code.co_name
    page.locator('.o-tab-nav').get_by_text('设置').click()
    page.locator('#e2e_deleteModel_inputValidation').fill('我已知晓，并确认删除模型')
    page.locator('#e2e_deleteModel_deleteBtn').click()


def logout(page: sync_api.Page):
    name = inspect.currentframe().f_code.co_name
    hover_user_img(page)
    page.get_by_text('退出登录').click()
    page.wait_for_timeout(1500)


def edit_model_tags(page: sync_api.Page, arglist: list):
    name = inspect.currentframe().f_code.co_name
    arglist = tag_list_operation(arglist)
    expect(page.locator('.o-btn.o-btn-primary.o-btn-large.o-btn-solid.use-openmind')).not_to_be_attached()
    page.get_by_text('编辑标签').click()
    for arg in arglist:
        if type(arg) is list:
            page.get_by_placeholder(tag_dict[arg[0]]).click()
            page.wait_for_timeout(200)
            for index in range(len(arg[1])):
                page.wait_for_timeout(200)
                page.locator('.o-option').get_by_text(arg[1][index], exact=True).click()
    page.get_by_text('提交').click()
    page.get_by_placeholder('Update README.md').fill(arglist[-1])
    page.locator('.o-btn.o-btn-primary.o-btn-large.o-btn-solid.o-dlg-btn').get_by_text('提交').click()
    page.wait_for_timeout(200)



def create_file(page: sync_api.Page, arglist: list):
    name = inspect.currentframe().f_code.co_name
    page.locator('.o-tab-nav').get_by_text('文件').click()
    page.get_by_text('新建文件').click()
    page.get_by_placeholder('请输入文件名').fill(arglist[0])
    page.locator('.view-line').click()
    pyautogui.write(arglist[1])  # ???什么类型啊这个元素vocal，整不会了
    # page.locator('.mtk7').fill(arglist[1],force=True)
    page.locator('.o-btn.o-btn-primary.o-btn-large.o-btn-solid.upload').get_by_text('提交').click()
    page.locator('.o-textarea-textarea').fill(arglist[2])
    page.locator('.o-btn.o-btn-primary.o-btn-large.o-btn-solid.o-dlg-btn').get_by_text('提交').click()
    page.wait_for_timeout(500)


def delete_file(page: sync_api.Page, arglist: list):
    name = inspect.currentframe().f_code.co_name
    page.locator('.o-tab-nav').get_by_text('文件').click()
    page.get_by_title(arglist[0]).click()
    # page.locator('.hover-stress').get_by_title(arglist[0]).click()
    page.locator('.hover-stress').get_by_text('删除').click()
    page.wait_for_timeout(500)
    page.locator('.o-btn.o-btn-primary.o-btn-large.o-btn-solid.o-dlg-btn').get_by_text('删除').click()
    page.wait_for_timeout(500)


def_dict = {'登录sh环境': login_sh,
            '鼠标悬停在个人头像上': hover_user_img,
            '悬停方式创建组织': hover_create_organization,
            '悬停方式创建模型': hover_create_model,
            '进入个人中心': enter_user_center,
            '查看我创建的模型': show_my_models,
            '查看指定模型': show_point_model,
            '删除当前模型': delete_current_model,
            '退出登录': logout,
            '编辑模型标签': edit_model_tags,
            '新建文件': create_file,
            '删除文件': delete_file,
            }
tag_dict = {'pipeline_tag': '新增标签',
            'frameworks': '新增框架',
            'license': '新增许可证',
            ' library_name ': '新增库',
            'hardwares': '新增硬件',
            'language': '新增语言'}

# import inspect
import re
import time
# import pyautogui
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


# 进入环境
# 首次登录环境
def login_first(page: sync_api.Page, arglist: list):
    page = login_common(page, arglist)
    page.get_by_text("跳过").click()
    page.get_by_role("button", name="全部接受").click()
    return page


# 登录环境
def login_common(page: sync_api.Page, arglist: list):
    # sh
    # page.goto("https://openmind.test.osinfra.cn/")
    # test
    # page.goto("https://modelfoundry.test.osinfra.cn/")
    # 生产
    page.goto("https://modelers.cn/")
    # page.locator('#e2e_header_loginBtn').click()
    # page.wait_for_selector('#e2e_login_account')
    # page.locator('#e2e_login_account').fill(arglist[0])
    try:
        page.get_by_role("button", name="登录", exact=True).click()
    finally:
        pass
    page.get_by_placeholder('请输入您的手机号/用户名/邮箱地址').fill(arglist[0])
    # page.locator('#e2e_login_password').fill(arglist[1])
    page.get_by_placeholder('请输入您的密码').fill(arglist[1])
    page.click('#e2e_login_submit')
    page.wait_for_timeout(1000)
    expect(page.locator('#e2e_header_isLogined')).to_be_attached()
    # if not page.locator('#e2e_header_isLogined'):
    #     login_sh(page, arglist)
    return page


# 登录生产环境
def login(page: sync_api.Page):
    page.goto("https://telecom.openmind.cn/")
    # page.locator('#e2e_header_loginBtn').click()
    page.wait_for_selector('#e2e_login_account')
    page.locator('#e2e_login_account').fill('18801113053')
    page.locator('#e2e_login_password').fill('liuyu!198')
    page.click('#e2e_login_submit')
    page.wait_for_timeout(1000)
    # if not page.locator('#e2e_header_isLogined'):
    #     login_sh(page)


# 进入首页
def go_home(page: sync_api.Page):
    page.locator('#e2e_headerNav_home').click()


# 退出登录
def logout(page: sync_api.Page):
    # name = inspect.currentframe().f_code.co_name
    hover_user_img(page)
    page.get_by_text('退出登录').click()
    page.wait_for_timeout(1500)
    return page


# 个人中心
# 鼠标悬停在个人头像上
def hover_user_img(page: sync_api.Page):
    # screenshot_count = 1
    # name = inspect.currentframe().f_code.co_name
    page.hover('#e2e_header_isLogined')
    page.wait_for_timeout(200)
    # shot(page, name, screenshot_count)
    return page


# 进入个人中心
def enter_user_center(page: sync_api.Page):
    # name = inspect.currentframe().f_code.co_name
    # 进入个人中心
    page.locator('#e2e_headerUser_center').hover()
    page.locator('#e2e_headerUser_center').click()
    page.wait_for_timeout(500)
    return page


# 创建令牌
def create_token(page: sync_api.Page, arglist: list):
    page.locator("#e2e_myAside_token").click()
    page.get_by_role("button", name="创建令牌").click()
    page.locator("#e2e_newMyToken_tokenInput label").click()
    page.get_by_placeholder("请输入令牌名称").fill(arglist[0])
    if arglist[1] == 'Read':
        pass
    elif arglist[1] == 'Write':
        page.locator("div").filter(has_text=re.compile(r"^\*权限readwrite$")).get_by_role("textbox").click()
        page.locator("div").filter(has_text=re.compile(r"^write$")).click()
    page.get_by_role("button", name="下一步").click()
    page.get_by_text("我了解令牌不再显示在平台上，已复制保存好该令牌").click()
    page.get_by_role("button", name="确定").click()
    return page


# 删除最新创建的令牌
def delete_first_token(page: sync_api.Page):
    page.locator("a").filter(has_text="删除").first.click()
    page.locator("#e2e_deleteToken_dialog").get_by_role("img").click()
    page.locator("a").filter(has_text="删除").first.click()
    page.get_by_role("button", name="确定").click()
    return page


# 注销/取消注销账号
def log_out_user(page: sync_api.Page):
    enter_user_setting(page)
    # page.locator("div").filter(has_text=re.compile(r"^注销魔乐社区账号$")).hover()
    # page.locator('.o-link-label').get_by_text('注销账号').click()
    # page.get_by_role("button", name="继续注销").click()
    # page.locator("div").filter(has_text=re.compile(r"^注销魔乐社区账号$")).hover()
    # page.locator('.o-link-label').get_by_text('取消注销').click()
    page.get_by_text("注销魔乐社区账号注销账号").click()
    page.locator("a").filter(has_text="注销账号").click()
    page.get_by_role("button", name="继续注销").click()
    page.get_by_text("注销魔乐社区账号取消注销").click()
    page.locator("a").filter(has_text="取消注销").click()
    return page


# 收藏并取消收藏
def like_and_not_like(page: sync_api.Page):
    page.get_by_role("link", name="模型库").click()
    page.get_by_title("TeleAI / TeleChat-7B-pt").click()
    page.get_by_role("button", name="收藏").click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="收藏").click()


# 进入账户设置页面
def enter_user_setting(page: sync_api.Page):
    page.locator("#e2e_myAside_settings").click()


# 查看我创建的模型
def show_my_models(page: sync_api.Page):
    # name = inspect.currentframe().f_code.co_name
    page.locator('#e2e_myAside_creation').click()
    page.get_by_text('我的模型').click()
    page.wait_for_timeout(500)


查看我创建的组织
def show_my_orgs(page: sync_api.Page):
    # name = inspect.currentframe().f_code.co_name
    page.locator('#e2e_myAside_organization').click()
    page.wait_for_timeout(500)


# 查看我创建的数据集
def show_my_datasets(page: sync_api.Page):
    # name = inspect.currentframe().f_code.co_name
    page.locator('#e2e_myAside_creation').click()
    page.get_by_text('数据集').click()
    page.wait_for_timeout(500)


# 修改用户昵称签名
def update_user_name_fullname(page: sync_api.Page, arglist: list):
    enter_user_setting(page)
    page.locator("#e2e_mySettings_fullname label").fill(arglist[0])
    page.locator("#e2e_mySettings_desc label").fill(arglist[1])
    page.get_by_role("button", name="保存修改").click()
    page.wait_for_timeout(1000)
    return page


# 修改用户头像
def update_user_picture(page: sync_api.Page, arglist: list):
    enter_user_setting(page)
    page.locator(".o-form-item-main-wrap > .avatar").click()
    page.wait_for_timeout(1000)
    page.locator('.o-upload-input').all()[0].set_input_files(arglist[0])
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="保存头像").click()
    page.wait_for_timeout(3000)


# 组织
# 悬停方式创建组织
def hover_create_organization(page: sync_api.Page, arglist: list):
    page.locator('#e2e_headerUser_newOrg').hover()
    page.locator('#e2e_headerUser_newOrg').click()
    page.locator('#e2e_newOrg_nameInput').fill(arglist[0])
    page.locator('#e2e_newOrg_fullnameInput').fill(arglist[1])
    page.wait_for_timeout(1000)
    # page.locator('.o-upload-input').all()[0].set_input_files(arglist[2])
    page.locator('.o-textarea-textarea').fill(arglist[3])
    page.get_by_placeholder("关联组织官网或GitHub地址").fill(arglist[4])
    page.wait_for_timeout(5000)
    page.locator('#e2e_newOrg_submitBtn').click()
    page.wait_for_timeout(1000)


# 组织创建模型
def org_create_model(page: sync_api.Page, arglist: list):
    page.locator('.o-dropdown').get_by_text(' 创建').click()
    page.locator('.o-dropdown-item').get_by_text('创建模型').click()
    create_model(page, arglist)


# 组织创建数据集
def org_create_dataset(page: sync_api.Page, arglist: list):
    page.locator('.o-dropdown').get_by_text(' 创建').click()
    page.locator('.o-dropdown-item').get_by_text('创建数据集').click()
    create_dataset(page, arglist)


# 组织邀请成员
def org_invite_members(page: sync_api.Page, arglist: list):
    page.locator('#e2e_orgDetail_modifyBtn').click()
    page.locator("#e2e_orgDetailMenu_members-manage").click()
    page.get_by_role("button", name="邀请成员").click()
    page.get_by_placeholder("请输入用户名，添加新成员").click()
    page.get_by_placeholder("请输入用户名，添加新成员").fill(arglist[0])
    page.get_by_role("button", name="发送邀请").click()
    page.wait_for_timeout(500)


# 允许主动申请加入组织
def allow_want_in_org(page: sync_api.Page):
    page.locator('#e2e_orgDetail_modifyBtn').click()
    page.locator('#e2e_orgDetailMenu_account').click()
    page.get_by_text("是").click()
    page.get_by_role("button", name="保存修改").click()


# 同意主动加入组织
def allow_in_org(page: sync_api.Page):
    page.locator('#e2e_orgDetail_modifyBtn').click()
    page.wait_for_timeout(1000)
    page.locator('#e2e_orgDetailMenu_members-manage').click()
    page.locator('.o-link-label').get_by_text('查看').click()
    page.locator('.o-btn.o-btn-primary.o-btn-large.o-btn-solid').get_by_text('接受').click()


# 同意邀请加入组织
def agree_org_invite(page: sync_api.Page):
    hover_user_img(page)
    enter_user_center(page)
    page.get_by_text("我的组织").click()
    page.locator("a").filter(has_text="接受").click()


# 申请加入组织
def user_want_in_org(page: sync_api.Page, arglist: list):
    page.locator('#e2e_headerNav_more').hover()
    page.get_by_text("组织").click()
    page.get_by_placeholder("输入关键字，搜索你想查询的组织").fill(arglist[0])
    page.locator('.fullname').get_by_text(arglist[0]).click()
    page.get_by_role("button", name="申请加入").click()
    page.get_by_placeholder("请输入申请理由，不超过20个字符").fill(arglist[1])
    page.get_by_role("button", name="提交").click()


# 拒绝加入组织
def refuse_org_invite(page: sync_api.Page):
    hover_user_img(page)
    enter_user_center(page)
    page.get_by_text("我的组织").click()
    page.locator("a").filter(has_text="拒绝").click()


# 查看指定组织
def show_point_org(page: sync_api.Page, arglist: list):
    page.locator('.org-fullname').get_by_text(arglist[0]).click()
    page.wait_for_timeout(500)


# 删除当前组织
def delete_current_org(page: sync_api.Page):
    # name = inspect.currentframe().f_code.co_name
    # page.locator('#e2e_orgDetail_modifyBtn').click()
    page.locator('#e2e_orgDetailMenu_account').click()
    page.locator('#e2e_deleteOrg_inputValidation').fill('我已知晓，并确认删除组织')
    page.locator('#e2e_deleteOrg_deleteBtn').click()
    page.locator('.o-btn.o-btn-normal.o-btn-large.o-btn-outline.o-dlg-btn').click()


# 修改组织昵称介绍链接
def update_org(page: sync_api.Page, arglist: list):
    page.locator('#e2e_orgDetail_modifyBtn').click()
    page.locator('#e2e_orgDetailMenu_profile').click()
    page.get_by_placeholder('请填写组织昵称').fill(arglist[0])
    page.get_by_placeholder('请输入组织介绍内容').fill(arglist[1])
    page.get_by_placeholder('关联组织官网或GitHub地址').fill(arglist[2])
    page.locator('#e2e_orgDetail_submitDetailBtn').click()
    page.wait_for_timeout(500)


# 修改组织封面
def update_org_picture(page: sync_api.Page, arglist: list):
    page.locator('#e2e_orgDetail_modifyBtn').click()
    page.locator('#e2e_orgDetailMenu_profile').click()
    # page.locator("form").get_by_role("img").click()
    page.get_by_role("button", name="选择照片").set_input_files(arglist[0])
    page.get_by_role("button", name="保存头像").click()
    page.wait_for_timeout(4000)


# 数据集
# 悬停方式创建数据集
def hover_create_dataset(page: sync_api.Page, arglist: list):
    page.locator('#e2e_headerUser_newDataset').hover()
    page.locator('#e2e_headerUser_newDataset').click()
    create_dataset(page, arglist)
    # page.locator('#e2e_newDatasets_nameInput').fill(arglist[0])
    # page.get_by_placeholder('请输入数据集别名').fill(arglist[1])
    # # arglist 2 一定是 私有数据集/公有数据集之一
    # page.locator('.o-radio-label').get_by_text(arglist[2]).click()
    # page.get_by_placeholder('请选择许可证').click()
    # page.locator('.o-option').get_by_text(arglist[3]).click()
    # page.locator('#e2e_newDatasets_submitBtn').click()
    # page.wait_for_timeout(1500)


# 创建数据集
def create_dataset(page: sync_api.Page, arglist: list):
    page.locator('#e2e_newDatasets_nameInput').fill(arglist[0])
    page.get_by_placeholder('请输入数据集别名').fill(arglist[1])
    # arglist 2 一定是 私有数据集/公有数据集之一
    page.locator('.o-radio-label').get_by_text(arglist[2]).click()
    page.get_by_placeholder('请选择许可证').click()
    page.locator('.o-option').get_by_text(arglist[3]).click()
    page.locator('#e2e_newDatasets_submitBtn').click()
    page.wait_for_timeout(1500)


# 查看指定数据集
def show_point_dataset(page: sync_api.Page, arglist: list):
    page.locator('.title').get_by_text(arglist[0]).click()
    page.wait_for_timeout(500)


# 删除当前数据集
def delete_current_dataset(page: sync_api.Page):
    # name = inspect.currentframe().f_code.co_name
    page.locator('.o-tab-nav').get_by_text('设置').click()
    page.locator('#e2e_deleteDataset_inputValidation').fill('我已知晓，并确认删除数据集')
    page.locator('#e2e_deleteDataset_deleteBtn').click()


# 修改当前数据集私有
def change_current_dataset_private(page: sync_api.Page):
    page.locator('.o-tab-nav').get_by_text('设置').click()
    page.locator('.o-radio-label').get_by_text('私有数据集').click()
    page.locator('#e2e_modifyDataset_submit').click()


# 查看数据集
def go_datasets(page: sync_api.Page):
    page.locator('#e2e_headerNav_datasets').click()


# 模型
# 悬停方式创建模型
def hover_create_model(page: sync_api.Page, arglist: list):
    # name = inspect.currentframe().f_code.co_name
    page.locator('#e2e_headerUser_newModel').hover()
    page.locator('#e2e_headerUser_newModel').click()
    # 填入参数
    create_model(page, arglist)
    # page.locator('#e2e_newModels_nameInput').fill(arglist[0])
    # page.get_by_placeholder("请填写模型别名").fill(arglist[1])
    # if arglist[2] == '私有模型':
    #     page.get_by_text('私有模型').click()
    # elif arglist[2] == '公开模型':
    #     page.get_by_text('公开模型').click()
    # page.locator('#e2e_newModels_licenseSelect').click()
    # page.get_by_text(arglist[3], exact=True).click()
    # page.locator('#e2e_newModels_submitBtn').click()
    # page.wait_for_timeout(500)
    # # input()


# 创建模型
def create_model(page: sync_api.Page, arglist: list):
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


# 查看指定模型
def show_point_model(page: sync_api.Page, arglist: list):
    page.locator('.title').get_by_text(arglist[0]).click()
    page.wait_for_timeout(500)


# 删除当前模型
def delete_current_model(page: sync_api.Page):
    # name = inspect.currentframe().f_code.co_name
    page.locator('.o-tab-nav').get_by_text('设置').click()
    page.locator('#e2e_deleteModel_inputValidation').fill('我已知晓，并确认删除模型')
    page.locator('#e2e_deleteModel_deleteBtn').click()


# 修改当前模型私有
def change_current_model_private(page: sync_api.Page):
    page.get_by_role("link", name="设置").click()
    # 空间封面
    # page.locator('.o-upload-input').all()[0].set_input_files(arglist[0])
    page.wait_for_timeout(2000)
    page.get_by_text("私有模型").click()
    page.get_by_role("button", name="保存修改").click()


# 修改当前模型别名
def change_current_model_name(page: sync_api.Page, arglist: list):
    page.locator('.o-tab-nav').get_by_text('设置').click()
    page.get_by_placeholder('请填写模型别名').fill(arglist[0])
    page.get_by_role("button", name="保存修改").click()


# 查看模型库
def go_models(page: sync_api.Page):
    page.locator('#e2e_headerNav_models').click()


# 空间
# 悬停方式创建空间
def hover_create_space(page: sync_api.Page, arglist: list):
    page.get_by_text("创建空间").click()
    # 空间名称
    page.get_by_placeholder("请输入空间名").fill(arglist[0])
    # 空间别名
    page.get_by_placeholder("请输入空间别名").fill(arglist[1])
    # 空间封面
    # page.locator("div").filter(has_text=re.compile(r"^点击上传$")).nth(4).click()
    # page.get_by_role("button", name="确认").click()
    # page.get_by_role("button", name="确认").set_input_files(arglist[2])
    page.locator('.o-upload-input').all()[0].set_input_files(arglist[2])
    page.wait_for_timeout(2000)
    # 许可证
    page.locator("#e2e_newSpaces_licenseSelect").click()
    page.get_by_text(arglist[3]).click()
    # 接入SDK
    page.get_by_text(arglist[4]).click()
    # 算力资源
    page.get_by_placeholder("请选择算力资源").click()
    if arglist[5] == 'CPU':
        page.get_by_text("CPU basic 2 vCPU · 16GB · 免费").click()
    elif arglist[5] == 'NPU':
        page.get_by_text("NPU basic 16 vCPU · 128GB").click()
    # 基础环境
    page.get_by_placeholder("请选择基础环境").click()
    if arglist[6] == 'pytorch':
        page.get_by_text("PyTorch (python3.8-pytorch2.1)").click()
    elif arglist[6] == 'mindspore':
        page.get_by_text("MindSpore (python3.8-").click()
    # 是否公开
    page.get_by_text(arglist[7]).click()
    # 创建
    page.get_by_role("button", name="创建").click()
    page.wait_for_timeout(2000)


# 删除当前空间
def delete_current_space(page: sync_api.Page):
    page.get_by_role("link", name="设置").click()
    page.get_by_placeholder("请输入", exact=True).fill("我已知晓，并确认删除空间")
    page.locator("#e2e_deleteSpace_deleteBtn").click()


# 修改当前空间
def change_current_space(page: sync_api.Page, arglist: list):
    page.get_by_role("link", name="设置").click()
    page.wait_for_timeout(500)
    # 空间封面
    page.locator("form").get_by_role("img").nth(2).click()
    page.locator('.o-upload-input').all()[0].set_input_files(arglist[0])
    page.wait_for_timeout(2000)
    # 空间别名
    page.get_by_placeholder("请输入空间别名").fill(arglist[1])
    # 是否公开
    page.get_by_text(arglist[2]).click()
    # 修改
    page.get_by_role("button", name="确认修改").click()
    page.wait_for_timeout(2000)


# 创建变量
def create_variable(page: sync_api.Page, arglist: list):
    page.get_by_role("link", name="设置").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^环境变量创建$")).get_by_role("button").click()
    page.get_by_placeholder("请输入变量名称").fill(arglist[0])
    page.get_by_placeholder("请输入变量值").fill(arglist[1])
    page.get_by_role("button", name="确认", exact=True).click()


# 编辑变量
def change_variable(page: sync_api.Page, arglist: list):
    page.locator("a").filter(has_text=re.compile(r"^编辑$")).click()
    page.get_by_placeholder("请输入变量值").click()
    page.get_by_placeholder("请输入变量值").fill(arglist[0])
    page.get_by_role("button", name="确认", exact=True).click()


# 删除变量
def delete_variable(page: sync_api.Page):
    page.locator("a").filter(has_text=re.compile(r"^删除$")).click()


# 创建机密变量
def create_secret(page: sync_api.Page, arglist: list):
    page.get_by_role("link", name="设置").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^机密变量创建$")).get_by_role("button").click()
    if arglist[0] == '是':
        page.get_by_text("是", exact=True).click()
    elif arglist[0] == '否':
        page.get_by_text("否", exact=True).click()
    page.get_by_placeholder("请输入变量名称").fill(arglist[1])
    page.get_by_placeholder("请输入变量值").fill(arglist[2])
    page.get_by_role("button", name="确认", exact=True).click()


# 编辑机密变量
def change_secret(page: sync_api.Page, arglist: list):
    page.locator("a").filter(has_text=re.compile(r"^编辑$")).click()
    page.get_by_placeholder("请输入变量值").click()
    page.get_by_placeholder("请输入变量值").fill(arglist[0])
    page.get_by_role("button", name="确认", exact=True).click()


删除机密变量
def delete_secret(page: sync_api.Page):
    page.locator("a").filter(has_text=re.compile(r"^删除$")).click()


# 查看体验空间
def go_spaces(page: sync_api.Page):
    page.locator('#e2e_headerNav_spaces').click()


# 讨论区
# 创建评论
def create_issue(page: sync_api.Page, arglist: list):
    page.locator('.o-tab-nav').get_by_text('讨论区').click()
    page.get_by_text('创建Issue').click()
    page.get_by_placeholder('请输入标题').fill(arglist[0])
    page.get_by_placeholder('请输入内容').fill(arglist[1])
    page.locator('.o-btn.o-btn-primary.o-btn-large.o-btn-solid').get_by_text('创建').click()


# 回复评论
def review_issue(page: sync_api.Page, arglist: list):
    page.locator('.o-tab-nav').get_by_text('讨论区').click()
    page.get_by_title(arglist[0]).click()
    page.get_by_placeholder('请输入评论').fill(arglist[1])
    page.locator('.o-btn.o-btn-primary.o-btn-large.o-btn-solid').get_by_text('发表评论').click()


# 编辑第一条讨论
def edit_issue(page: sync_api.Page, arglist: list):
    page.locator(".o-dropdown > .o-icon > svg").click()
    page.get_by_text("编辑", exact=True).click()
    page.get_by_placeholder("请输入评论").first.fill(arglist[0])
    page.get_by_role("button", name="更新").click()


# 删除第二条讨论
def delete2nd_issue(page: sync_api.Page):
    page.locator(
        "div:nth-child(2) > .issue-discussion-item > .issue-discussion-header > .o-dropdown > .o-icon > svg").click()
    page.get_by_text("删除", exact=True).click()
    page.get_by_role("button", name="确认").click()


# 举报第二条讨论
def report2nd_issue(page: sync_api.Page, arglist: list):
    page.locator(
        "div:nth-child(2) > .issue-discussion-item > .issue-discussion-header > .o-dropdown > .o-icon > svg").click()
    page.locator("li").filter(has_text="举报").click()
    page.get_by_role("button", name="提交").click()
    page.get_by_text("违法违规").click()
    page.get_by_text("涉政谣言").click()
    page.get_by_text("涉社会事件谣言").click()
    page.get_by_text("色情").click()
    page.get_by_text("引战").click()
    page.get_by_text("人身攻击").click()
    page.get_by_text("虚假不实信息").click()
    page.get_by_text("其他").click()
    page.get_by_text("违法信息").click()
    page.get_by_placeholder("请输入举报内容").click()
    page.get_by_placeholder("请输入举报内容").fill(arglist[0])
    page.get_by_role("button", name="提交").click()
    page.wait_for_timeout(3000)


# 关闭讨论
def close_issue(page: sync_api.Page, arglist: list):
    page.locator('.o-tab-nav').get_by_text('讨论区').click()
    page.get_by_title(arglist[0]).click()
    page.get_by_role('button').get_by_text('关闭讨论').click()


# 重启讨论
def reuse_issue(page: sync_api.Page, arglist: list):
    page.locator('.o-tab-nav').get_by_text('讨论区').click()
    page.get_by_title(arglist[0]).click()
    page.get_by_role('button').get_by_text('重启讨论').click()


# 切换讨论区状态
def change_all_issue(page: sync_api.Page):
    page.locator('.o-tab-nav').get_by_text('设置').click()
    page.locator("div").filter(
        has_text=re.compile(r"^讨论区您可以主动开启或关闭讨论区，关闭后将无法访问讨论区内容$")).locator("div").nth(
        2).click()
    page.wait_for_timeout(3000)


# 查看讨论
def view_issue(page: sync_api.Page, arglist: list):
    page.locator('.o-tab-nav').get_by_text('讨论区').click()
    page.get_by_title(arglist[0]).click()


# 资源处理
# 下载文件
def download_point_file(page: sync_api.Page, arglist: list):
    page.locator('.o-tab-nav').get_by_text('文件').click()
    page.get_by_text(arglist[0]).click()
    page.wait_for_timeout(500)
    with page.expect_download() as download_info:
        page.get_by_text("下载文件").click()
    download = download_info.value
    download.save_as("download/" + download.suggested_filename)


# 编辑模型标签
def edit_model_tags(page: sync_api.Page, arglist: list):
    # name = inspect.currentframe().f_code.co_name
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


# 新建文件
def create_file(page: sync_api.Page, arglist: list):
    # print(arglist)
    # name = inspect.currentframe().f_code.co_name
    page.locator('.o-tab-nav').get_by_text('文件').click()
    page.get_by_text('新建文件').click()
    page.get_by_placeholder('请输入文件名').fill(arglist[0])
    page.locator('.view-line').click()
    with open(arglist[1], 'r', encoding='utf-8') as file:
        arglist[1] = file.read()
    page.get_by_label("Editor content;Press Alt+F1").fill(arglist[1])
    # pyautogui.write(arglist[1])  # ???什么类型啊这个元素vocal，整不会了
    # page.locator('.mtk7').fill(arglist[1],force=True)
    page.locator('.o-btn.o-btn-primary.o-btn-large.o-btn-solid.upload').get_by_text('提交').click()
    page.locator('.o-textarea-textarea').fill(arglist[2])
    page.locator('.o-btn.o-btn-primary.o-btn-large.o-btn-solid.o-dlg-btn').get_by_text('提交').click()
    page.wait_for_timeout(2000)
    expect(page.get_by_text('文件太大或不支持展示，')).not_to_be_attached()


# 删除文件
def delete_file(page: sync_api.Page, arglist: list):
    # name = inspect.currentframe().f_code.co_name
    page.locator('.o-tab-nav').get_by_text('文件').click()
    page.get_by_title(arglist[0]).click()
    # page.locator('.hover-stress').get_by_title(arglist[0]).click()
    page.locator('.hover-stress').get_by_text('删除').click()
    page.wait_for_timeout(500)
    page.locator('.o-btn.o-btn-primary.o-btn-large.o-btn-solid.o-dlg-btn').get_by_text('删除').click()
    page.wait_for_timeout(500)


# 反馈
# 体验反馈
def feedback(page: sync_api.Page):
    page.locator("#feedback").get_by_role("img").first.hover()
    page.get_by_text("10", exact=True).click()
    page.get_by_placeholder("请输入您推荐的原因").fill("体验非常好哇")
    page.get_by_role("button", name="确定").click()
    return page

# 文档
# 查看文档
def go_docs(page: sync_api.Page):
    page.locator('#e2e_headerNav_docs').click()


def_dict = {
            # 进入环境
            '首次登录环境': login_first,
            '登录环境': login_common,
            '登录生产环境': login,
            '进入首页': go_home,
            '退出登录': logout,

            # 个人中心
            '鼠标悬停在个人头像上': hover_user_img,
            '进入个人中心': enter_user_center,
            '创建令牌': create_token,
            '删除最新创建的令牌': delete_first_token,
            '注销并取消注销': log_out_user,
            '收藏并取消收藏': like_and_not_like,
            '进入账户设置': enter_user_setting,
            '查看我创建的模型': show_my_models,
            '查看我创建的组织': show_my_orgs,
            '查看我创建的数据集': show_my_datasets,
            '修改用户昵称签名': update_user_name_fullname,
            '修改用户头像': update_user_picture,
    
            # 组织
            '悬停方式创建组织': hover_create_organization,
            '组织创建模型': org_create_model,
            '组织创建数据集': org_create_dataset,
            '组织邀请成员': org_invite_members,
            '允许主动申请加入组织': allow_want_in_org,
            '同意主动加入组织': allow_in_org,
            '同意邀请加入组织': agree_org_invite,
            '申请加入组织': user_want_in_org,
            '拒绝加入组织': refuse_org_invite,
            '查看指定组织': show_point_org,
            '删除当前组织': delete_current_org,
            '修改组织昵称介绍链接': update_org,
            '修改组织封面': update_org_picture,
    
            # 数据集
            '悬停方式创建数据集': hover_create_dataset,
            '创建数据集': create_dataset,
            '查看指定数据集': show_point_dataset,
            '删除当前数据集': delete_current_dataset,
            '修改当前数据集私有': change_current_dataset_private,
            '查看数据集': go_datasets,
    
            # 模型
            '悬停方式创建模型': hover_create_model,
            '创建模型': create_model,
            '查看指定模型': show_point_model,
            '删除当前模型': delete_current_model,
            '修改当前模型私有': change_current_model_private,
            '修改当前模型别名': change_current_model_name,
            '查看模型库': go_models,
    
            # 空间
            '悬停方式创建空间': hover_create_space,
            '删除当前空间': delete_current_space,
            '修改当前空间': change_current_space,
            '创建变量': create_variable,
            '编辑变量': change_variable,
            '删除变量': delete_variable,
            '创建机密变量': create_secret,
            '编辑机密变量': change_secret,
            '删除机密变量': delete_secret,
            '查看体验空间': go_spaces,

            # 讨论区
            '创建讨论': create_issue,
            '回复讨论': review_issue,
            '编辑第一条讨论': edit_issue,
            '删除第二条讨论': delete2nd_issue,
            '举报第二条讨论': report2nd_issue,
            '关闭讨论': close_issue,
            '重启讨论': reuse_issue,
            '切换讨论区状态': change_all_issue,
            '查看讨论': view_issue,
    
            # 资源处理
            '下载文件': download_point_file,
            '编辑模型标签': edit_model_tags,
            '新建文件': create_file,
            '删除文件': delete_file,

            # 反馈
            '体验反馈': feedback,

            # 文档
            '查看文档': go_docs,
            }
tag_dict = {'pipeline_tag': '新增标签',
            'frameworks': '新增框架',
            'license': '新增许可证',
            ' library_name ': '新增库',
            'hardwares': '新增硬件',
            'language': '新增语言'}

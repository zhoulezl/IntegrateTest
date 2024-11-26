import re
from playwright import sync_api
from playwright.sync_api import expect


# 账号服务
def open_url(page: sync_api.Page):
    """进入生产环"""
    page.goto('https://www.openeuler.org/zh/')
    return page


def open_url_test(page: sync_api.Page):
    """进入测试环境"""
    page.goto('https://openeuler-website.test.osinfra.cn/zh/')
    return page


def longin(page: sync_api.Page, arglist: list):
    """ 登录 """
    page.locator(".login > .o-icon > svg").click()  # 点击右上角头像图标
    page.wait_for_timeout(2000)
    page.get_by_placeholder("请输入您的手机号/用户名/邮箱地址").fill(arglist[0])  # 输入账号
    page.get_by_placeholder("请输入您的密码").fill(arglist[1])  # 输入密码
    page.get_by_role("button", name="登录").click()  # 点击登录按钮
    page.wait_for_timeout(1000)
    element = page.locator("label span").first
    # page.wait_for_timeout(1000)
    try:
        expect(element).to_be_visible()
        page.wait_for_timeout(1000)
        page.locator("label span").first.click()
        page.get_by_role("button", name="确认").click()
        page.wait_for_timeout(1000)
        page.hover('.user-img')  # 鼠标悬浮在头像上
        expect(page.get_by_text("退出登录")).to_be_visible()  # 有退出登录，则断言成功
    except Exception:
        page.hover('.user-img')  # 鼠标悬浮在头像上
        expect(page.get_by_text("退出登录")).to_be_visible()  # 有退出登录，则断言成功

    return page  # 返回登录后的页面


def longin_and_sign_privacy_statement(page: sync_api.Page, arglist: list):
    """ 登录并签署隐私声明 """
    page.wait_for_timeout(1000)
    page.locator(".login > .o-icon > svg").click()  # 点击右上角头像图标
    page.wait_for_timeout(1000)
    page.get_by_placeholder("请输入您的手机号/用户名/邮箱地址").fill(arglist[0])  # 输入账号
    page.get_by_placeholder("请输入您的密码").fill(arglist[1])  # 输入密码
    page.get_by_role("button", name="登录").click()  # 点击登录按钮
    page.wait_for_timeout(1000)
    page.locator("label span").first.click()  # 勾选隐私声明
    page.get_by_role("button", name="确认").click()  # 点击确认按钮
    page.wait_for_timeout(1000)
    page.hover('.img[class*="img"]')  # 鼠标悬浮在头像上
    page.wait_for_timeout(1000)
    expect(page.get_by_text("退出登录")).to_be_visible()  # 有退出登录，则断言成功
    page.close()
    all_page = page.context.pages
    return all_page[0]


def logout(page: sync_api.Page):
    """ 退出登录 """
    page.locator('img[class*="img"]').first.hover()  # 鼠标悬浮在头像上
    page.get_by_text("退出登录").click()  # 点击退出登录按钮
    page.wait_for_timeout(1000)
    expect(page.locator(".login > .o-icon > svg")).to_be_visible()  # 断言
    page.wait_for_timeout(500)
    return page


#
# 个人中心
def enter_user_center(page: sync_api.Page):
    """ 进入个人中心 """
    page.hover('.user-img')
    with page.expect_popup() as page1_info:
        page.get_by_text("个人中心").click()
    page1 = page1_info.value
    return page1


def change_user_avatar(page: sync_api.Page, arglist: list):
    """ 个人中心更换头像 """
    old_img_src = page.locator("//img[@class='img']").get_attribute("src")  # 获取旧头像地址
    # print(old_img_src)
    page.wait_for_timeout(1000)
    page.locator("//input[@type='file']").set_input_files(f"{arglist[0]}")
    page.wait_for_timeout(1000)
    new_img_src = page.locator("//img[@class='img']").get_attribute("src")  # 获取新头像地址
    # print(new_img_src)
    assert old_img_src != new_img_src, "更换头像失败"
    page.wait_for_timeout(2000)
    return page


def change_nickname(page: sync_api.Page, arglist: list):
    """修改昵称"""
    page.get_by_placeholder("请输入你的昵称").fill("")
    page.get_by_placeholder("请输入你的昵称").fill(arglist[0])
    page.get_by_role("button", name="保存").click()
    expect(page.get_by_placeholder("请输入你的昵称")).to_have_value(arglist[0])
    return page


def change_company(page: sync_api.Page, arglist: list):
    """修改公司"""
    page.get_by_placeholder("请输入你的公司").fill("")
    page.get_by_placeholder("请输入你的公司").fill(arglist[0])
    page.get_by_role("button", name="保存").click()
    expect(page.get_by_placeholder("请输入你的公司")).to_have_value(arglist[0])
    page.wait_for_timeout(1000)
    page.close()
    all_page = page.context.pages
    return all_page[0]


def cancel_signature(page: sync_api.Page):
    """取消签署协议"""
    page.get_by_text("账号安全").click()
    page.get_by_role("button", name="取消签署").click()
    page.locator(".el-input__inner").fill("delete")
    page.get_by_role("button", name="确认").click()
    expect(page.get_by_text("请先 登录 !")).to_be_visible()
    return page


# 消息中心
def enter_messag2_center(page: sync_api.Page):
    """ 进入消息中心 """
    page.hover('.user-img')
    with page.expect_popup() as page_info:
        page.get_by_text("消息中心").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_text("消息中心")).to_be_visible()
    return page1


def message_to_read(page: sync_api.Page):
    """ 标为已读 """
    page.get_by_text("提到我的").click()
    page.locator(
        ".list-item-left > .o-checkbox > .o-checkbox-wrap > .o-checkbox-input-wrap > .o-checkbox-input").first.click()
    page.get_by_text("已读 标记已读").click()
    page.wait_for_timeout(2000)
    return page


def delete_message(page: sync_api.Page):
    """ 删除消息 """
    page.locator(".list-item-left > .o-checkbox > .o-checkbox-wrap > .o-checkbox-input-wrap").first.click()
    page.locator("a").filter(has_text="删除").first.click()
    page.get_by_role("button", name="确定").click()
    page.wait_for_timeout(1000)
    return page


def message_pagesize(page: sync_api.Page, arglist: list):
    """ 调整消息分页 """
    page.get_by_role("textbox").nth(1).click()
    page.get_by_text(arglist[0]).click()
    page.wait_for_timeout(1000)
    return page


def message_page_change(page: sync_api.Page, arglist: list):
    """ 切换消息切页 """
    page.locator("div").filter(has_text=re.compile(r"^前往$")).locator("div").first.click()
    page.locator("div").filter(has_text=re.compile(r"^前往$")).get_by_label("").fill(arglist[0])
    page.locator("div").filter(has_text=re.compile(r"^前往$")).get_by_label("").press("Enter")
    page.wait_for_timeout(1000)
    page.close()
    all_page = page.context.pages
    return all_page[0]


# 导航-下载


def navigation_download(page: sync_api.Page, arglist: list):
    """ 选择导航_下载"""
    page.get_by_role("navigation").get_by_text("下载", exact=True).click()
    page.wait_for_timeout(1000)

    options = {
        '社区发行版': ".nav-sub > .active",
        '其他版本': ".nav-sub > div:nth-child(2)",
        '下载资源': "div:nth-child(3)"
    }

    if arglist[0] in options:
        page.locator(options[arglist[0]]).first.click()

    page.wait_for_timeout(1500)
    return page


def other_download_way(page: sync_api.Page):
    """ 其他获取方式 """
    navigation_download(page, ['社区发行版'])
    page.locator(".extra > div > div").first.click()
    page.wait_for_timeout(1000)
    expect(page.get_by_role("heading", name="获取openEuler操作系统")).to_be_visible()
    page.wait_for_timeout(500)
    return page


def click_public_cloud(page: sync_api.Page):
    """ 点击公有云 """
    navigation_download(page, ['社区发行版'])
    page.locator(".extra > div > .content-container > div > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="公有云上openEuler镜像使用指南 Permalink")).to_be_visible()
    page.wait_for_timeout(500)
    return page


def click_container_image(page: sync_api.Page):
    """ 点击容器镜像 """
    navigation_download(page, ['社区发行版'])
    page.locator(".extra > div > .content-container > div:nth-child(2) > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="openEuler容器镜像部署指南 Permalink")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def click_windows(page: sync_api.Page):
    """ 点击Windows """
    navigation_download(page, ['社区发行版'])
    page.locator(".extra > div > .content-container > div:nth-child(3) > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="如何在 openEuler WSL 中体验完整的桌面环境")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def click_virtualization(page: sync_api.Page):
    """ 点击虚拟化 """
    navigation_download(page, ['社区发行版'])
    page.locator("div:nth-child(4) > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="windows 下使用 VirtualBox 安装")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def click_raspberry_pi(page: sync_api.Page):
    """ 点击树莓派 """
    navigation_download(page, ['社区发行版'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="下载社区发行版其他版本下载资源社区发行版openEuler").get_by_role(
            "link").first.click()
    page1 = page_info.value
    page1.wait_for_timeout(3000)
    expect(page1.get_by_text("openEuler/raspberrypi", exact=True)).to_be_visible()
    page1.wait_for_timeout(500)
    page1.close()
    return page


def click_openeuler_24_03_lts(page: sync_api.Page, arglist: list):
    """ 点击openEuler 20.03 LTS """
    if arglist[0] in ['获取方式快捷链接', '社区发行版']:
        navigation_download(page, [arglist[0]])
        page.locator(".shortcut > .link" if arglist[0] == '获取方式快捷链接' else ".link").first.click()
        expect(page.get_by_role("heading", name="下载", exact=True)).to_be_visible()

    return page


def click_image_warehouse_list(page: sync_api.Page, arglist: list):
    """ 点击镜像仓库列表 """
    options = {
        '下载资源': (['下载资源'], "div:nth-child(2) > .item-title > .link")
    }

    if arglist[0] in options:
        navigation_download(page, options[arglist[0]][0])
        page.locator(options[arglist[0]][1]).first.click()
        expect(page.get_by_role("heading", name="镜像仓列表")).to_be_visible()
        page.wait_for_timeout(2000)

    return page


def openeuler_24_03_lts_scene_filter(page: sync_api.Page):
    """ openEuler 24.03 LTS场景筛选 """

    navigation_download(page, ['社区发行版'])

    def click_and_download(index):
        page.locator(f".system-container > div:nth-child({index})").first.click()
        page.wait_for_timeout(2000)
        expect(page.get_by_role("heading", name="下载", exact=True)).to_be_visible()

    for i in range(1, 5):
        if i == 4:
            click_and_download(i)
        else:
            click_and_download(i)
            navigation_download(page, ['社区发行版'])

    page.wait_for_timeout(500)
    return page


def click_openeuler_24_09(page: sync_api.Page):
    """ 点击openEuler 24.09 """
    navigation_download(page, ['社区发行版'])
    page.locator("div:nth-child(2) > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="下载", exact=True)).to_be_visible()
    return page


def openeuler_24_09_scene_filter(page: sync_api.Page):
    """ openEuler 24.09场景筛选 """
    navigation_download(page, ['社区发行版'])
    for i in range(1, 5):  # 遍历1到4，代表不同的div
        if i == 4:
            page.locator(f"div:nth-child(2) > .system-container > div:nth-child({i})").first.click()
            page.wait_for_timeout(2000)
            expect(page.get_by_role("heading", name="下载", exact=True)).to_be_visible()
        else:
            page.locator(f"div:nth-child(2) > .system-container > div:nth-child({i})").first.click()
            page.wait_for_timeout(2000)
            expect(page.get_by_role("heading", name="下载", exact=True)).to_be_visible()
            navigation_download(page, ['社区发行版'])

    page.wait_for_timeout(500)
    return page


def click_openeuler_22_03_lts_sp4(page: sync_api.Page):
    """ 点击openEuler 22.03 LTS SP4 """
    navigation_download(page, ['社区发行版'])
    page.locator("div:nth-child(3) > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="openEuler 22.03 LTS SP4")).to_be_visible()
    return page


def openeuler_22_03_lts_sp4_scene_filter(page: sync_api.Page):
    """ openEuler 22.03 LTS SP4场景筛选 """
    navigation_download(page, ['社区发行版'])

    def click_and_download(index):
        page.locator(f"div:nth-child(3) > .system-container > div:nth-child({index})").first.click()
        page.wait_for_timeout(2000)
        expect(page.get_by_role("heading", name="openEuler 22.03 LTS SP4")).to_be_visible()

    for i in range(1, 5):
        if i == 4:
            click_and_download(i)
        else:
            click_and_download(i)
            navigation_download(page, ['社区发行版'])
    page.wait_for_timeout(500)
    return page


def click_technical_white_paper(page: sync_api.Page):
    """ 点击技术白皮书 """
    navigation_download(page, ['社区发行版'])
    page.locator(".shortcut > .link").first.click()
    page.wait_for_timeout(1000)
    expect(page.get_by_role("heading", name="白皮书")).to_be_visible()
    page.wait_for_timeout(2000)
    return page


def click_24_03_lts_installation_guide(page: sync_api.Page):
    """ 点击24.03 LTS安装指南 """
    navigation_download(page, ['社区发行版'])
    with (page.expect_popup() as page_info):
        page.locator("li").filter(has_text="下载社区发行版其他版本下载资源社区发行版openEuler"
                                  ).get_by_role("link").nth(1).click()
    page1 = page_info.value
    page1.wait_for_timeout(1000)
    expect(page1.get_by_role("heading", name="安装指南")).to_be_visible()
    page1.wait_for_timeout(600)
    page1.close()
    return page


def click_24_09_installation_guide(page: sync_api.Page):
    """ 点击24.09安装指南 """
    navigation_download(page, ['社区发行版'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="下载社区发行版其他版本下载资源社区发行版openEuler").get_by_role("link").nth(
            2).click()
    page1 = page_info.value
    page1.wait_for_timeout(1000)
    expect(page1.get_by_role("heading", name="安装指南")).to_be_visible()
    page1.wait_for_timeout(600)
    page1.close()
    return page


def click_version_lifecycle(page: sync_api.Page):
    """ 点击版本生命周期 """
    navigation_download(page, ['社区发行版'])
    page.locator("div:nth-child(4) > .link").first.click()
    expect(page.get_by_role("heading", name="、openEuler社区版本生命周期管理规范（总体）")).to_be_visible()
    return page


def click_query_history_version(page: sync_api.Page):
    """ 点击查询历史版本 """
    navigation_download(page, ['社区发行版'])
    page.locator("div:nth-child(5) > .link").first.click()
    expect(page.get_by_role("link", name="历史版本下载")).to_be_visible()
    return page


def click_commercial_release(page: sync_api.Page):
    """ 点击商业发行版 """
    navigation_download(page, ['其他版本'])
    page.locator(".link").first.click()
    page.wait_for_timeout(1000)
    expect(page.get_by_role("heading", name="下载", exact=True)).to_be_visible()
    return page


def click_software_center(page: sync_api.Page):
    """ 点击软件中心 """
    navigation_download(page, ['下载资源'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="下载社区发行版其他版本下载资源下载资源软件中心"
                                  ).get_by_role("link").first.click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("heading", name="openEuler软件中心")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_repo_source(page: sync_api.Page):
    """ 点击Repo源 """
    navigation_download(page, ['下载资源'])
    with (page.expect_popup() as page_info):
        page.locator("li").filter(has_text="下载社区发行版其他版本下载资源下载资源软件中心"
                                  ).get_by_role("link").nth(1).click()
    page1 = page_info.value
    page1.wait_for_timeout(1000)
    expect(page1.get_by_role("heading", name="openEuler Repo")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


# 导航-学习
def navigation_study(page: sync_api.Page, arglist: list):
    """ 选择导航_学习 """

    navigation_options = {
        '文档中心': ".active > .nav-dropdown > .nav-drop-content > .nav-sub > .active",
        '课程中心': ".active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(2)",
        '迁移与运维': ".active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(3)",
        '技术展示': ".active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(4)"
    }

    if arglist[0] in navigation_options:
        page.get_by_text("学习", exact=True).click()
        page.wait_for_timeout(1000)
        page.locator(navigation_options[arglist[0]]).click()
        page.wait_for_timeout(3000)

    return page


def click_document_center(page: sync_api.Page):
    """ 点击文档中心 """
    navigation_study(page, ['文档中心'])
    with page.expect_popup() as page_info:
        page.locator(".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > .content-left > a").click()
    page1 = page_info.value
    expect(page1.locator("#left img")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_hot_documents(page: sync_api.Page):
    """ 点击热门文档 """
    navigation_study(page, ['文档中心'])
    with page.expect_popup() as page_info:
        page.locator(
            ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
            " .content-left > .content-container > div > .item-title > .link").first.click()
    page1 = page_info.value
    expect(page1.locator("#left img")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def click_development_tutorials(page: sync_api.Page):
    """ 点击开发教程 """
    navigation_study(page, ['文档中心'])
    with page.expect_popup() as page_info:
        page.locator(
            ".active > .nav-dropdown > .nav-drop-content > ."
            "nav-sub-content > .content-left > .content-container > "
            "div:nth-child(2) > .item-title > .link").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("img", name="logo")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def click_process_standards(page: sync_api.Page):
    """ 点击流程标准 """
    navigation_study(page, ['文档中心'])
    with page.expect_popup() as page_info:
        page.locator(
            ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content "
            "> .content-left > .content-container > div:nth-child(3) > .item-title > .link").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.locator("#left img")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def click_tool_query(page: sync_api.Page):
    """ 点击工具查询 """
    navigation_study(page, ['文档中心'])
    with page.expect_popup() as page_info:
        page.locator(
            ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content"
            " > .content-left > .content-container > div:nth-child(4) > .item-title > .link").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.locator("#left img")).to_be_visible()
    page1.close()
    return page


def click_24_03_lts_documents(page: sync_api.Page):
    """ 点击24.03 LTS文档 """
    navigation_study(page, ['文档中心'])
    with page.expect_popup() as page1_info:
        page.locator(
            ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > .content-right > div > div > div > .link").first.click()
    page1 = page1_info.value
    page1.wait_for_timeout(1000)
    expect(page1.get_by_role("img", name="logo")).to_be_visible()
    page1.close()
    return page


def click_installation_upgrade(page: sync_api.Page):
    """ 点击安装升级 """
    navigation_study(page, ['文档中心'])
    with page.expect_popup() as page_info:
        page.locator(
            ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
            ".content-right > div > div > div:nth-child(2) > .link").click()
    page1 = page_info.value
    page1.wait_for_timeout(1000)
    expect(page1.get_by_role("heading", name="安装指南")).to_be_visible()
    page1.close()
    return page


def click_document_writing_guide(page: sync_api.Page):
    """ 点击文档编写指南 """
    navigation_study(page, ['文档中心'])
    with page.expect_popup() as page_info:
        page.locator(
            ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
            " .content-right > div > div > div:nth-child(3) > .link").click()
    page1 = page_info.value
    page1.wait_for_timeout(3000)
    expect(page1.get_by_text("openEuler/docs", exact=True)).to_be_visible()
    page1.close()
    return page


def click_man_pages(page: sync_api.Page):
    """ 点击man手册 """
    navigation_study(page, ['文档中心'])
    with page.expect_popup() as page_info:
        page.locator(
            ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
            " .content-right > div > div > div:nth-child(4) > .link").click()
    page1 = page_info.value
    page1.wait_for_timeout(1000)
    expect(page1.get_by_role("heading", name="Man Pages")).to_be_visible()
    page1.close()
    return page


def click_course_center(page: sync_api.Page):
    """ 点击课程中心 """
    navigation_study(page, ['课程中心'])
    page.locator(".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > .content-left > div").first.click()
    expect(page.get_by_role("heading", name="课程中心")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def click_start_learning(page: sync_api.Page, arglist: list):
    """ 点击开始学习 """
    navigation_study(page, ['课程中心'])
    if arglist[0] == 'HCIA':
        page.locator(
            ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content "
            "> .content-left > .content-container > div > .system-container > div").first.click()
        expect(page.get_by_role("heading", name="HCIA-openEuler 认证培训课程")).to_be_visible()
        page.wait_for_timeout(1500)
    elif arglist[0] == 'openEuler安全知识培训':
        with page.expect_popup() as page_info:
            page.locator("li").filter(has_text="学习文档中心课程中心迁移与运维技术展示课程中心 HCIA-").get_by_role(
                "link").nth(2).click()
        page1 = page_info.value
        page1.wait_for_timeout(2000)
        expect(page1.get_by_role("link", name="TA的合集和视频列表")).to_be_visible()
        page1.wait_for_timeout(1000)
        page1.close()
    return page


def click_apply_for_exam(page: sync_api.Page, arglist: list):
    """ 点击报名考试 """
    navigation_study(page, ['课程中心'])
    if arglist[0] == 'HCIA':
        with page.expect_popup() as page_info:
            page.locator("li").filter(has_text="学习文档中心课程中心迁移与运维技术展示课程中心 HCIA-").get_by_role(
                "link").first.click()
        page1 = page_info.value
        page1.wait_for_timeout(1000)
        expect(page1.get_by_text("认证学习")).to_be_visible()
        page1.wait_for_timeout(1000)
        page1.close()
    elif arglist[0] == 'openEuler安全知识培训':
        page.locator(
            ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
            ".content-left > .content-container > div:nth-child(3) > .system-container > div").click()
        expect(page.get_by_role("heading", name="openEuler基础安全意识与能力评估考试相关资料及要求")).to_be_visible()
        page.wait_for_timeout(1000)
    return page


def click_openeuler_best_courses(page: sync_api.Page):
    """ 点击openEuler精品课程 """
    navigation_study(page, ['课程中心'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="学习文档中心课程中心迁移与运维技术展示课程中心 HCIA-").get_by_role(
            "link").nth(1).click()
    page1 = page_info.value
    page1.wait_for_timeout(5000)
    expect(page1.get_by_role("img", name="logo")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_tutorials(page: sync_api.Page):
    """ 点击tutorials """
    navigation_study(page, ['课程中心'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="学习文档中心课程中心迁移与运维技术展示课程中心 HCIA-").get_by_role(
            "link").nth(3).click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.locator(".bili-avatar-img")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_openeuler_live(page: sync_api.Page):
    """ 点击openEuler直播 """
    navigation_study(page, ['课程中心'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > ."
        "nav-sub-content > .content-left > .content-container > div:nth-child(5) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="直播")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def click_migrate_openeuler_os(page: sync_api.Page):
    """ 点击从入门到精通-openEuler操作系统迁移专题 """
    navigation_study(page, ['课程中心'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="学习文档中心课程中心迁移与运维技术展示课程中心 HCIA-").get_by_role(
            "link").nth(4).click()
    page1 = page_info.value
    page1.wait_for_timeout(4000)
    expect(page1.locator("#breacrumb-box").get_by_text("半月智谈")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_migration_center(page: sync_api.Page):
    """ 进入迁移专区 """
    navigation_study(page, ['迁移与运维'])
    page.locator(".active > .nav-dropdown > .nav-drop-content > "
                 ".nav-sub-content > .content-left > .content-container > div > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="我们的优势")).to_be_visible()
    page.wait_for_timeout(2000)
    return page


def enter_operation_center(page: sync_api.Page):
    """ 进入运维专区 """
    navigation_study(page, ['迁移与运维'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .n"
        "av-sub-content > .content-left > .content-container > div:nth-child(2) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="运维专区")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def click_x2openeuler_migration_tool(page: sync_api.Page):
    """ 点击x2openEuler迁移工具 """
    navigation_study(page, ['迁移与运维'])
    page.locator(".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
                 " .content-right > div > div > div > .link").first.click()
    expect(page.get_by_role("heading", name="x2openEuler")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def click_migration_practice(page: sync_api.Page):
    """ 点击迁移实践 """
    navigation_study(page, ['迁移与运维'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub"
        "-content > .content-right > div > div > div:nth-child(2) > .link").click()
    expect(page.get_by_text("最佳实践", exact=True)).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_user_case(page: sync_api.Page):  # 进入用户案例
    """ 进入用户案例 """
    navigation_study(page, ['技术展示'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > ."
        "nav-sub-content > .content-left > .content-container > div > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="用户案例")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_white_paper(page: sync_api.Page):
    """ 进入白皮书 """
    navigation_study(page, ['技术展示'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > ."
        "nav-sub-content > .content-left > .content-container > div:nth-child(2) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="白皮书")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_market_research_report(page: sync_api.Page):
    """ 进入市场调研报告 """
    navigation_study(page, ['技术展示'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > "
        ".nav-sub-content > .content-left > .content-container > div:nth-child(3) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="市场研究报告")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


# 导航-开发
def navigation_develop(page: sync_api.Page, arglist: list):
    """ 导航到开发 """
    options = {
        '构建': '.active > .nav-dropdown > .nav-drop-content > .nav-sub > .active',
        '测试': '.active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(2)',
        '发布': '.active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(3)',
        '分析': '.active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(4)',
        '问题反馈': '.active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(5)',
    }

    if arglist[0] in options:
        page.get_by_text("开发", exact=True).click()
        page.locator(options[arglist[0]]).click()
        page.wait_for_timeout(2000)

    return page


def enter_euler_maker(page: sync_api.Page):
    """ 进入openEuler Maker """
    navigation_develop(page, ['构建'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="开发构建测试发布分析问题反馈构建EulerMaker").get_by_role(
            "link").first.click()
    page1 = page_info.value
    page1.wait_for_timeout(6000)
    expect(page1.get_by_role("button", name="登录")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_compass_ci(page: sync_api.Page):
    """ 进入openEuler Compass CI """
    navigation_develop(page, ['构建'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="开发构建测试发布分析问题反馈构建EulerMaker").get_by_role("link").nth(
            1).click()
    page1 = page_info.value
    page1.wait_for_timeout(3000)
    expect(page1.get_by_role("menuitem", name="测试汇总")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def enter_user_software_warehouse(page: sync_api.Page):
    """ 进入openEuler用户软件仓库 """
    navigation_develop(page, ['构建'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="开发构建测试发布分析问题反馈构建EulerMaker").get_by_role("link").nth(
            2).click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("heading", name="Recent Projects")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_software_package_contribution(page: sync_api.Page):
    """ 进入openEuler软件包贡献 """
    navigation_develop(page, ['构建'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="开发构建测试发布分析问题反馈构建EulerMaker").get_by_role("link").nth(
            3).click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_text("贡献软件包").first).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_license_tool_portal(page: sync_api.Page):
    """ 进入openEuler许可证工具门户 """
    navigation_develop(page, ['构建'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="开发构建测试发布分析问题反馈构建EulerMaker").get_by_role("link").nth(
            4).click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_text("貂蝉 License Show Room")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_euler_test(page: sync_api.Page):
    """ 进入openEuler测试 """
    navigation_develop(page, ['测试'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="开发构建测试发布分析问题反馈测试EulerTest 基于").get_by_role("link").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_text("radiaTest")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_euler_publisher(page: sync_api.Page):
    """ 进入openEuler发布 """
    navigation_develop(page, ['发布'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="开发构建测试发布分析问题反馈发布").get_by_role("link").first.click()
    page1 = page_info.value
    page1.wait_for_timeout(3000)
    expect(page1.get_by_text("openEuler/eulerpublisher", exact=True)).to_be_visible()
    page1.close()
    return page


def enter_euler_launcher(page: sync_api.Page):
    """ 进入openEuler Launcher """
    navigation_develop(page, ['发布'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="开发构建测试发布分析问题反馈发布").get_by_role("link").nth(1).click()
    page1 = page_info.value
    page1.wait_for_timeout(3000)
    expect(page1.locator("a").filter(has_text=re.compile(r"^eulerlauncher$"))).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_oepkgs(page: sync_api.Page):
    """ 进入oepkgs """
    navigation_develop(page, ['发布'])
    with (page.expect_popup() as page_info):
        page.locator("li").filter(has_text="开发构建测试发布分析问题反馈发布"
                                  ).get_by_role("link").nth(2).click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("img", name="logo-176-")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_oecp(page: sync_api.Page):
    """ 进入oecp """
    navigation_develop(page, ['分析'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="开发构建测试发布分析问题反馈分析oecp").get_by_role("link").first.click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.locator("a").filter(has_text=re.compile(r"^oecp$"))).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_pkgship(page: sync_api.Page):
    """ 进入pkgship """
    navigation_develop(page, ['分析'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="开发构建测试发布分析问题反馈分析oecp").get_by_role("link").nth(1).click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("heading", name="Packages in the palm of your")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_quick_issue(page: sync_api.Page, arglist: list):
    """ 进入快速反馈 """

    if arglist[0] == "问题反馈":
        navigation_develop(page, ['问题反馈'])
        with page.expect_popup() as page_info:
            page.locator("li").filter(has_text="开发构建测试发布分析问题反馈问题反馈QuickIssue").get_by_role(
                "link").click()
        page1 = page_info.value
        page1.wait_for_timeout(2000)
        expect(page1.get_by_role("button", name="提交 Issue")).to_be_visible()
        page1.wait_for_timeout(1000)
        page1.close()
        return page
    elif arglist[0] == "支持与服务":
        navigation_support(page, ['支持与服务'])
        with page.expect_popup() as page_info:
            page.locator("li").filter(has_text="支持兼容性专区支持与服务支持与服务").get_by_role("link").nth(1).click()
        page1 = page_info.value
        page1.wait_for_timeout(2000)
        expect(page1.get_by_role("button", name="提交 Issue")).to_be_visible()
        page1.wait_for_timeout(1000)
        page1.close()
        return page


# 导航-支持
def navigation_support(page: sync_api.Page, arglist: list):
    """ 导航到支持 """
    if arglist[0] in ["支持与服务", "兼容性专区"]:
        page.get_by_text("支持", exact=True).click()

        if arglist[0] == "支持与服务":
            element_selector = ".active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(2)"
        else:  # arglist[0] == "兼容性专区"
            element_selector = ".active > .nav-dropdown > .nav-drop-content > .nav-sub > .active"

        page.locator(element_selector).click()
        page.wait_for_timeout(2000)

    return page


def enter_compatibility_list(page: sync_api.Page):
    """ 进入兼容性列表 """
    navigation_support(page, ['兼容性专区'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > ."
        "nav-sub-content > .content-left > .content-container > div > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="兼容性列表")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_compatibility_tech_assessment(page: sync_api.Page):
    """ 进入兼容性技术评估 """
    navigation_support(page, ['兼容性专区'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="支持兼容性专区支持与服务兼容性专区兼容性列表 查看").get_by_role(
            "link").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_openeuler_hardware_compatibility_test_intro(page: sync_api.Page):
    """ 点击openEuler硬件兼容性测试介绍 """
    navigation_support(page, ['兼容性专区'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
        ".content-right > div > div > .shortcut > .link").click()
    page.wait_for_timeout(1000)
    expect(page.get_by_role("heading", name="简介")).to_be_visible()
    page.wait_for_timeout(3000)
    return page


def enter_x2openeuler(page: sync_api.Page):
    """ 进入x2openEuler """
    navigation_support(page, ['支持与服务'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="支持兼容性专区支持与服务支持与服务x2openEuler").get_by_role(
            "link").first.click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("treeitem", name="x2openEuler介绍")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def enter_osv_tech_assessment(page: sync_api.Page):
    """ 进入OSV技术评估 """
    navigation_support(page, ['支持与服务'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-"
        "content > .content-left > .content-container > div:nth-child(2) > .item-title > .link").click()
    page.wait_for_timeout(2000)
    expect(page.get_by_role("heading", name="OSV技术测评列表")).to_be_visible()
    page.wait_for_timeout(2500)
    page.go_back()
    return page


def enter_security_center(page: sync_api.Page):
    """ 进入安全中心 """
    navigation_support(page, ['支持与服务'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > ."
        "nav-sub-content > .content-left > .content-container > div:nth-child(3) > .system-container > div").first.click()
    expect(page.get_by_role("heading", name="安全中心")).to_be_visible()
    page.wait_for_timeout(2000)
    return page


def enter_defect_center(page: sync_api.Page):
    """ 进入缺陷中心 """
    navigation_support(page, ['支持与服务'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > ."
        "nav-sub-content > .content-left > .content-container > div:nth-child(3) > .system-container > div:nth-child(2)").click()
    expect(page.get_by_role("heading", name="缺陷中心")).to_be_visible()
    page.wait_for_timeout(1500)
    return page


def enter_faq_common_questions(page: sync_api.Page):
    """ 进入常见问题FAQ """
    navigation_support(page, ['支持与服务'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > "
        ".nav-sub-content > .content-left > .content-container > div:nth-child(4) > .item-title > .link").click()
    expect(page.get_by_role("link", name="通用")).to_be_visible()
    page.wait_for_timeout(2500)
    return page


def enter_osv_tech_assessment_intro(page: sync_api.Page):
    """ 进入OSV技术评估介绍 """
    navigation_support(page, ['支持与服务'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-right > div > div > div > .link").first.click()
    expect(page.get_by_text("OSV技术测评步骤")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


# 导航-社区
def navigation_community(page: sync_api.Page, arglist: list):
    """ 导航到社区 """
    # 社区的菜单项映射
    menu_mapping = {
        "关于社区": ".active > .nav-dropdown > .nav-drop-content > .nav-sub > .active",
        "贡献与成长": ".active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(2)",
        "项目": ".active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(3)",
        "社区交流": ".active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(4)"
    }

    # 获取用户选择的菜单项
    selected_option = arglist[0]

    # 如果选项在映射中，执行点击操作
    if selected_option in menu_mapping:
        page.get_by_text("社区", exact=True).click()
        page.locator(menu_mapping[selected_option]).click()

    page.wait_for_timeout(2000)
    return page


def enter_organization_structure(page: sync_api.Page):
    """ 进入组织结构 """
    navigation_community(page, ['关于社区'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > "
        ".nav-sub-content > .content-left > .content-container > div > .item-title > .link").first.click()
    expect(page.get_by_role("complementary").get_by_text("组织架构")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_community_charter(page: sync_api.Page):
    """ 进入社区章程 """
    navigation_community(page, ['关于社区'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > "
        ".nav-sub-content > .content-left > .content-container > div:nth-child(2) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="openEuler项目群开源治理制度")).to_be_visible()
    page.wait_for_timeout(2000)
    return page


def enter_member_units(page: sync_api.Page):
    """ 进入成员单位 """
    navigation_community(page, ['关于社区'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content >"
        " .nav-sub-content > .content-left > .content-container > div:nth-child(3) > .item-title > .link").click()
    page.wait_for_timeout(3000)
    expect(page.get_by_role("link", name="战略捐赠人")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_community_honor(page: sync_api.Page):
    """ 进入社区荣誉 """
    navigation_community(page, ['关于社区'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content >"
        " .nav-sub-content > .content-left > .content-container > div:nth-child(4) > .item-title > .link").click()
    page.wait_for_timeout(1000)
    expect(page.get_by_role("heading", name="社区荣誉")).to_be_visible()
    page.wait_for_timeout(1500)
    return page


def enter_oeep(page: sync_api.Page):
    """ 进入OEEP """
    navigation_community(page, ['关于社区'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content >"
        " .nav-sub-content > .content-left > .content-container > div:nth-child(5) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="索引:")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_city_user_group(page: sync_api.Page):
    """ 进入城市用户组 """
    navigation_community(page, ['关于社区'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-left > .content-container > div:nth-child(6) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="openEuler 用户组")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_contribution_board(page: sync_api.Page):
    """ 进入贡献板 """
    navigation_community(page, ['关于社区'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="社区关于社区贡献与成长项目社区交流关于社区组织架构 了解").get_by_role(
            "link").first.click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("img", name="logo")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_openeuler_community_intro_pdf(page: sync_api.Page):
    """ 进入openEuler社区介绍pdf """
    navigation_community(page, ['关于社区'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="社区关于社区贡献与成长项目社区交流关于社区组织架构 了解").get_by_role(
            "link").nth(1).click()
    page1 = page_info.value
    current_url = page1.url
    # print(current_url)
    assert current_url == ("https://www.openeuler.org/whitepaper/openEuler%20"
                           "%E5%BC%80%E6%BA%90%E7%A4%BE%E5%8C%BA%E4%BB%8B%E7%BB%8D.pdf"), "URL 不匹配！"
    page1.wait_for_timeout(3000)
    page1.close()
    return page


def enter_sig_center(page: sync_api.Page):
    """ 进入SIG中心 """
    navigation_community(page, ['贡献与成长'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
        ".content-left > div > div > .content-container > div > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="SIG中心")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_contribution_strategy(page: sync_api.Page):
    """ 进入贡献策略 """
    navigation_community(page, ['贡献与成长'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-left > div > div > .content-container > div:nth-child(2) > .item-title > .link").first.click()
    expect(page.get_by_role("tab", name="贡献攻略地图")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_cla_sign(page: sync_api.Page):
    """ 进入CLA签署 """
    navigation_community(page, ['贡献与成长'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="社区关于社区贡献与成长项目社区交流贡献与成长开发者贡献").get_by_role(
            "link").first.click()
    page1 = page_info.value
    expect(page1.get_by_text("Signing CLA Guide for")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def enter_high_schools(page: sync_api.Page):
    """ 进入高校 """
    navigation_community(page, ['贡献与成长'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-left > div > div:nth-child(2) > .content-container > div > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="高校", exact=True)).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_talent_recruitment(page: sync_api.Page):
    """ 进入人才培养 """
    navigation_community(page, ['贡献与成长'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
        ".content-left > div > div:nth-child(2) > .content-container > div:nth-child(2) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="人才培养")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_open_internship(page: sync_api.Page):
    """ 进入开源实习 """
    navigation_community(page, ['贡献与成长'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-left > div > div:nth-child(2) > .content-container > div:nth-child(3) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="openEuler开源实习")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_enterprise_cla_process(page: sync_api.Page):
    """ 进入企业CLA流程 """
    navigation_community(page, ['贡献与成长'])
    page.locator(".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
                 " .content-right > div > div > div > .link").first.click()
    page.wait_for_timeout(3000)
    expect(page.get_by_role("heading", name="企业签署 CLA ，正式加入 openEuler 社区的流程")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_cla_faq(page: sync_api.Page):
    """ 进入CLA常见问题FAQ """
    navigation_community(page, ['贡献与成长'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="社区关于社区贡献与成长项目社区交流贡献与成长开发者贡献").get_by_role(
            "link").nth(1).click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("heading", name="指引视频")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_developer_calendar(page: sync_api.Page):
    """ 进入开发日历 """
    navigation_community(page, ['贡献与成长'])
    page.locator(".active > .nav-dropdown > .nav-drop-content >"
                 " .nav-sub-content > .content-right > div > div > div:nth-child(3) > .link").click()
    page.wait_for_timeout(1000)
    return page


def enter_activities_competitions(page: sync_api.Page):
    """ 进入活动与大赛 """
    navigation_community(page, ['贡献与成长'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-right > div > div > div:nth-child(4) > .link").click()
    expect(page.get_by_role("heading", name="活动与大赛")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_high_school_technical_group(page: sync_api.Page):
    """ 进入高校技术小组 """
    navigation_community(page, ['贡献与成长'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
        ".content-right > div > div > div:nth-child(5) > .link").click()
    expect(page.get_by_role("heading", name="高校", exact=True)).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_a_tune(page: sync_api.Page):
    """ 进入a_tune"""
    navigation_community(page, ['项目'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
        ".content-left > .content-container > div > .item-title > .link").first.click()
    page.wait_for_timeout(2000)
    expect(page.get_by_role("heading", name="A-Tune")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_isula(page: sync_api.Page):
    """ 进入isula """
    navigation_community(page, ['项目'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-left > .content-container > div:nth-child(2) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="iSula")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_stratovirt(page: sync_api.Page):
    """ 进入stratovirt """
    navigation_community(page, ['项目'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
        ".content-left > .content-container > div:nth-child(3) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="StratoVirt")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_bisheng_jdk(page: sync_api.Page):
    """ 进入bisheng_jdk """
    navigation_community(page, ['项目'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-left > .content-container > div:nth-child(4) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="毕昇JDK")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_secgear(page: sync_api.Page):
    """ 进入secgear """
    navigation_community(page, ['项目'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-left > .content-container > div:nth-child(5) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="secGear")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_nestos(page: sync_api.Page):
    """ 进入nestos """
    navigation_community(page, ['项目'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(has_text="社区关于社区贡献与成长项目社区交流项目A-Tune").get_by_role("link").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("heading", name="NestOS")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_forum(page: sync_api.Page):
    """ 进入论坛 """
    navigation_community(page, ['社区交流'])
    with page.expect_popup() as page_info:
        page.locator("li").filter(
            has_text="社区关于社区贡献与成长项目社区交流社区交流论坛 与开发者讨论openEuler邮件列表 订阅邮件列表，与SIG成员讨论openEuler").get_by_role(
            "link").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.locator("header").get_by_role("link").nth(1)).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_mail_list(page: sync_api.Page):
    """ 进入邮件列表 """
    navigation_community(page, ['社区交流'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
        ".content-left > .content-container > div:nth-child(2) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="邮件列表")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_online_meeting(page: sync_api.Page):
    """ 进入线上会议 """
    navigation_community(page, ['社区交流'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
        ".content-left > .content-container > div:nth-child(3) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="线上会议")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_contact_us(page: sync_api.Page):
    """ 进入联系我们 """
    navigation_community(page, ['社区交流'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-left > .content-container > div:nth-child(4) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="联系我们")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


# 导航-动态
def navigation_dynamic(page: sync_api.Page, arglist: list):
    """ 导航-动态 """
    if arglist[0] == "社区活动":
        page.get_by_text("动态", exact=True).click()
        page.locator(".active > .nav-dropdown > .nav-drop-content > .nav-sub > .active").click()
    elif arglist[0] == "资讯":
        page.get_by_text("动态", exact=True).click()
        page.locator(".active > .nav-dropdown > .nav-drop-content > .nav-sub > div:nth-child(2)").click()
    page.wait_for_timeout(2000)
    return page


def enter_activity_calendar(page: sync_api.Page):
    """ 进入活动日历 """
    navigation_dynamic(page, ['社区活动'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-left > .content-container > div > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="活动")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_summit(page: sync_api.Page):
    """ 进入峰会 """
    navigation_dynamic(page, ['社区活动'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
        ".content-left > .content-container > div:nth-child(2) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="活动日程")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def enter_openeuler_call_for_x_plan(page: sync_api.Page):
    """ 进入openEuler X计划 """
    navigation_dynamic(page, ['社区活动'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > .content-left "
        "> .content-container > div:nth-child(3) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="openEuler Call for X 计划")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def operation_system_conference_openeuler_summit_2024(page: sync_api.Page):
    """ 进入openEuler 2024年度操作系统年会 """
    navigation_dynamic(page, ['社区活动'])
    page.locator("li").filter(has_text="动态社区活动资讯社区活动活动日历 了解openEuler").get_by_role("paragraph").nth(
        3).click()
    expect(page.get_by_role("heading", name="活动日程")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def openeuler_sig_gathering_2024(page: sync_api.Page):
    navigation_dynamic(page, ['社区活动'])
    page.locator(".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
                 " .content-right > div > div > div:nth-child(2) > .review-content > .review-title").click()
    page.get_by_text("活动简介").click()
    page.wait_for_timeout(1000)
    return page


def click_news(page: sync_api.Page):
    """ 点击新闻 """
    navigation_dynamic(page, ['资讯'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content > "
        ".content-left > .content-container > div > .item-title > .link").first.click()
    expect(page.get_by_role("heading", name="新闻")).to_be_visible()
    page.wait_for_timeout(1000)
    page.go_back()
    return page


def click_blog(page: sync_api.Page):
    """ 点击博客 """
    navigation_dynamic(page, ['资讯'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-left > .content-container > div:nth-child(2) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="博客", exact=True)).to_be_visible()
    page.wait_for_timeout(1000)
    page.go_back()
    return page


def click_monthly(page: sync_api.Page):
    """ 点击月刊 """
    navigation_dynamic(page, ['资讯'])
    page.locator(
        ".active > .nav-dropdown > .nav-drop-content > .nav-sub-content >"
        " .content-left > .content-container > div:nth-child(3) > .item-title > .link").click()
    expect(page.get_by_role("heading", name="月刊")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def openeuler_2023_community_annual_report(page: sync_api.Page):
    """ 进入openEuler 2023年度社区年报 """
    navigation_dynamic(page, ['资讯'])
    page.locator("li").filter(has_text="动态社区活动资讯资讯新闻 查看openEuler").get_by_role("paragraph").nth(3).click()
    expect(page.get_by_role("heading", name="openEuler 2023 社区年报")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


# 首页操作
def new_guide(page: sync_api.Page):
    """ 新手指引 """
    for i in range(13):  # 点击“下一步”按钮10次
        page.get_by_role("button", name="下一步").click()
        page.wait_for_timeout(1000)
    page.get_by_role("button", name="知道了").click()
    page.wait_for_timeout(1000)
    expect(page.locator("#tour_headerNav_tool").get_by_role("img").nth(3)).to_be_visible()
    return page


def skip_new_guide(page: sync_api.Page):
    """ 跳过新手指引 """
    page.get_by_text("跳过").click()
    return page


def change_home_banner(page: sync_api.Page):
    """ 切换首页banner """
    page.locator(".swiper-button-next").click()
    page.wait_for_timeout(1500)
    page.locator(".swiper-button-next").click()
    page.wait_for_timeout(1500)
    page.locator(".swiper-button-next").click()
    page.wait_for_timeout(1500)
    page.locator(".swiper-button-next").click()
    page.wait_for_timeout(1500)
    return page


def enter_technical_white_paper(page: sync_api.Page):
    """ 进入技术白皮书 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="openEuler 技术白皮书 了解openEuler").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="白皮书")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def enter_security_center_home(page: sync_api.Page):
    """ 进入安全中心 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="openEuler 安全中心 查看安全公告等安全问题").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="安全中心")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def enter_migration_center_home(page: sync_api.Page):
    """ 进入迁移中心 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="openEuler 迁移专区 教你替换操作系统成").click()
    page1 = page_info.value
    expect(page1.get_by_text("迁移专区", exact=True)).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def enter_summits_home(page: sync_api.Page):
    """ 进入活动专区 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="openEuler 活动专区 了解openEuler最新活动").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="活动")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def suspended_window_feedback(page: sync_api.Page, arglist: list):
    """ 悬浮窗反馈 """
    page.get_by_role("button", name="全部接受").click()
    page.wait_for_timeout(1000)
    page.locator("#feedback").get_by_role("img").first.click()
    page.wait_for_timeout(1000)
    page.locator(f"div:nth-child(3) > div:nth-child({arglist[0]})").first.click()  # 9,8,7,6,5
    page.wait_for_timeout(1000)
    page.get_by_placeholder("改进哪些方面会让您更愿意推荐？").fill(arglist[1])
    page.get_by_role("button", name="提交").click()
    page.wait_for_timeout(1000)
    return page


def click_support_diversity_devices(page: sync_api.Page):
    """ 点击支持多样化设备 """
    page.get_by_text("支持多样性设备").click()
    expect(page.get_by_role("img", name="openEuler", exact=True).nth(4)).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def click_cover_all_scene_applications(page: sync_api.Page):
    """ 点击覆盖全场景应用 """
    page.get_by_text("覆盖全场景应用").click()
    expect(page.get_by_role("img", name="openEuler", exact=True).nth(4)).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def click_complete_development_toolchain(page: sync_api.Page):
    """ 点击完整开发工具链 """
    page.get_by_text("完整开发工具链").click()
    expect(page.get_by_role("img", name="openEuler", exact=True).nth(4)).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def click_get_openeuler_home(page: sync_api.Page):
    """ 点击首页获取openEuler """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="获取openEuler", exact=True).click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="获取openEuler操作系统")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_contribution_strategy_home(page: sync_api.Page):
    """ 点击首页贡献策略 """
    with page.expect_popup() as page_info:
        page.get_by_role("button", name="贡献攻略").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="贡献攻略")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_sig_center_home(page: sync_api.Page):
    """ 点击首页SIG中心 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="进入SIG中心").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="SIG中心")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_member_units_home(page: sync_api.Page):
    """ 点击首页会员单位 """
    with page.expect_popup() as page_info:
        page.get_by_role("button", name="成员单位").click()
    page1 = page_info.value
    expect(page1.get_by_role("complementary").get_by_text("成员单位")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_view_donation_benefits_home(page: sync_api.Page):
    """ 点击查看捐赠收益 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="查看捐赠权益").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="第八条 项目群捐赠人的开源治理参与方式")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_user_cases(page: sync_api.Page, arglist: list):
    """ 点击用户案例 """
    if arglist[0] == "金融":
        # page.wait_for_timeout(1000)
        page.get_by_text("金融").click()
        # page.wait_for_timeout(1000)
        expect(page.get_by_role("main")).to_contain_text("三湘银行基于麒麟信安打造银行IT信息化系统安全底座")
        expect(page.get_by_role("main")).to_contain_text("天弘基金以服务器操作系统配合完成邮件与OA的改造")
        expect(page.get_by_role("main")).to_contain_text(
            "中国建设银行分布式信用卡核心业务系统，单日交易量超过 1 亿笔，峰值TPS超过 6000")
        expect(page.get_by_role("main")).to_contain_text("兴业银行某核心业务系统国产化改造项目")
    elif arglist[0] == "运营商":
        # page.wait_for_timeout(1000)
        page.get_by_text("运营商").click()
        # page.wait_for_timeout(1000)
        expect(page.get_by_role("main")).to_contain_text(
            "联通系统集成公司联通智能化运营平台 完成全生命周期运营平台的平稳迁移")
        expect(page.get_by_role("main")).to_contain_text(
            "中国移动中移苏州研究院完成服务器操作系统无感知迁移，实现业务高效稳定运行")
        expect(page.get_by_role("main")).to_contain_text("中国移动云能力中心打造运营商行业级迁移解决方案")
        expect(page.get_by_role("main")).to_contain_text("天翼云科技有限公司", expected=True)
        expect(page.get_by_role("main")).to_contain_text(
            "基于stratovirt的安全容器为函数计算提供完善的租户隔离和安全运行环境，并且在内存底噪、启动速度、并发、密度上具备较大优势。",
            expected=True)
    elif arglist[0] == "能源":
        page.wait_for_timeout(1000)
        page.get_by_text("能源").click()
        # page.wait_for_timeout(1000)
        expect(page.get_by_role("main")).to_contain_text(
            "中国电建集团华东勘测设计研究院有限公司面向新能源领域的国产操作系统O-PowerOS",expected=True)
        expect(page.get_by_role("main")).to_contain_text("国家电网基于openEuler实现等保四级安全防护建设")
        expect(page.get_by_role("main")).to_contain_text("迁移适配后产品支持多架构，部署时长大幅降低")
        expect(page.get_by_role("main")).to_contain_text(
            "国家电网“国家电网河北智慧标杆站” 智慧工地系统，平滑完成操作系统创新，实现业务高效稳定运行")
    elif arglist[0] == "物流":
        # page.wait_for_timeout(1000)
        page.get_by_text("物流").click()
        expect(page.get_by_role("main")).to_contain_text("中国邮政OA 业务系统迁移改造")

    elif arglist[0] == "高校&科研":
        # page.wait_for_timeout(1000)
        page.get_by_text("高校&科研").click()
        # page.wait_for_timeout(1000)
        expect(page.get_by_role("main")).to_contain_text(
            "华中科技大学/武汉理工大学基于openEuler+鲲鹏打造超大规模计算流体力学平台")
        expect(page.get_by_role("main")).to_contain_text("上海交通大学交大“交我算”计算集群：共建openEuler开源技术新生态")
        expect(page.get_by_role("main")).to_contain_text("兰州大学openEuler + 鲲鹏全栈实现HPC性能倍增")
        expect(page.get_by_role("main")).to_contain_text(
            "南京信息工程大学极端高温干旱天气模拟与预测平台，有效及时发现预警极端气候，提升应急处置能力，性能提升58%")
    elif arglist[0] == "云计算":
        # page.wait_for_timeout(1000)
        page.get_by_text("云计算").click()
        # page.wait_for_timeout(1000)
        expect(page.get_by_role("main")).to_contain_text(
            "中国电信中国电信天翼云基于 openEuler 打造CTyunOS，服务电信集团云改数转战略，助力数字经济发展")
        expect(page.get_by_role("main")).to_contain_text("中国移动云能力中心基于openEuler的安全可信技术探索和实践")
        expect(page.get_by_role("main")).to_contain_text(
            "云宏信息科技股份有限公司同比例虚拟机计算性能翻倍，金融行业上云效率提高")
        expect(page.get_by_role("main")).to_contain_text("深信服科技股份有限公司基于openEuler实现桌面云提质降本")
    elif arglist[0] == "其他":
        # page.wait_for_timeout(1000)
        page.get_by_text("其他").click()
        expect(page.get_by_role("main")).to_contain_text("东方通DPI流量采集平台V2.0确保网络环境的安全和高效运行")
        expect(page.get_by_role("main")).to_contain_text(
            "四川中电启明星技术有限公司性能卓越，稳定可靠，环境级高可用， 智能运维，安全性，自主可控，可移植、易操作")
        expect(page.get_by_role("main")).to_contain_text(
            "科来网络技术股份有限公司基于openEuler打造全流量安全分析解决方案，助力用户提升安全防御水平。")
        expect(page.get_by_role("main")).to_contain_text(
            "新华社新华社科技创新应用项目共筑 AI 创新方案安全智能加速内容生态建设")
    return page


def more_user_cases(page: sync_api.Page):
    """ 点击查看更多案例 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="查看更多").first.click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="用户案例")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_contribution_details(page: sync_api.Page):
    """ 点击查看贡献详情 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="查看贡献详情").click()
    page1 = page_info.value
    expect(page1.get_by_role("img", name="logo")).to_be_visible()
    page.wait_for_timeout(1000)
    page1.close()
    return page


def assert_community_dynamic_data(page: sync_api.Page):
    """ 断言社区活力数据 """
    assert page.locator(".data-item").first.inner_text() is not None, "社区动态数据不存在"
    assert page.locator(".data-item").nth(1).inner_text() is not None, "社区动态数据不存在"
    assert page.locator(".data-item").nth(2).inner_text() is not None, "社区动态数据不存在"
    assert page.locator(".data-item").nth(3).inner_text() is not None, "社区动态数据不存在"
    assert page.locator(".data-item").nth(4).inner_text() is not None, "社区动态数据不存在"
    page.wait_for_timeout(1000)
    return page


def assert_blog_data_and_more(page: sync_api.Page):
    """ 断言博客数据和查看更多 """
    page.get_by_role("main").get_by_text("博客").click()
    expect(page.locator(
        ".o-card o-card-layout-v o-card-hoverable o-card-cursor-pointer trend-card trend-blog")).first.to_be_visible()
    page.wait_for_timeout(1000)
    expect(page.locator(".o-card o-card-layout-v o-card-hoverable o-card-cursor-pointer trend-card trend-blog").nth(
        1)).to_be_visible()
    page.wait_for_timeout(1000)
    expect(page.locator(".o-card o-card-layout-v o-card-hoverable o-card-cursor-pointer trend-card trend-blog").nth(
        2)).to_be_visible()
    page.wait_for_timeout(1000)
    expect(page.locator(".o-card o-card-layout-v o-card-hoverable o-card-cursor-pointer trend-card trend-blog").nth(
        3)).to_be_visible()
    page.wait_for_timeout(1000)
    expect(page.locator(".o-card o-card-layout-v o-card-hoverable o-card-cursor-pointer trend-card trend-blog").nth(
        4)).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def home_more_blog(page: sync_api.Page):
    """ 点击首页查看更多博客 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="查看更多").nth(1).click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="博客", exact=True)).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def assert_news_data_and_more(page: sync_api.Page):
    """ 断言新闻数据和查看更多 """
    page.get_by_role("main").get_by_text("新闻").click()
    expect(page.locator(
        ".o-card o-card-layout-v o-card-hoverable o-card-cursor-pointer trend-card")).first.to_be_visible()
    page.wait_for_timeout(1000)
    expect(page.locator(".o-card o-card-layout-v o-card-hoverable o-card-cursor-pointer trend-card").nth(
        1)).to_be_visible()
    page.wait_for_timeout(1000)
    expect(page.locator(".o-card o-card-layout-v o-card-hoverable o-card-cursor-pointer trend-card").nth(
        2)).to_be_visible()
    page.wait_for_timeout(1000)
    expect(page.locator(".o-card o-card-layout-v o-card-hoverable o-card-cursor-pointer trend-card").nth(
        3)).to_be_visible()
    page.wait_for_timeout(1000)
    expect(page.locator(".o-card o-card-layout-v o-card-hoverable o-card-cursor-pointer trend-card").nth(
        4)).to_be_visible()
    page.wait_for_timeout(1000)

    page.wait_for_timeout(1000)
    return page


def home_more_news(page: sync_api.Page):
    """ 点击首页查看更多新闻 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="查看更多").nth(1).click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="新闻")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def calendar_type_switch(page: sync_api.Page):
    """ 日历类型切换 """
    page.wait_for_timeout(1000)
    page.locator("xpath=//div[text()=' 全部']").click()
    page.wait_for_timeout(1000)
    page.locator("xpath=//div[text()=' 会议']").click()
    page.wait_for_timeout(1000)
    page.locator("xpath=//div[text()=' 活动']").click()
    page.wait_for_timeout(1000)
    page.locator("xpath=//div[text()=' 峰会']").click()
    page.wait_for_timeout(1000)
    page.locator("xpath=//div[text()=' 全部']").click()
    page.wait_for_timeout(1000)
    return page


def switch_month(page: sync_api.Page):
    """ 切换月份 """
    page.wait_for_timeout(1000)
    old_month = page.locator(".month-date").inner_text()
    page.locator(".o-icon").nth(14).click()
    new_month = page.locator(".month-date").inner_text()
    assert old_month != new_month, "切换月份失败"
    page.wait_for_timeout(1000)
    return page


def meeting_details_collapse_expand(page: sync_api.Page):
    """ 会议详情折叠/展开 """
    page.wait_for_timeout(1000)
    page.get_by_role("cell", name="05").locator("div").nth(1).click()
    page.get_by_role("button", name="云原生sig例会 SIG组").click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="云原生sig例会 SIG组").click()
    expect(page.get_by_label("云原生sig例会SIG组: sig-")).to_be_visible()
    page.wait_for_timeout(1000)
    return page


def suspended_window_enter_forum(page: sync_api.Page):
    """ 悬浮穿窗口进入论坛 """
    page.get_by_role("button", name="全部接受").click()
    page.locator("#issueback").get_by_role("img").first.click()
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="社区论坛 发帖互助解决各类问题").click()
    page1 = page_info.value
    page1.wait_for_timeout(1000)
    expect(page1.get_by_role("link", name="话题")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def suspended_window_enter_quick_issue(page: sync_api.Page):
    """ 悬浮穿窗口进入快速发布问题 """
    page.reload()
    page.locator("#issueback").get_by_role("img").first.click()
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="QuickIssue 快捷提交/查询社区Issues").click()
    page1 = page_info.value
    page1.wait_for_timeout(1000)
    expect(page1.get_by_role("button", name="提交 Issue")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def suspended_window_enter_faqs(page: sync_api.Page):
    """ 悬浮穿窗口进入常见问题 """
    page.reload()
    page.locator("#issueback").get_by_role("img").first.hover()
    page.wait_for_timeout(1000)
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="FAQs").click()
    page1 = page_info.value
    page1.wait_for_timeout(1000)
    expect(page1.get_by_role("heading", name="openEuler 常见问题")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


# 页脚

def enter_footer_member_units(page: sync_api.Page):
    """ 进入页脚成员单位 """
    with page.expect_popup() as page_info:
        page.locator("#tour_footer").get_by_role("link", name="成员单位").click()
    page1 = page_info.value
    expect(page1.get_by_role("complementary").get_by_text("成员单位")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_organization_structure(page: sync_api.Page):
    """ 进入页脚组织架构 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="组织架构").click()
    page1 = page_info.value
    expect(page1.get_by_role("complementary").get_by_text("组织架构")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_community_charter(page: sync_api.Page):
    """ 进入页脚社区章程 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="社区章程").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="openEuler项目群开源治理制度")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_contribution_board(page: sync_api.Page):
    """ 进入页脚贡献板 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="贡献看板").click()
    page1 = page_info.value
    page1.wait_for_timeout(1000)
    expect(page1.get_by_role("img", name="logo")).to_be_visible()
    page1.wait_for_timeout(500)
    page1.close()
    return page


def enter_footer_community_intro(page: sync_api.Page):
    """ 进入页脚社区介绍 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="社区介绍").click()
    page1 = page_info.value
    current_url = page1.url
    # print(current_url)
    assert current_url == ("https://www.openeuler.org/whitepaper/"
                           "openEuler%20%E5%BC%80%E6%BA%90%E7%A4%BE%E5%8C%BA%E4%BB%8B%E7%BB%8D.pdf"), "URL 不匹配！"
    page1.wait_for_timeout(3000)
    page1.close()
    return page


def enter_footer_news(page: sync_api.Page):
    """ 进入页脚新闻 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="新闻").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="新闻")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_blog(page: sync_api.Page):
    """ 进入页脚博客 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="博客").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="博客", exact=True)).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_white_paper(page: sync_api.Page):
    """ 进入页脚白皮书 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="白皮书", exact=True).click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="白皮书")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_get_openeuler_os(page: sync_api.Page):
    """ 进入页脚获取openEuler操作系统 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="获取openEuler操作系统").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="获取openEuler操作系统")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_latest_community_release(page: sync_api.Page):
    """ 进入页脚最新社区发行版 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="最新社区发行版").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="下载", exact=True)).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_commercial_release(page: sync_api.Page):
    """ 进入页脚商业发行版 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="商业发行版").click()
    page1 = page_info.value
    expect(page1.get_by_role("tab", name="商业发行版")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_software_center(page: sync_api.Page):
    """ 进入页脚软件中心 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="软件中心").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="openEuler软件中心")).to_be_visible()
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def enter_footer_document(page: sync_api.Page):
    """ 进入页脚文档 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="文档").click()
    page1 = page_info.value
    expect(page1.locator("#left img")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_faq(page: sync_api.Page):
    """ 进入页脚FAQ """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="FAQ").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="openEuler 常见问题")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_mail_list(page: sync_api.Page):
    """ 进入页脚邮件列表 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="邮件列表").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="邮件列表")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_contact_us(page: sync_api.Page):
    """ 进入页脚联系我们 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="联系我们").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="联系我们")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_activities(page: sync_api.Page):
    """ 进入页脚活动 """

    with page.expect_popup() as page_info:
        page.get_by_role("link", name="活动", exact=True).click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="活动")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_forum(page: sync_api.Page):
    """ 进入页脚论坛 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="论坛").click()
    page1 = page_info.value
    expect(page1.get_by_role("link", name="话题")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_sig_center(page: sync_api.Page):
    """ 进入页脚SIG中心 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="SIG中心", exact=True).click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="SIG中心")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_contribution_strategy(page: sync_api.Page):
    """ 进入页脚贡献攻略 """
    with page.expect_popup() as page_info:
        page.locator("#tour_footer").get_by_role("link", name="贡献攻略").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="贡献攻略")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def enter_footer_course_center(page: sync_api.Page):
    """ 进入页脚课程中心 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="课程中心").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="课程中心")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def openatom_foundation(page: sync_api.Page):
    """ 点击开放原子开源基金会 """
    with page.expect_popup() as page_info:
        page.locator(".atom > a").click()
    page1 = page_info.value
    expect(page1.get_by_role("link", name="LOGO")).to_be_visible()
    page.wait_for_timeout(1000)
    page1.close()
    return page


def brand(page: sync_api.Page):
    """ 点击品牌 """
    page.get_by_role("button", name="全部接受").click()
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="品牌").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="商标", exact=True)).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page  # 点击品牌


def privacy_policy(page: sync_api.Page):
    """ 点击隐私政策 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="隐私政策").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="隐私政策")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def law_declaration(page: sync_api.Page):
    """ 点击法律声明 """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="法律声明").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="法律声明")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page  # 点击法律声明


def about_cookies(page: sync_api.Page):
    """ 点击关于cookies """
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="关于cookies").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="关于 COOKIES")).to_be_visible()
    page1.wait_for_timeout(1000)
    page1.close()
    return page


def friend(page: sync_api.Page):
    """ 点击友情链接 """
    page.get_by_role("button", name="全部接受").click()
    page.wait_for_timeout(500)
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="木兰开源社区").click()
    page1 = page_info.value
    page1.wait_for_timeout(3000)
    expect(page1.get_by_text("©木兰开源社区")).to_be_visible()
    page1.close()

    with page.expect_popup() as page_info:
        page.get_by_role("link", name="鲲鹏社区").click()
    page2 = page_info.value
    page2.wait_for_timeout(3000)
    expect(page2.get_by_role("link", name="鲲鹏社区", exact=True)).to_be_visible()
    page2.close()

    with page.expect_popup() as page_info:
        page.get_by_role("link", name="鲲鹏小智").click()
    page3 = page_info.value
    page3.wait_for_timeout(3000)
    expect(page3.get_by_text("欢迎使用鲲鹏小智", exact=True)).to_be_visible()
    page3.close()

    with page.expect_popup() as page_info:
        page.get_by_role("link", name="鹏城实验室").click()
    page4 = page_info.value
    page4.wait_for_timeout(3000)
    expect(page4.get_by_role("button", name="首页")).to_be_visible()
    page4.close()

    with page.expect_popup() as page_info:
        page.get_by_role("link", name="infoQ").click()
    page5 = page_info.value
    page5.wait_for_timeout(3000)
    expect(page5.get_by_role("link", name="logo")).to_be_visible()
    page5.close()

    with page.expect_popup() as page_info:
        page.get_by_role("link", name="开源社", exact=True).click()
    page6 = page_info.value
    page6.wait_for_timeout(4000)
    new_url = page6.url
    assert new_url == "https://kaiyuanshe.cn/", "断言失败"
    page6.close()

    with page.expect_popup() as page_info:
        page.get_by_role("link", name="中科微澜").click()
    page7 = page_info.value
    page7.wait_for_timeout(2000)
    page7.get_by_role("button", name="高级").click()
    page7.get_by_role("link", name="继续前往www.vulab.com.cn（不安全）").click()
    page7.wait_for_timeout(2000)
    expect(page7.get_by_role("img")).to_be_visible()
    page7.close()

    with page.expect_popup() as page_info:
        page.get_by_role("link", name="Authing").click()
    page8 = page_info.value
    page8.wait_for_timeout(3000)
    expect(page8.get_by_role("link", name="关于 Authing")).to_be_visible()
    page8.close()

    with page.expect_popup() as page_info:
        page.get_by_role("link", name="openGauss").click()
    page9 = page_info.value
    page9.wait_for_timeout(3000)
    expect(page9.get_by_role("link", name="openGauss logo")).to_be_visible()
    page9.close()

    with page.expect_popup() as page_info:
        page.get_by_role("link", name="昇思MindSpore").click()
    page10 = page_info.value
    page10.wait_for_timeout(3000)
    expect(page10.get_by_role("button", name="我已阅读并同意")).to_be_visible()
    page10.close()

    with page.expect_popup() as page_info:
        page.get_by_role("link", name="Ebaina").click()
    page11 = page_info.value
    page11.wait_for_timeout(3000)
    expect(page11.locator(".logo")).to_be_visible()
    page11.close()

    with page.expect_popup() as page_info:
        page.locator(".links-logo").first.click()
    page12 = page_info.value
    page12.wait_for_timeout(3000)
    expect(page12.get_by_label("OSCHINA")).to_be_visible()
    page12.close()

    with page.expect_popup() as page_info:
        page.locator(".iszh > a:nth-child(2)").click()
    page13 = page_info.value
    page13.wait_for_timeout(3000)
    expect(page13.get_by_role("link", name="CSDN首页")).to_be_visible()
    page13.close()

    with page.expect_popup() as page_info:
        page.locator(".iszh > a:nth-child(3)").click()
    page14 = page_info.value
    page14.wait_for_timeout(3000)
    expect(page14.get_by_role("link", name="稀土掘金")).to_be_visible()
    page14.close()

    with page.expect_popup() as page_info:
        page.locator(".iszh > a:nth-child(4)").click()
    page15 = page_info.value
    page15.wait_for_timeout(3000)
    expect(page15.get_by_role("link", name="首页")).to_be_visible()
    page15.close()

    with page.expect_popup() as page_info:
        page.locator(".iszh > a:nth-child(5)").click()
    page16 = page_info.value
    page16.wait_for_timeout(3000)
    expect(page16.get_by_label("今日头条徽标")).to_be_visible()
    page16.close()

    return page  # 点击友情链接


# 定义字典
def_dict = {
    # 进入环境
    '进入生产环境': open_url,
    '进入测试环境': open_url_test,
    "登录": longin,
    "登录并签署隐私声明": longin_and_sign_privacy_statement,
    "退出登录": logout,

    # 个人中心
    "进入个人中心": enter_user_center,
    "更换头像": change_user_avatar,
    "修改昵称": change_nickname,
    "修改公司": change_company,
    "取消签署协议": cancel_signature,

    # 消息中心
    "进入消息中心": enter_messag2_center,
    "消息标为已读": message_to_read,
    "删除消息": delete_message,
    "消息分页": message_pagesize,
    "消息切页": message_page_change,

    # 导航-下载
    "选择导航-下载": navigation_download,
    "其他获取方式": other_download_way,
    "点击公有云": click_public_cloud,
    "点击容器镜像": click_container_image,
    "点击Windows": click_windows,
    "点击Virtualization": click_virtualization,
    "点击Raspberry Pi": click_raspberry_pi,
    "点击openEuler 24.03 LTS": click_openeuler_24_03_lts,
    "点击镜像仓列表": click_image_warehouse_list,
    "openEuler 24.03 LTS场景筛选": openeuler_24_03_lts_scene_filter,
    "点击openEuler 24.09": click_openeuler_24_09,
    "openEuler 24.09场景筛选": openeuler_24_09_scene_filter,
    "点击openEuler 22.03 LTS SP4": click_openeuler_22_03_lts_sp4,
    "openEuler 22.03 LTS SP4场景筛选": openeuler_22_03_lts_sp4_scene_filter,
    "点击技术白皮书": click_technical_white_paper,
    "点击24.03 LTS安装指南": click_24_03_lts_installation_guide,
    "点击24.09安装指南": click_24_09_installation_guide,
    "点击版本生命周期": click_version_lifecycle,
    "点击查询历史版本": click_query_history_version,
    "点击商业发行版": click_commercial_release,
    "点击软件中心": click_software_center,
    "点击Repo源": click_repo_source,

    # 导航-学习
    "选择导航-学习": navigation_study,
    "点击文档中心": click_document_center,
    "点击热门文档": click_hot_documents,
    "点击开发教程": click_development_tutorials,
    "点击流程规范": click_process_standards,
    "点击工具查询": click_tool_query,
    "点击24.03LTS文档": click_24_03_lts_documents,
    "点击安装升级": click_installation_upgrade,
    "点击文档撰写指南": click_document_writing_guide,
    "点击Man Pages": click_man_pages,
    "点击课程中心": click_course_center,
    "点击开始学习": click_start_learning,
    "点击报名考试": click_apply_for_exam,
    "点击openEuler精品课程": click_openeuler_best_courses,
    "点击Tutorials": click_tutorials,
    "点击openEuler直播": click_openeuler_live,
    "点击从入门到精通-openEuler操作系统迁移专题": click_migrate_openeuler_os,
    "进入迁移专区": enter_migration_center,
    "进入运维专区": enter_operation_center,
    "点击迁移工具x2openEuler": click_x2openeuler_migration_tool,
    "点击迁移实践": click_migration_practice,
    "进入用户案例": enter_user_case,
    "进入白皮书": enter_white_paper,
    "进入市场研究报告": enter_market_research_report,

    # 导航-开发
    "选择导航-开发": navigation_develop,
    "进入EulerPublisher": enter_euler_publisher,
    "进入EulerMaker": enter_euler_maker,
    "进入Compass-CI": enter_compass_ci,
    "进入用户软件仓": enter_user_software_warehouse,
    "进入软件包贡献": enter_software_package_contribution,
    "进入License工具门户": enter_license_tool_portal,
    "进入EulerTest": enter_euler_test,
    "进入EulerLauncher": enter_euler_launcher,
    "进入OEPKGS": enter_oepkgs,
    "进入oecp": enter_oecp,
    "进入Pkgship": enter_pkgship,
    "进入QuickIssue": enter_quick_issue,

    # 导航-支持
    "选择导航-支持": navigation_support,
    "进入兼容性列表": enter_compatibility_list,
    "进入兼容性技术测评": enter_compatibility_tech_assessment,
    "点击openEuler 硬件兼容性测试整体介绍": click_openeuler_hardware_compatibility_test_intro,
    "进入x2openEuler": enter_x2openeuler,
    "进入OSV技术测评": enter_osv_tech_assessment,
    "进入安全中心": enter_security_center,
    "进入缺陷中心": enter_defect_center,
    "进入FAQ常见问题": enter_faq_common_questions,
    "进入OSV技术测评整体介绍": enter_osv_tech_assessment_intro,

    # 导航-社区
    "选择导航-社区": navigation_community,
    "进入组织架构": enter_organization_structure,
    "进入社区章程": enter_community_charter,
    "进入成员单位": enter_member_units,
    "进入社区荣誉": enter_community_honor,
    "进入oEEP": enter_oeep,
    "进入城市用户组": enter_city_user_group,
    "进入贡献看板": enter_contribution_board,
    "进入openEuler社区介绍PDF": enter_openeuler_community_intro_pdf,
    "进入SIG中心": enter_sig_center,
    "进入贡献攻略": enter_contribution_strategy,
    "进入CLA签署": enter_cla_sign,
    "进入高校": enter_high_schools,
    "进入人才培养": enter_talent_recruitment,
    "进入开源实习": enter_open_internship,
    "进入企业签署CLA流程": enter_enterprise_cla_process,
    "进入CLA-FAQ": enter_cla_faq,
    "进入开发者日历": enter_developer_calendar,
    "进入活动与大赛": enter_activities_competitions,
    "进入高校技术小组": enter_high_school_technical_group,
    "进入A-Tune": enter_a_tune,
    "进入iSula": enter_isula,
    "进入StratoVirt": enter_stratovirt,
    "进入BiSheng JDK": enter_bisheng_jdk,
    "进入secGear": enter_secgear,
    "进入NestOS": enter_nestos,
    "进入论坛": enter_forum,
    "进入邮件列表": enter_mail_list,
    "进入线上会议": enter_online_meeting,
    "进入联系我们": enter_contact_us,

    # 导航-动态
    "选择导航-动态": navigation_dynamic,
    "进入活动日历": enter_activity_calendar,
    "进入峰会": enter_summit,
    "进入openEuler Call for X计划": enter_openeuler_call_for_x_plan,
    "操作系统大会 & openEuler Summit 2024": operation_system_conference_openeuler_summit_2024,
    "openEuler SIG Gathering 2024": openeuler_sig_gathering_2024,
    "进入新闻": click_news,
    "进入博客": click_blog,
    "进入月刊": click_monthly,
    "openEuler 2023 社区年报": openeuler_2023_community_annual_report,

    # 首页
    "新手指引": new_guide,
    "跳过新手指引": skip_new_guide,
    "切换首页banner": change_home_banner,
    "进入技术白皮书": enter_technical_white_paper,
    "进入首页安全中心": enter_security_center_home,
    "进入首页迁移专区": enter_migration_center_home,
    "进入首页活动专区": enter_summits_home,
    "点击支持多样性设备": click_support_diversity_devices,
    "点击覆盖全场景应用": click_cover_all_scene_applications,
    "点击完整开发工具链": click_complete_development_toolchain,
    "点击首页获取openEuler": click_get_openeuler_home,
    "点击首页贡献攻略": click_contribution_strategy_home,
    "点击首页进入SIG中心": click_sig_center_home,
    "点击首页成员单位": click_member_units_home,
    "点击首页查看捐赠权益": click_view_donation_benefits_home,
    "点击主页用户案例": click_user_cases,
    "查看更多": more_user_cases,
    "点击查看贡献详情": click_contribution_details,
    "断言社区活力有数据": assert_community_dynamic_data,
    "首页断言博客数据": assert_blog_data_and_more,
    "首页查看更多博客": home_more_blog,
    "首页断言新闻数据": assert_news_data_and_more,
    "首页查看更多新闻": home_more_news,
    "日历类型切换": calendar_type_switch,
    "切换月份": switch_month,
    "会议详情收起与展开": meeting_details_collapse_expand,
    "悬浮窗进入社区论坛": suspended_window_enter_forum,
    "悬浮窗进入QuickIssue": suspended_window_enter_quick_issue,
    "悬浮窗进入FAQs": suspended_window_enter_faqs,
    "悬浮窗反馈": suspended_window_feedback,

    # 页脚
    "进入页脚成员单位": enter_footer_member_units,
    "进入页脚组织架构": enter_footer_organization_structure,
    "进入页脚社区章程": enter_footer_community_charter,
    "进入页脚贡献看板": enter_footer_contribution_board,
    "进入页脚社区介绍": enter_footer_community_intro,
    "进入页脚新闻": enter_footer_news,
    "进入页脚博客": enter_footer_blog,
    "进入页脚白皮书": enter_footer_white_paper,
    "进入页脚获取openEuler操作系统": enter_footer_get_openeuler_os,
    "进入页脚最新社区发行版": enter_footer_latest_community_release,
    "进入页脚商业发行版": enter_footer_commercial_release,
    "进入页脚软件中心": enter_footer_software_center,
    "进入页脚文档": enter_footer_document,
    "进入页脚FAQ": enter_footer_faq,
    "进入页脚联系我们": enter_footer_contact_us,
    "进入页脚邮件列表": enter_footer_mail_list,
    "进入页脚活动": enter_footer_activities,
    "进入页脚论坛": enter_footer_forum,
    "进入页脚SIG中心": enter_footer_sig_center,
    "进入页脚贡献攻略": enter_footer_contribution_strategy,
    "进入页脚课程中心": enter_footer_course_center,
    "开放原子开源基金会": openatom_foundation,
    "品牌": brand,
    "隐私政策": privacy_policy,
    "法律声明": law_declaration,
    "关于cookies": about_cookies,
    "友情链接": friend,

}

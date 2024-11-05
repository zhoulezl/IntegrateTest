import re
import traceback

from playwright import sync_api
from playwright.sync_api import expect


# 账号服务
def open_url(page: sync_api.Page):
    """
    进入生产环境
    """
    page.goto('https://www.openeuler.org/zh/')
    page.wait_for_timeout(2000)
    return page


def open_url_test(page: sync_api.Page):
    """
        进入测试环境
    """
    page.goto('https://openeuler.test.osinfra.cn/zh/')
    page.wait_for_timeout(1000)
    return page


def longin(page: sync_api.Page, arglist: list):
    """ 登录 """
    page.locator(".login > .o-icon > svg").click()
    page.wait_for_timeout(2000)
    page.get_by_placeholder("请输入您的手机号/用户名/邮箱地址").fill(arglist[0])
    page.get_by_placeholder("请输入您的密码").fill(arglist[1])
    page.get_by_role("button", name="登录").click()
    page.wait_for_timeout(2000)
    page.hover('.user-img')
    expect(page.get_by_text("退出登录")).to_be_visible()
    print("登录成功")
    return page


def longin_and_sign_privacy_statement(page: sync_api.Page, arglist: list):
    """ 登录并签署隐私声明 """
    page.wait_for_timeout(1000)
    page.locator(".login > .o-icon > svg").click()
    page.wait_for_timeout(2000)
    page.get_by_placeholder("请输入您的手机号/用户名/邮箱地址").fill(arglist[0])
    page.get_by_placeholder("请输入您的密码").fill(arglist[1])
    page.get_by_role("button", name="登录").click()
    page.wait_for_timeout(2000)
    page.locator("label span").first.click()
    page.get_by_role("button", name="确认").click()
    page.wait_for_timeout(2000)
    page.hover('.img[class*="img"]')
    page.wait_for_timeout(1000)
    expect(page.get_by_text("退出登录")).to_be_visible()
    print("登录并签署隐私声明成功")
    return page


def logout(page: sync_api.Page):
    """ 退出登录 """
    page.locator('img[class*="img"]').first.hover()
    page.get_by_text("退出登录").click()
    page.wait_for_timeout(2000)
    expect(page.locator(".login > .o-icon > svg")).to_be_visible()
    print("退出登录成功")
    page.wait_for_timeout(1000)
    return page


# 首页操作
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


def enter_success_tories(page: sync_api.Page):
    """ 进入案例中心 """
    with page.expect_popup() as page_info:
        page.get_by_role("heading", name="案例中心").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("heading", name="用户案例")).to_be_visible()
    print("进入案例中心成功")
    page1.close()
    return page


def enter_migration_center(page: sync_api.Page):
    """ 进入迁移专区 """
    with page.expect_popup() as page_info:
        page.get_by_role("heading", name="迁移专区").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_text("迁移专区", exact=True)).to_be_visible()
    print("进入迁移专区成功")
    page1.close()
    return page


def enter_openeuler_forum(page: sync_api.Page):
    """ 进入社区论坛 """
    with page.expect_popup() as page_info:
        page.get_by_role("heading", name="社区论坛").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("link", name="话题")).to_be_visible()
    print("进入社区论坛成功")
    page1.close()
    return page


def enter_summits(page: sync_api.Page):
    """ 进入活动专区 """
    with page.expect_popup() as page_info:
        page.get_by_role("heading", name="活动专区").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("heading", name="活动")).to_be_visible()
    print("进入活动专区成功")
    page1.close()
    return page


def suspended_window_feedback(page: sync_api.Page, arglist: list):
    """ 悬浮窗反馈 """
    page.locator("#app div").filter(
        has_text="您向他人推荐 openEuler社区 的可能性有多大？00-不可能10-非常可能0/500 感谢您的反馈，如需帮助，可论坛发帖求助提交").nth(
        3).click()
    page.wait_for_timeout(1000)
    page.locator(f"div:nth-child(3) > div:nth-child({arglist[0]})").first.click()  # 9,8,7,6,5
    page.wait_for_timeout(1000)
    page.get_by_placeholder("改进哪些方面会让您更愿意推荐？").fill(arglist[1])
    page.get_by_role("button", name="提交").click()
    page.wait_for_timeout(1000)
    return page


# 个人中心
def enter_user_center(page: sync_api.Page):
    """ 进入个人中心 """
    page.hover('.user-img')
    with page.expect_popup() as page1_info:
        page.get_by_text("个人中心").click()
    page1 = page1_info.value
    # expect(page1.get_by_text("用户名称")).to_be_visible()
    # page.close()
    print("进入个人中心成功")
    return page1


def change_user_avatar(page: sync_api.Page, arglist: list):
    """ 个人中心更换头像 """
    old_img_src = page.locator("//img[@class='img']").get_attribute("src")
    print(old_img_src)
    page.wait_for_timeout(1000)
    page.locator("//input[@type='file']").set_input_files(f"{arglist[0]}")
    page.wait_for_timeout(2000)
    new_img_src = page.locator("//img[@class='img']").get_attribute("src")
    print(new_img_src)
    assert old_img_src != new_img_src, "更换头像失败"
    print("更换头像成功")
    page.wait_for_timeout(1000)
    page.close()
    all_page = page.context.pages

    return all_page[0]


def change_nickname(page: sync_api.Page, arglist: list):
    """修改昵称"""
    page.get_by_placeholder("请输入你的昵称").fill("")
    page.get_by_placeholder("请输入你的昵称").fill(arglist[0])
    page.get_by_role("button", name="保存").click()
    expect(page.get_by_placeholder("请输入你的昵称")).to_have_value(arglist[0])
    print("昵称修改成功")
    return page


def change_company(page: sync_api.Page, arglist: list):
    """修改公司"""
    page.get_by_placeholder("请输入你的公司").fill("")
    page.get_by_placeholder("请输入你的公司").fill(arglist[0])
    page.get_by_role("button", name="保存").click()
    expect(page.get_by_placeholder("请输入你的公司")).to_have_value(arglist[0])
    print("公司修改成功")
    page.wait_for_timeout(1000)
    page.close()
    all_page = page.context.pages
    return all_page[0]


def cancel_signature(page: sync_api.Page):
    """取消签署"""
    page.get_by_text("账号安全").click()
    page.get_by_role("button", name="取消签署").click()
    page.locator(".el-input__inner").fill("delete")
    page.get_by_role("button", name="确认").click()
    expect(page.get_by_text("请先 登录 !")).to_be_visible()
    print("取消签署成功")
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
    print("进入消息中心成功")
    return page1


def change_gitee_message(page: sync_api.Page):
    """ 选择Gitee消息 """
    page.locator("li").filter(has_text="Gitee消息").click()
    page.wait_for_timeout(1000)
    return page


def message_to_read(page: sync_api.Page):
    """ 标为已读 """
    page.locator(".list-item-left > .o-checkbox > .o-checkbox-wrap > .o-checkbox-input-wrap").first.click()
    page.get_by_text("已读 标记已读").click()
    page.wait_for_timeout(1000)
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
    page.get_by_role("textbox").first.click()
    page.get_by_text(arglist[0]).click()
    page.wait_for_timeout(1000)
    return page


def message_page_change(page: sync_api.Page, arglist: list):
    """ 切换消息分页 """
    page.locator("div").filter(has_text=re.compile(r"^前往$")).locator("div").first.click()
    page.locator("div").filter(has_text=re.compile(r"^前往$")).get_by_label("").fill(arglist[0])
    page.locator("div").filter(has_text=re.compile(r"^前往$")).get_by_label("").press("Enter")
    page.wait_for_timeout(1000)
    return page


# 导航-用户
def hover_home_user(page: sync_api.Page):
    """ 鼠标悬浮用户 """
    page.locator(".nav-item").first.hover()
    page.wait_for_timeout(1000)
    return page


def click_user_case(page: sync_api.Page):
    """ 点击用户案例 """
    page.get_by_role("navigation").get_by_text("用户案例").click()
    expect(page.get_by_role("heading", name="用户案例")).to_be_visible()
    print("进入用户案例成功")
    page.wait_for_timeout(1000)
    return page


def click_tech_white_paper(page: sync_api.Page):
    """ 点击技术白皮书 """
    page.get_by_text("技术白皮书").click()
    expect(page.get_by_role("heading", name="技术白皮书")).to_be_visible()
    print("进入技术白皮书成功")
    page.wait_for_timeout(1000)
    return page


def click_industry_white_paper(page: sync_api.Page):
    """ 点击行业白皮书 """
    page.get_by_text("行业白皮书").click()
    expect(page.get_by_role("heading", name="行业白皮书")).to_be_visible()
    print("进入行业白皮书成功")
    page.wait_for_timeout(1000)
    return page


def click_market_report(page: sync_api.Page):
    """ 点击市场研究报告 """
    page.get_by_text("市场研究报告").click()
    expect(page.get_by_role("heading", name="市场研究报告")).to_be_visible()
    print("进入市场研究报告成功")
    page.wait_for_timeout(1000)
    return page


def click_document(page: sync_api.Page, arglist: list):
    """ 点击文档 """
    if arglist[0] == "开发者":
        with page.expect_popup() as page_info:
            page.get_by_text("文档").nth(2).click()
        page1 = page_info.value
        expect(page1.locator("#left img")).to_be_visible()
        print("进入文档成功")
        page1.wait_for_timeout(2000)
        page1.close()
        return page
    elif arglist[0] == "用户":
        with page.expect_popup() as page_info:
            page.get_by_text('文档').first.click()
        page1 = page_info.value
        expect(page1.locator("#left img")).to_be_visible()
        print("进入文档成功")
        page1.wait_for_timeout(2000)
        page1.close()
        return page


def click_man_pages(page: sync_api.Page):
    """ 点击Man Pages """
    with page.expect_popup() as page_info:
        page.get_by_text("Man Pages").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="Man Pages")).to_be_visible()
    print("进入Man Pages成功")
    page1.wait_for_timeout(2000)
    page1.close()
    return page


def click_course_center(page: sync_api.Page, arglist: list):
    """ 点击课程中心 """
    if arglist[0] == "开发者":
        page.get_by_text("课程中心").nth(1).click()
        page.wait_for_timeout(1000)
        expect(page.get_by_role("heading", name="课程中心")).to_be_visible()
        print("进入课程中心成功")
        page.wait_for_timeout(1000)
        return page
    elif arglist[0] == "用户":
        page.get_by_text("课程中心").first.click()
        page.wait_for_timeout(1000)
        expect(page.get_by_role("heading", name="课程中心")).to_be_visible()
        print("进入课程中心成功")
        page.wait_for_timeout(1000)
        return page


def click_migration_center(page: sync_api.Page):
    """ 点击迁移中心 """
    page.get_by_text("迁移中心").click()
    page.wait_for_timeout(1000)
    expect(page.get_by_text("迁移专区", exact=True)).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入迁移中心成功")
    return page


def click_operation_center(page: sync_api.Page):
    """ 点击运维专区 """
    page.get_by_text("运维专区").click()
    expect(page.get_by_role("heading", name="运维专区")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入运维专区成功")
    return page


# 导航-用户-支持与服务
def click_software_center(page: sync_api.Page):
    """ 点击软件中心 """
    with page.expect_popup() as page_info:
        page.get_by_text("软件中心").click()
    page1 = page_info.value
    page1.wait_for_timeout(2000)
    expect(page1.get_by_role("heading", name="openEuler软件中心")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入软件中心成功")
    page1.close()
    return page


def click_compatibility_test(page: sync_api.Page):
    """ 点击兼容性技术测评 """
    with page.expect_popup() as page_info:
        page.get_by_text("兼容性技术测评", exact=True).click()
    page1 = page_info.value
    expect(page1.get_by_text("openEuler兼容性测评服务")).to_be_visible()
    page1.wait_for_timeout(1000)
    print("进入兼容性技术测评成功")
    page1.close()
    return page


def click_security_center(page: sync_api.Page):
    """ 点击安全中心 """
    page.get_by_text("安全中心").click()
    expect(page.get_by_role("heading", name="安全中心")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入安全中心成功")
    return page


def click_bug_center(page: sync_api.Page):
    """ 点击缺陷中心 """
    page.get_by_text("缺陷中心").click()
    expect(page.get_by_role("heading", name="缺陷中心")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入缺陷中心成功")
    return page


def click_osv_test(page: sync_api.Page):
    """ 点击OSV技术测评 """
    page.get_by_text("OSV技术测评", exact=True).click()
    expect(page.get_by_role("heading", name="OSV技术测评列表")).to_be_visible()  # 验证页面标题
    page.wait_for_timeout(1000)
    print("进入OSV技术测评成功")
    return page


def click_compatibility_list(page: sync_api.Page):  # 点击兼容性列表
    """ 点击兼容性列表 """
    page.get_by_text("兼容性列表", exact=True).click()
    expect(page.get_by_role("heading", name="兼容性列表")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入兼容性列表成功")
    return page


# 导航-开发者
def hover_home_developer(page: sync_api.Page):
    """ 鼠标悬浮开发者 """
    page.locator(".nav-item").nth(1).hover()  # 鼠标悬浮开发者
    page.wait_for_timeout(1000)
    return page


def click_contribution_guide(page: sync_api.Page):
    """ 点击贡献攻略 """
    page.get_by_text("贡献攻略").first.click()
    expect(page.get_by_role("heading", name="贡献攻略")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入贡献攻略成功")
    return page


def click_sig_center(page: sync_api.Page):
    """ 点击SIG中心 """
    page.get_by_text("SIG中心").first.click()
    expect(page.get_by_role("heading", name="SIG中心")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入SIG中心成功")
    return page  # 点击SIG中心


def click_openeuler_intern(page: sync_api.Page):
    """ 点击开源实习 """
    page.get_by_text("开源实习").click()
    expect(page.get_by_role("heading", name="openEuler开源实习")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入开源实习成功")
    return page  # 点击开源实习


def click_cla_sign(page: sync_api.Page):
    """ 点击CLA签署 """
    with page.expect_popup() as page_info:
        page.get_by_text("CLA签署").click()
    page1 = page_info.value
    expect(page1.get_by_role("button", name="Sign Corporate CLA")).to_be_visible()
    page.wait_for_timeout(2000)
    print("进入CLA签署成功")
    page1.close()
    return page  # 点击CLA签署


def click_quick_issue(page: sync_api.Page):
    """ 点击QuickIssue """
    with page.expect_popup() as page_info:
        page.get_by_role("list").get_by_text("QuickIssue").click()
    page1 = page_info.value
    expect(page1.get_by_text("ISSUE", exact=True)).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入QuickIssue成功")
    page1.close()
    return page  # 点击QuickIssue


def click_software_package_contribution(page: sync_api.Page):
    """ 点击软件包贡献 """
    with page.expect_popup() as page_info:
        page.get_by_text("软件包贡献").click()
    page1 = page_info.value
    expect(page1.get_by_text("贡献软件包").first).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入软件包贡献成功")
    page1.close()
    return page  # 点击软件包贡献


def click_euler_test(page: sync_api.Page):
    """ 点击EulerTest """
    with page.expect_popup() as page_info:
        page.get_by_text("EulerTest").click()
    page1 = page_info.value
    expect(page1.get_by_text("radiaTest")).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入EulerTest成功")
    page1.close()
    return page  # 点击EulerTest


def click_compass_ci(page: sync_api.Page):
    """ 点击Compass-CI """
    with page.expect_popup() as page_info:
        page.get_by_text("Compass-CI").click()
    page1 = page_info.value
    expect(page1.get_by_text("Compass CI", exact=True)).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入Compass-CI成功")
    page1.close()
    return page


def click_euler_maker(page: sync_api.Page):
    """ 点击EulerMaker """
    with page.expect_popup() as page_info:
        page.get_by_text("EulerMaker").click()
    page1 = page_info.value
    expect(page1.get_by_text("EulerMaker", exact=True)).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入EulerMaker成功")
    page1.close()
    return page  # 点击EulerMaker


def click_pkgship(page: sync_api.Page):
    """ 点击Pkgship """
    with page.expect_popup() as page_info:
        page.get_by_text("Pkgship").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="Packages in the palm of your")).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入Pkgship成功")
    page1.close()
    return page  # 点击Pkgship


def click_license_tool_portal(page: sync_api.Page):
    """ 点击License工具门户 """
    with page.expect_popup() as page_info:
        page.get_by_text("License工具门户").click()
    page1 = page_info.value
    expect(page1.get_by_text("貂蝉 License Show Room")).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入License工具门户成功")
    page1.close()
    return page  # 点击License工具门户


def click_x2openeuler(page: sync_api.Page):
    """ 点击x2openEuler """
    with page.expect_popup() as page_info:
        page.get_by_text("x2openEuler").click()
    page1 = page_info.value
    expect(page1.get_by_role("img", name="logo")).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入x2openEuler成功")
    page1.close()
    return page  # 点击x2openEuler


def click_oepkgs(page: sync_api.Page):
    """ 点击OEPKGS """
    with page.expect_popup() as page_info:
        page.get_by_text("OEPKGS", exact=True).click()
    page1 = page_info.value
    expect(page1.get_by_role("img", name="logo-176-")).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入OEPKGS成功")
    page1.close()
    return page  # 点击OEPKGS


def click_oecp(page: sync_api.Page):
    """ 点击oecp """
    with page.expect_popup() as page_info:
        page.get_by_text("oecp").click()
    page1 = page_info.value
    expect(page1.get_by_text("openEuler/oecp", exact=True)).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入oecp成功")
    page1.close()
    return page  # 点击oecp


def click_euler_launcher(page: sync_api.Page):
    """ 点击EulerLauncher """
    with page.expect_popup() as page_info:
        page.get_by_text("EulerLauncher").click()
    page1 = page_info.value
    expect(page1.get_by_text("openEuler/eulerlauncher", exact=True)).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入EulerLauncher成功")
    page1.close()
    return page  # 点击EulerLauncher


def click_user_software_warehouse(page: sync_api.Page):
    """ 点击用户软件仓 """
    with page.expect_popup() as page_info:
        page.get_by_text("用户软件仓(EUR)").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="openEuler Copr hosts")).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入用户软件仓成功")
    page1.close()
    return page  # 点击用户软件仓


def click_code_warehouse(page: sync_api.Page):
    """ 点击代码仓 """
    with page.expect_popup() as page_info:
        page.get_by_text("代码仓", exact=True).click()
    page1 = page_info.value
    expect(page1.get_by_role("link", name="openEuler", exact=True)).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入代码仓成功")
    page1.close()
    return page  # 点击代码仓


def click_software_package_warehouse(page: sync_api.Page):
    """ 点击软件包仓 """
    with page.expect_popup() as page_info:
        page.get_by_text("软件包仓").click()
    page1 = page_info.value
    expect(page1.get_by_role("link", name="src-openEuler", exact=True)).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入软件包仓成功")
    page1.close()
    return page  # 点击软件包仓


def click_github_mirror_warehouse(page: sync_api.Page):
    """ 点击Github镜像仓 """
    with page.expect_popup() as page_info:
        page.get_by_text("Github镜像仓").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="openEuler")).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入Github镜像仓成功")
    page1.close()
    return page  # 点击Github镜像仓


# 导航-社区
def click_organization_structure(page: sync_api.Page):
    """ 点击组织架构 """
    page.get_by_text("组织架构").click()
    expect(page.get_by_text("组织架构")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入组织架构成功")
    return page  # 点击组织架构


def click_community_charter(page: sync_api.Page):
    """ 点击社区章程 """
    page.get_by_role("navigation").get_by_text("社区章程").click()
    expect(page.get_by_text("政策和规则")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入社区章程成功")
    return page  # 点击社区章程


def click_oeep(page: sync_api.Page):
    """ 点击oEEP """
    page.get_by_text("oEEP").click()
    expect(page.get_by_role("heading", name="oEEP 类型分类：")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入oEEP成功")
    return page  # 点击oEEP


def click_city_user_group(page: sync_api.Page):
    """ 点击城市用户组 """
    page.get_by_text("城市用户组").click()
    expect(page.get_by_role("heading", name="openEuler 用户组")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入城市用户组成功")
    return page  # 点击城市用户组


def click_member_units(page: sync_api.Page):
    """ 点击成员单位 """
    page.get_by_text("成员单位").click()
    expect(page.get_by_text("成员单位")).to_be_visible()
    page.wait_for_timeout(2000)
    print("进入成员单位成功")
    return page  # 点击成员单位


def click_community_honor(page: sync_api.Page):
    """ 点击社区荣誉 """
    page.get_by_text("社区荣誉").click()
    expect(page.get_by_role("heading", name="社区荣誉")).to_be_visible()
    page.wait_for_timeout(2000)
    print("进入社区荣誉成功")
    return page  # 点击社区荣誉


def click_openeuler_call_for_x_plan(page: sync_api.Page):
    """ 点击openEuler Call for X 计划 """
    page.get_by_text("openEuler Call for X 计划", exact=True).click()
    expect(page.get_by_role("heading", name="openEuler Call for X 计划")).to_be_visible()
    page.wait_for_timeout(2000)
    print("进入openEuler Call for X 计划成功")
    return page  # 点击openEuler Call for X 计划


def click_contribution_board(page: sync_api.Page):
    """ 点击贡献看板 """
    with page.expect_popup() as page_info:
        page.get_by_text("贡献看板").click()
    page1 = page_info.value
    expect(page1.get_by_role("img", name="logo")).to_be_visible()
    page1.wait_for_timeout(2000)
    print("进入贡献看板成功")
    page1.close()
    return page  # 点击贡献看板


# 定义字典
def_dict = {
    # 进入环境
    '进入生产环境': open_url,
    '进入测试环境': open_url_test,
    "登录": longin,
    "登录并签署隐私声明": longin_and_sign_privacy_statement,
    "退出登录": logout,

    # 主页
    "切换首页banner": change_home_banner,
    "进入案例中心": enter_success_tories,
    "进入迁移专区": enter_migration_center,
    "进入社区论坛": enter_openeuler_forum,
    "进入活动专区": enter_summits,
    "悬浮窗反馈": suspended_window_feedback,

    # 个人中心
    "进入个人中心": enter_user_center,
    "更换头像": change_user_avatar,
    "修改昵称": change_nickname,
    "修改公司": change_company,
    "取消签署协议": cancel_signature,

    # 消息中心
    "进入消息中心": enter_messag2_center,
    "选择Gitee消息": change_gitee_message,
    "消息标为已读": message_to_read,
    "删除消息": delete_message,
    "消息分页": message_pagesize,
    "消息切页": message_page_change,

    # 导航-用户
    "鼠标悬浮用户": hover_home_user,
    "点击用户案例": click_user_case,
    "点击技术白皮书": click_tech_white_paper,
    "点击行业白皮书": click_industry_white_paper,
    "点击市场研究报告": click_market_report,
    "点击文档": click_document,
    "点击Man Pages": click_man_pages,
    "点击课程中心": click_course_center,
    "点击迁移中心": click_migration_center,
    "点击运维专区": click_operation_center,
    # 导航用-用户-支持与服务
    "点击软件中心": click_software_center,
    "点击兼容性技术测评": click_compatibility_test,
    "点击安全中心": click_security_center,
    "点击缺陷中心": click_bug_center,
    "点击OSV技术测评": click_osv_test,
    "点击兼容性列表": click_compatibility_list,

    # 导航-开发者
    "鼠标悬浮开发者": hover_home_developer,
    "点击贡献攻略": click_contribution_guide,
    "点击SIG中心": click_sig_center,
    "点击开源实习": click_openeuler_intern,
    "点击CLA签署": click_cla_sign,
    "点击QuickIssue": click_quick_issue,
    "点击软件包贡献": click_software_package_contribution,
    "点击EulerTest": click_euler_test,
    "点击Compass-CI": click_compass_ci,
    "点击EulerMaker": click_euler_maker,
    "点击Pkgship": click_pkgship,
    "点击License工具门户": click_license_tool_portal,
    "点击x2openEuler": click_x2openeuler,
    "点击OEPKGS": click_oepkgs,
    "点击oecp": click_oecp,
    "点击EulerLauncher": click_euler_launcher,
    "点击用户软件仓": click_user_software_warehouse,
    "点击代码仓": click_code_warehouse,
    "点击软件包仓": click_software_package_warehouse,
    "点击Github镜像仓": click_github_mirror_warehouse,

    # 导航-社区
    "点击组织架构": click_organization_structure,
    "点击社区章程": click_community_charter,
    "点击oEEP": click_oeep,
    "点击城市用户组": click_city_user_group,
    "点击成员单位": click_member_units,
    "点击社区荣誉": click_community_honor,
    "点击openEuler Call for X 计划": click_openeuler_call_for_x_plan,
    "点击贡献看板": click_contribution_board,

}

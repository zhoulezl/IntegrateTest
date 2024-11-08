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
    page.wait_for_timeout(1000)
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
    page.get_by_role("button", name="全部接受").click()
    page.wait_for_timeout(1000)
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


def click_support_diversity_devices(page: sync_api.Page):
    """ 点击支持多样化设备 """
    page.get_by_text("支持多样性设备").first.click()
    expect(page.locator("div").filter(has_text=re.compile(
        r"^支持多样性设备覆盖全场景应用完整开发工具链 立即体验支持多样性设备覆盖全场景应用完整开发工具链$")).get_by_role(
        "img").first).to_be_visible()
    print("断言支持多样化设备成功")
    page.wait_for_timeout(1000)
    return page


def click_cover_all_scene_applications(page: sync_api.Page):
    """ 点击覆盖全场景应用 """
    page.get_by_text("覆盖全场景应用").first.click()
    expect(page.locator("div").filter(has_text=re.compile(
        r"^支持多样性设备覆盖全场景应用完整开发工具链 立即体验支持多样性设备覆盖全场景应用完整开发工具链$")).get_by_role(
        "img").first).to_be_visible()
    print("断言覆盖全场景应用成功")
    page.wait_for_timeout(1000)
    return page


def click_complete_development_toolchain(page: sync_api.Page):
    """ 点击完整开发工具链 """
    page.get_by_text("完整开发工具链").first.click()
    expect(page.locator("div").filter(has_text=re.compile(
        r"^支持多样性设备覆盖全场景应用完整开发工具链 立即体验支持多样性设备覆盖全场景应用完整开发工具链$")).get_by_role(
        "img").first).to_be_visible()
    print("断言完整开发工具链成功")
    page.wait_for_timeout(1000)
    return page


def click_try_now(page: sync_api.Page):
    """ 立即体验 """
    with page.expect_popup() as page_info:
        page.get_by_role("button", name="立即体验").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="贡献攻略")).to_be_visible()
    print("点击立即体验成功")
    page.wait_for_timeout(1000)
    page1.close()
    return page


def click_user_cases(page: sync_api.Page, arglist: list):
    """ 点击用户案例 """
    if arglist[0] == "金融":
        page.locator(".case-word").first.click()
        expect(page.get_by_role("link", name="三湘银行 基于麒麟信安打造银行IT信息化系统安全底座")).to_be_visible()
        expect(page.get_by_role("link", name="天弘基金 以服务器操作系统配合完成邮件与OA的改造")).to_be_visible()
        expect(page.get_by_role("link", name="中国建设银行 分布式信用卡核心业务系统，单日交易量超过 1")).to_be_visible()
        expect(page.get_by_role("link", name="兴业银行 某核心业务系统国产化改造项目")).to_be_visible()
        page.wait_for_timeout(1000)
        print("断言金融用户案例成功")
        return page
    elif arglist[0] == "运营商":
        page.locator(".case-word").nth(1).click()
        expect(page.get_by_role("link", name="天翼云科技有限公司")).to_be_visible()
        expect(page.locator(".user-card").nth(26)).to_be_visible()
        expect(page.get_by_role("link", name="中国联通")).to_be_visible()
        expect(page.get_by_role("link", name="联通系统集成公司")).to_be_visible()
        # page.wait_for_timeout(2000)
        print("断言运营商用户案例成功")
        return page
    elif arglist[0] == "能源":
        page.locator(".case-word").nth(2).click()
        expect(page.get_by_role("link",
                                name="国家电网 “国家电网河北智慧标杆站” 智慧工地系统，平滑完成操作系统创新，实现业务高效稳定运行")).to_be_visible()
        expect(page.get_by_role("link", name="全面基于国内主流安全操作系统进行大规模建设")).to_be_visible()
        expect(page.get_by_role("link", name="国家电网 智能调度系统 D5000")).to_be_visible()
        expect(page.get_by_role("link", name="南京瀚元科技有限公司 A-OPS")).to_be_visible()
        page.wait_for_timeout(1000)
        print("断言能源用户案例成功")
        return page
    elif arglist[0] == "物流":
        page.locator(".case-word").nth(3).click()
        expect(page.get_by_role("link", name="中国邮政 OA 业务系统迁移改造")).to_be_visible()
        page.wait_for_timeout(1000)
        print("断言物流用户案例成功")
        return page
    elif arglist[0] == "高校&科研":
        page.locator(".case-word").nth(4).click()
        expect(page.get_by_role("link", name="华中科技大学/武汉理工大学 基于openEuler")).to_be_visible()
        expect(page.get_by_role("link", name="上海交通大学 交大“交我算”计算集群：共建")).to_be_visible()
        expect(page.get_by_role("link", name="兰州大学 openEuler + 鲲鹏全栈实现HPC性能倍增")).to_be_visible()
        expect(page.get_by_role("link",
                                name="南京信息工程大学 极端高温干旱天气模拟与预测平台，有效及时发现预警极端气候，提升应急处置能力，性能提升58%")).to_be_visible()
        page.wait_for_timeout(1000)
        print("断言高校&科研用户案例成功")
        return page
    elif arglist[0] == "云计算":
        page.locator(".case-word").nth(5).click()
        expect(page.get_by_role("link", name="中国电信 中国电信天翼云基于 openEuler 打造")).to_be_visible()
        expect(page.get_by_role("link", name="中国移动云能力中心 基于openEuler")).to_be_visible()
        expect(page.get_by_role("link",
                                name="云宏信息科技股份有限公司 同比例虚拟机计算性能翻倍，金融行业上云效率提高")).to_be_visible()
        expect(page.get_by_role("link", name="深信服科技股份有限公司 基于openEuler")).to_be_visible()
        # page.wait_for_timeout(2000)
        print("断言云计算用户案例成功")
        return page
    elif arglist[0] == "其他":
        page.locator(".case-word").nth(6).click()
        expect(page.get_by_role("link", name="确保网络环境的安全和高效运行")).to_be_visible()
        expect(page.get_by_role("link",
                                name="四川中电启明星技术有限公司 性能卓越，稳定可靠，环境级高可用， 智能运维，安全性，自主可控，可移植、易操作")).to_be_visible()
        expect(page.get_by_role("link", name="科来网络技术股份有限公司 基于openEuler")).to_be_visible()
        expect(page.get_by_role("link", name="新华社 新华社科技创新应用项目共筑 AI")).to_be_visible()
        page.wait_for_timeout(1000)
        print("断言其他用户案例成功")
        return page


def more_user_cases(page: sync_api.Page):
    """ 点击查看更多案例 """
    with page.expect_popup() as page_info:
        page.get_by_role("button", name="查看更多").first.click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="用户案例")).to_be_visible()
    print("点击查看更多案例成功")
    page.wait_for_timeout(1000)
    page1.close()
    return page


def click_contribution_details(page: sync_api.Page):
    """ 点击查看贡献详情 """
    with page.expect_popup() as page_info:
        page.get_by_role("button", name="查看贡献详情").click()
    page1 = page_info.value
    expect(page1.get_by_role("img", name="logo")).to_be_visible()
    page.wait_for_timeout(1000)
    print("点击贡献攻略成功")
    page1.close()
    return page


def assert_community_dynamic_data(page: sync_api.Page):
    """ 断言社区动态数据 """
    assert page.locator(".round-value").first.inner_text() is not None, "社区动态数据不存在"
    assert page.locator(".round-value").nth(1).inner_text() is not None, "社区动态数据不存在"
    assert page.locator(".round-value").nth(2).inner_text() is not None, "社区动态数据不存在"
    assert page.locator(".round-value").nth(3).inner_text() is not None, "社区动态数据不存在"
    assert page.locator(".round-value").nth(4).inner_text() is not None, "社区动态数据不存在"
    page.wait_for_timeout(1000)
    print("断言社区动态数据成功")
    return page


def home_view_more_blog(page: sync_api.Page):
    """ 点击查看更多博客 """
    with page.expect_popup() as page_info:
        page.get_by_role("button", name="查看更多").nth(1).click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="博客", exact=True)).to_be_visible()
    page.wait_for_timeout(1000)
    print("点击查看更多博客成功")
    page1.close()
    return page


def assert_home_blog_data(page: sync_api.Page):
    """ 断言首页博客数据 """
    # print(page.locator(".room-item-right").first.text_content())
    # page.wait_for_timeout(10000)
    assert page.locator(".room-item-right").first.text_content() is not None, "首页博客数据不存在"
    assert page.locator(".room-item-right").nth(1).text_content() is not None, "首页博客数据不存在"
    assert page.locator(".room-item-right").nth(2).text_content() is not None, "首页博客数据不存在"
    assert page.locator(".room-item-right").nth(3).text_content() is not None, "首页博客数据不存在"
    page.wait_for_timeout(1000)
    print("断言首页博客数据成功")
    return page


def home_view_more_news(page: sync_api.Page):
    """ 点击查看更多新闻 """
    page.get_by_role("tab", name="新闻").click()
    page.wait_for_timeout(1000)
    with page.expect_popup() as page_info:
        page.get_by_role("button", name="查看更多").nth(1).click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="新闻")).to_be_visible()
    page.wait_for_timeout(1000)
    print("点击查看更多新闻成功")
    page1.close()
    return page


def assert_home_news_data(page: sync_api.Page):
    """ 断言首页新闻数据 """
    assert page.locator(".room-item-right").nth(4).text_content() is not None, "首页新闻数据不存在"
    assert page.locator(".room-item-right").nth(5).text_content() is not None, "首页新闻数据不存在"
    assert page.locator(".room-item-right").nth(6).text_content() is not None, "首页新闻数据不存在"
    assert page.locator(".room-item-right").nth(7).text_content() is not None, "首页新闻数据不存在"
    page.wait_for_timeout(1000)
    print("断言首页新闻数据成功")
    return page


def calendar_type_switch(page: sync_api.Page):
    """ 日历类型切换 """
    page.wait_for_timeout(1000)
    page.locator("#tab-all").click()
    page.wait_for_timeout(1000)
    page.locator("#tab-meetings").click()
    page.wait_for_timeout(1000)
    page.locator("#tab-activity").click()
    page.wait_for_timeout(1000)
    page.locator("#tab-summit").click()
    page.wait_for_timeout(1000)
    page.locator("#tab-all").click()
    return page


def switch_month(page: sync_api.Page):
    """ 切换月份 """
    page.wait_for_timeout(1000)
    old_month = page.locator(".month-date").inner_text()
    page.locator("#meeting").get_by_role("img").nth(1).click()
    new_month = page.locator(".month-date").inner_text()
    assert old_month != new_month, "切换月份失败"
    print("切换月份成功")
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
    print("会议详情收起/展开成功")
    return page


def suspended_window_enter_forum(page: sync_api.Page):
    """ 悬浮穿窗口进入论坛 """
    page.wait_for_timeout(1000)
    page.locator(".nav-box1 > div:nth-child(2) > span > svg").hover()
    page.locator(".nav-box1 > div:nth-child(2) > span > svg").hover()
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="社区论坛").click()
    page1 = page_info.value
    expect(page1.get_by_role("link", name="openEuler 论坛")).to_be_visible()
    page1.wait_for_timeout(1000)
    print("悬浮穿窗口进入论坛成功")
    page1.close()
    return page


def suspended_window_enter_quick_issue(page: sync_api.Page):
    """ 悬浮穿窗口进入快速发布问题 """
    page.wait_for_timeout(1000)
    page.locator(".nav-box1 > div:nth-child(2) > span > svg").hover()
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="QuickIssue").click()
    page1 = page_info.value
    expect(page1.locator("div").filter(has_text=re.compile(r"^ISSUEPR API 中文 提交 Issue$")).locator(
        "img").first).to_be_visible()
    print("悬浮穿窗口进入快速发布问题成功")
    page.wait_for_timeout(1000)
    page1.close()
    return page


def suspended_window_enter_faqs(page: sync_api.Page):
    """ 悬浮穿窗口进入常见问题 """
    page.wait_for_timeout(1000)
    page.locator(".nav-box1 > div:nth-child(2) > span > svg").hover()
    with page.expect_popup() as page_info:
        page.get_by_role("link", name="FAQs").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="openEuler常见问题")).to_be_visible()
    print("悬浮穿窗口进入常见问题成功")
    page.wait_for_timeout(1000)
    page1.close()
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
    elif arglist[0] == "社区":
        with page.expect_popup() as page_info:
            page.get_by_text("文档").nth(3).click()
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
    elif arglist[0] == "社区":
        page.get_by_text("课程中心").nth(2).click()
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


def click_contribution_guide(page: sync_api.Page, arglist: list):
    """ 点击贡献攻略 """
    if arglist[0] == "社区":
        page.get_by_text("贡献攻略").nth(1).click()
        expect(page.get_by_role("heading", name="贡献攻略")).to_be_visible()
        page.wait_for_timeout(1000)
        print("进入贡献攻略成功")
        return page
    elif arglist[0] == "开发者":
        page.get_by_text("贡献攻略").first.click()
        expect(page.get_by_role("heading", name="贡献攻略")).to_be_visible()
        page.wait_for_timeout(1000)
        print("进入贡献攻略成功")
        return page


def click_sig_center(page: sync_api.Page, arglist: list):
    """ 点击SIG中心 """
    if arglist[0] == "开发者":
        page.get_by_text("SIG中心").first.click()
        expect(page.get_by_role("heading", name="SIG中心")).to_be_visible()
        page.wait_for_timeout(1000)
        print("进入SIG中心成功")
        return page  # 点击SIG中心
    elif arglist[0] == "社区":
        page.get_by_text("SIG中心").nth(1).click()
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
    page1.wait_for_timeout(1000)
    print("进入EulerMaker成功")
    page1.wait_for_timeout(1000)
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

def hover_home_community(page: sync_api.Page):
    """ 鼠标悬浮社区 """
    page.locator(".nav-item").nth(2).hover()  # 鼠标悬浮社区
    page.wait_for_timeout(1000)
    return page


def click_organization_structure(page: sync_api.Page):
    """ 点击组织架构 """
    page.get_by_role("navigation").get_by_text("组织架构").click()
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


def click_university(page: sync_api.Page):
    """ 点击高校 """
    page.get_by_text("高校", exact=True).click()
    expect(page.get_by_role("heading", name="高校", exact=True)).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入高校成功")
    return page  # 点击高校


def click_recruitment_assessment(page: sync_api.Page):
    """ 点击人才评定 """
    with page.expect_popup() as page_info:
        page.get_by_text("人才评定").click()
    page1 = page_info.value
    expect(page1.get_by_text("人才能力评定", exact=True)).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入人才评定成功")
    page1.close()
    return page  # 点击人才评定


def click_a_tune(page: sync_api.Page):
    """ 点击A-Tune """
    page.get_by_role("navigation").get_by_text("A-Tune").click()
    expect(page.get_by_role("heading", name="A-Tune")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入A-Tune成功")
    return page  # 点击A-Tune


def click_isula(page: sync_api.Page):
    """ 点击iSula """
    page.get_by_text("iSula").click()
    expect(page.get_by_role("heading", name="iSula")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入iSula成功")
    return page  # 点击iSula


def click_strato_virt(page: sync_api.Page):
    """ 点击StratoVirt """
    page.get_by_text("StratoVirt").click()
    expect(page.get_by_role("heading", name="StratoVirt")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入StratoVirt成功")
    return page  # 点击StratoVirt


def click_bisheng_jdk(page: sync_api.Page):
    """ 点击BiSheng JDK """
    page.get_by_text("BiSheng JDK").click()
    expect(page.get_by_role("heading", name="毕昇JDK")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入BiSheng JDK成功")
    return page  # 点击BiSheng JDK


def click_secgear(page: sync_api.Page):
    """ 点击secGear """
    page.get_by_text("secGear").click()
    expect(page.get_by_role("heading", name="secGear")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入secGear成功")
    return page  # 点击secGear


def click_nestos(page: sync_api.Page):
    """ 点击NestOS """
    with page.expect_popup() as page_info:
        page.get_by_text("NestOS").click()
    page1 = page_info.value
    expect(page1.get_by_role("heading", name="NestOS")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入NestOS成功")
    page1.close()
    return page  # 点击NestOS


# 导航-下载

def hover_home_download(page: sync_api.Page):
    """ 鼠标悬浮下载 """
    page.locator(".nav-item").nth(3).hover()  # 鼠标悬浮下载
    page.wait_for_timeout(1000)
    return page


def click_get_openeuler_os(page: sync_api.Page):
    """ 点击获取openEuler操作系统 """
    page.get_by_text("获取openEuler操作系统").click()
    expect(page.get_by_role("heading", name="获取openEuler操作系统")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入获取openEuler操作系统成功")
    return page  # 点击获取openEuler操作系统


def click_openeuler_24_03_lts(page: sync_api.Page):
    """ 点击openEuler 24.03 LTS """
    page.get_by_text("openEuler 24.03 LTS", exact=True).click()
    expect(page.get_by_role("heading", name="下载", exact=True)).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入openEuler 24.03 LTS成功")
    return page  # 点击openEuler 24.03 LTS


def click_openeuler_24_09(page: sync_api.Page):
    """ 点击openEuler 24.09 """
    page.get_by_role("list").get_by_text("openEuler 24.09", exact=True).click()
    expect(page.get_by_role("heading", name="下载", exact=True)).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入openEuler 24.09成功")
    return page  # 点击openEuler 24.09


def click_community_release(page: sync_api.Page):
    """ 点击社区发行版 """
    page.get_by_role("list").get_by_text("社区发行版").click()
    expect(page.get_by_role("link", name="历史版本下载")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入社区发行版成功")
    return page  # 点击社区发行版


def click_commercial_release(page: sync_api.Page):
    """ 点击商业发行版 """
    page.get_by_text("商业发行版").click()
    expect(page.get_by_role("tab", name="商业发行版")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入商业发行版成功")
    return page  # 点击商业发行版


def click_mirror_warehouse_list(page: sync_api.Page):
    """ 点击镜像仓列表 """
    page.get_by_text("镜像仓列表").click()
    expect(page.get_by_role("heading", name="镜像仓列表")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入镜像仓列表成功")
    return page  # 点击镜像仓列表


# 首页动态

def click_news(page: sync_api.Page):
    """ 点击新闻 """
    page.get_by_text("新闻").first.click()
    expect(page.get_by_role("heading", name="新闻")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入新闻成功")
    return page  # 点击新闻


def click_blog(page: sync_api.Page):
    """ 点击博客 """
    page.get_by_text("博客").first.click()
    expect(page.get_by_role("heading", name="博客", exact=True)).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入博客成功")
    return page  # 点击博客


def click_activity(page: sync_api.Page):
    """ 点击活动 """
    page.get_by_text("活动").first.click()
    expect(page.get_by_role("heading", name="活动")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入活动成功")
    return page  # 点击活动


def click_summit(page: sync_api.Page):
    """ 点击峰会 """
    page.get_by_text("峰会").first.click()
    expect(page.get_by_role("heading", name="活动日程")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入峰会成功")
    return page  # 点击峰会


def click_monthly(page: sync_api.Page):
    """ 点击月刊 """
    page.get_by_text("月刊").first.click()
    expect(page.get_by_role("heading", name="月刊")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入月刊成功")
    return page  # 点击月刊


def click_openeuler_forum(page: sync_api.Page):
    """ 点击论坛 """
    with page.expect_popup() as page_info:
        page.get_by_text("论坛").first.click()
    page1 = page_info.value
    expect(page1.get_by_role("link", name="openEuler 论坛")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入论坛成功")
    page1.close()
    return page  # 点击论坛


def click_mail_list(page: sync_api.Page):
    """ 点击邮件列表 """
    page.get_by_text("邮件列表").first.click()
    expect(page.get_by_role("heading", name="邮件列表")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入邮件列表成功")
    return page  # 点击邮件列表


def click_online_meeting(page: sync_api.Page):
    """ 点击线上会议 """
    page.get_by_text("线上会议").first.click()
    expect(page.get_by_role("heading", name="线上会议")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入线上会议成功")
    return page  # 点击线上会议


def click_social_media(page: sync_api.Page):
    """ 点击社交媒体 """
    page.get_by_text("社交媒体").first.click()
    expect(page.get_by_role("heading", name="友情链接")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入社交媒体成功")
    return page  # 点击社交媒体


# 页脚
def openatom_foundation(page: sync_api.Page):
    """ 点击开放原子开源基金会 """
    with page.expect_popup() as page_info:
        page.locator(".atom > a").click()
    page1 = page_info.value
    expect(page1.get_by_role("link", name="LOGO")).to_be_visible()
    page.wait_for_timeout(1000)
    page1.close()
    print("进入开放原子开源基金会成功")
    return page  # 点击开放原子开源基金会


def brand(page: sync_api.Page):
    """ 点击品牌 """
    page.get_by_role("button", name="全部接受").click()
    page.get_by_role("link", name="品牌").click()
    expect(page.get_by_role("heading", name="品牌")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入品牌成功")
    return page  # 点击品牌


def privacy_policy(page: sync_api.Page):
    """ 点击隐私政策 """
    page.get_by_role("link", name="隐私政策").click()
    expect(page.get_by_role("heading", name="隐私政策")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入隐私政策成功")
    return page  # 点击隐私政策


def law_declaration(page: sync_api.Page):
    """ 点击法律声明 """
    page.get_by_role("link", name="法律声明").click()
    expect(page.get_by_role("heading", name="法律声明")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入法律声明成功")
    return page  # 点击法律声明


def about_cookies(page: sync_api.Page):
    """ 点击关于cookies """
    page.get_by_role("link", name="关于cookies").click()
    expect(page.get_by_role("heading", name="关于 COOKIES")).to_be_visible()
    page.wait_for_timeout(1000)
    print("进入关于cookies成功")
    return page  # 点击关于cookies


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
    "点击支持多样性设备": click_support_diversity_devices,
    "点击覆盖全场景应用": click_cover_all_scene_applications,
    "点击完整开发工具链": click_complete_development_toolchain,
    "点击立即体验": click_try_now,
    "点击主页用户案例": click_user_cases,
    "更多用户案例": more_user_cases,
    "点击查看贡献详情": click_contribution_details,
    "断言社区动态有数据": assert_community_dynamic_data,
    "主页查看更多博客": home_view_more_blog,
    "断言主页博客有数据": assert_home_blog_data,
    "主页查看更多新闻": home_view_more_news,
    "断言主页新闻有数据": assert_home_news_data,
    "日历类型切换": calendar_type_switch,
    "切换月份": switch_month,
    "会议详情收起与展开": meeting_details_collapse_expand,
    "悬浮窗进入社区论坛": suspended_window_enter_forum,
    "悬浮窗进入QuickIssue": suspended_window_enter_quick_issue,
    "悬浮窗进入FAQs": suspended_window_enter_faqs,

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
    "鼠标悬浮社区": hover_home_community,
    "点击组织架构": click_organization_structure,
    "点击社区章程": click_community_charter,
    "点击oEEP": click_oeep,
    "点击城市用户组": click_city_user_group,
    "点击成员单位": click_member_units,
    "点击社区荣誉": click_community_honor,
    "点击openEuler Call for X 计划": click_openeuler_call_for_x_plan,
    "点击贡献看板": click_contribution_board,
    "点击高校": click_university,
    "点击人才评定": click_recruitment_assessment,
    "点击A-Tune": click_a_tune,
    "点击iSula": click_isula,
    "点击StratoVirt": click_strato_virt,
    "点击BiSheng JDK": click_bisheng_jdk,
    "点击secGear": click_secgear,
    "点击NestOS": click_nestos,

    # 导航-下载
    "鼠标悬浮下载": hover_home_download,
    "点击获取openEuler操作系统": click_get_openeuler_os,
    "点击openEuler 24.03 LTS": click_openeuler_24_03_lts,
    "点击openEuler 24.09": click_openeuler_24_09,
    "点击社区发行版": click_community_release,
    "点击商业发行版": click_commercial_release,
    "点击镜像仓列表": click_mirror_warehouse_list,

    # 首页动态
    "点击新闻": click_news,
    "点击博客": click_blog,
    "点击活动": click_activity,
    "点击峰会": click_summit,
    "点击月刊": click_monthly,
    "点击论坛": click_openeuler_forum,
    "点击邮件列表": click_mail_list,
    "点击线上会议": click_online_meeting,
    "点击社交媒体": click_social_media,

    # 页脚
    "开放原子开源基金会": openatom_foundation,
    "品牌": brand,
    "隐私政策": privacy_policy,
    "法律声明": law_declaration,
    "关于cookies": about_cookies,

}

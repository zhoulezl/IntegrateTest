import re
from playwright import sync_api
from playwright.sync_api import expect


def open_url(page: sync_api.Page):
    """
    进入生产环境
    """
    page.goto('https://easysoftware.openeuler.org/zh/')
    return page


def open_url_test(page: sync_api.Page):
    """
        进入测试环境
    """
    page.goto('https://easysoftware.test.osinfra.cn/zh')
    return page


def home_search(page: sync_api.Page, arglist: list):
    """
        在主页进行搜索，arglist包含两个部分：
            标签：
                全部，按名称，按概要，按文件，ubuntu
            内容：
                要搜索的内容
    """
    page.locator('#e2e_headerNav_home').click()
    page.locator('.o-select.o-select-normal.o-select-text.o-select-large').click()
    page.locator('.o-option').get_by_text(arglist[0]).click()
    page.get_by_placeholder('输入内容进行搜索，多个关键字请用逗号隔开').fill(arglist[1])
    page.keyboard.press('Enter')
    page.wait_for_timeout(2000)  # 等待查询结果返回，暂定2秒
    expect(page.locator('.text').get_by_text(' 为您找到'))
    expect(page.locator('.total').get_by_text(' 个与 '))
    expect(page.locator('.search-value').get_by_text('匹配的搜索结果 '))
    return page


def home_search_not_found(page: sync_api.Page, arglist: list):
    """
        在主页进行搜索，arglist包含两个部分：
            标签：
                全部，按名称，按概要，按文件，ubuntu
            内容：
                要搜索的内容
    """
    page.locator('#e2e_headerNav_home').click()
    page.locator('.o-select.o-select-normal.o-select-text.o-select-large').click()
    page.locator('.o-option').get_by_text(arglist[0]).click()
    page.get_by_placeholder('输入内容进行搜索，多个关键字请用逗号隔开').fill(arglist[1])
    page.keyboard.press('Enter')
    page.wait_for_timeout(2000)  # 等待查询结果返回，暂定2秒
    expect(page.locator('.text').get_by_text(' 为您找到'))
    expect(page.locator('.total').get_by_text('0'))
    expect(page.locator('.search-value').get_by_text('匹配的搜索结果 '))
    return page


def home_learn_more(page: sync_api.Page, arglist: list):
    """
        在主页点击了解更多，arglist包含1个部分：
            内容：
                要了解更多的类别名称
    """
    page.locator('#e2e_headerNav_home').click()
    list_a = ['云服务', '数据库', 'AI', '大数据', 'HPC', '分布式存储', '其他']
    if arglist[0] == '云服务':
        page.locator(".o-link").first.click()
    else:
        i = list_a.index(arglist[0])
        page.locator(f"div:nth-child({i + 2}) > .domain-item-title > .o-link").click()
        page.wait_for_timeout(2000)
    expect(page.locator('.o-tag-label').get_by_text(arglist[0]))
    return page


def home_get_resource(page: sync_api.Page, arglist: list):
    """
        在主页点击获取资源，arglist包含1个部分：
            内容：
                要获取资源的类别名称
    """
    # page.set_viewport_size({'width': 1792, 'height': 1008})
    page.locator('#e2e_headerNav_home').click()
    page.wait_for_timeout(1000)
    # page.locator('.o-anchor-item-link').get_by_text('获取资源').click()
    # page.wait_for_timeout(1000)
    page.locator('.title').get_by_text(arglist[0]).click()
    page.wait_for_timeout(2000)
    expect(page.locator('.banner-title').get_by_text(arglist[0]))
    return page


def home_get_solution(page: sync_api.Page, arglist: list):
    """
        在主页点击解决方案，arglist包含1个部分：
            内容：
                要获取解决方案的类别名称
    """
    page.locator('#e2e_headerNav_home').click()
    page.wait_for_timeout(1000)
    page.locator('.o-card-title').get_by_text(arglist[0]).click()
    page.wait_for_timeout(2000)

    expect(page.locator('.solution-title').get_by_text('方案概述'))
    return page


def home_download(page: sync_api.Page, arglist: list):
    with page.expect_event('popup') as expectation:
        page.get_by_role("row", name=f"{arglist[0]}").get_by_role("link").click()
        
    page1 = expectation.value
    str1 = arglist[0].replace("-", " ")
    # page.close()
    expect(page1.get_by_role("heading", name=str1))
    page.wait_for_timeout(2000)
    page1.close()
    return page


def home_choose_app(page: sync_api.Page, arglist: list):
    """
        在主页选择软件包的版本查看详情
        list：社区版本，软件包分类，架构
        ！！！这个需要特别注意的是，每个用例在执行的时候，这个操作最多只能有两次
        如果有2次的话，那第一次必须是操作的第一个才行，否则就只能用一次
    """
    list_1 = ['领域应用', 'RPM', '应用镜像', 'OEPKG']
    page.locator('#e2e_headerNav_home').click()
    if arglist[0] == 'openEuler-24.03-LTS':
        # page.locator("a").filter(has_text=re.compile(r"^noarch(?:\(\d+\))?$")).first.click()
        page.locator('a').filter(has_text=re.compile(rf"^{arglist[2]}(?:\(\d+\))?$")).nth(
            list_1.index(arglist[1])).click()
    else:
        page.wait_for_timeout(2000)
        # 收起默认打开的第一个
        page.get_by_role("row", name="openEuler-24.03-LTS").get_by_role("img").click()
        page.wait_for_timeout(2000)
        # 展开需要展开的
        page.get_by_role("row", name=f"{arglist[0]}").get_by_role("img").click()
        # 定位到所在行
        locator = page.locator('.el-table__row').filter(has_text=arglist[1])
        locator.locator('a').filter(has_text=re.compile(rf"^{arglist[2]}(?:\(\d+\))?$")).click()
        # 断言传入的第三个参数是存在的（第一个判断不了，因为点完了以后，第一个标签会变）
        expect(page.locator('.o-tag-label').filter(has_text=arglist[2]))
    page.wait_for_timeout(2000)
    return page


def home_feedback(page: sync_api.Page, arglist: list):
    page.locator('.global-feedback-btn').click()
    page.locator('.o-rate-item').nth(int(arglist[0]) - 1).hover()
    page.locator('.o-rate-item').nth(int(arglist[0]) - 1).click()
    page.get_by_placeholder('请输入您的反馈').fill(arglist[1])
    page.get_by_role('button', name='提交反馈').click()
    return page


def home_login(page: sync_api.Page, arglist: list):
    page.locator('.o-icon.login-btn').click()
    page.get_by_placeholder('请输入您的手机号/用户名/邮箱地址').fill(arglist[0])
    page.get_by_placeholder('请输入您的密码').fill(arglist[1])
    page.get_by_role('button', name='登录').click()
    page.wait_for_timeout(4000)
    return page


# 协作平台 collaboration platform
def CP_enter(page: sync_api.Page):
    page.wait_for_timeout(2000)
    with page.expect_event('popup') as expectation:
        page.locator('.o-link-label').get_by_text('协作平台').click()
    page1 = expectation.value
    return page1


def CP_feedback(page: sync_api.Page, arglist: list):
    locator1 = page.locator('.el-table__row').filter(has_text=arglist[0])
    locator1.locator('.cell').get_by_text('反馈').click()

    page.locator("span").filter(has_text="CVE状态").click()
    page.locator("form input[type=\"text\"]").click()
    page.wait_for_timeout(2000)
    page.get_by_text("有CVE部分修复").nth(1).click()
    page.get_by_placeholder('请输入您的理由').click()
    page.get_by_placeholder('请输入您的理由').clear()
    page.get_by_placeholder('请输入您的理由').fill(arglist[1])
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="提交反馈").click()
    page.wait_for_timeout(2000)
    return page


def CP_feedback_history(page: sync_api.Page, arglist: list):
    locator1 = page.locator('.el-table__row').filter(has_text=arglist[0])
    locator1.locator('.cell').get_by_text('历史').click()
    return page


def CP_wait_center(page: sync_api.Page):
    page.locator("a").filter(has_text="待办中心").click()
    page.wait_for_timeout(2000)
    return page


def CP_revoke_application(page: sync_api.Page, arglist: list):
    page.get_by_text("我的申请").click()
    page.get_by_role("row").filter(has_text=arglist[0]).first.locator("a").get_by_text('撤销申请').click()
    page.get_by_role("button", name="确认").click()
    return page


def CP_approve_pass(page: sync_api.Page, arglist: list):
    page.get_by_role("row").filter(has_text=arglist[0]).first.locator("a").click()
    page.get_by_placeholder("请输入审批意见").fill(arglist[1])
    page.get_by_role("button", name="通过").click()
    return page


def CP_approve_not_pass(page: sync_api.Page, arglist: list):
    page.get_by_role("row").filter(has_text=arglist[0]).first.locator("a").click()
    page.get_by_placeholder("请输入审批意见").fill(arglist[1])
    page.get_by_role("button", name="驳回").click()
    return page


def CP_application_detail(page: sync_api.Page, arglist: list):
    page.get_by_text("我的申请").click()
    page.get_by_role("row").filter(has_text=arglist[0]).locator("a").first.click()
    page.wait_for_timeout(2000)
    return page


def CP_approve_detail(page: sync_api.Page):
    page.get_by_text("我审批过的").click()
    page.get_by_role("row", name="ranger CVE状态 有CVE").locator("a").click()
    page.wait_for_timeout(2000)
    return page


def CP_appstore(page: sync_api.Page, arglist: list):
    page.get_by_text("软件仓库").click()
    page.get_by_text(arglist[0]).click()
    page.locator("a").filter(has_text="确定").first.click()
    page.wait_for_timeout(2000)
    page.get_by_role("cell", name="软件仓库").get_by_role("img").click()
    page.locator("a").filter(has_text="重置").first.click()
    page.wait_for_timeout(2000)
    return page


def CP_wait_center_choose(page: sync_api.Page, arglist: list):
    page.get_by_text("我的申请").click()
    page.locator('.o-svg-icon.o-icon-filter.type-fill').first.click()
    page.locator("span").filter(has_text=arglist[0]).click()
    page.wait_for_timeout(2000)
    page.locator("a").filter(has_text="确定").first.click()
    page.wait_for_timeout(2000)
    page.locator('.o-svg-icon.o-icon-filter.type-fill').first.click()
    page.locator("a").filter(has_text="重置").first.click()
    page.wait_for_timeout(2000)
    return page


# 领域应用
def field_enter(page: sync_api.Page):
    """
        进入领域应用页面
    """
    page.locator("#e2e_headerNav_field").get_by_text("领域应用").click()
    page.wait_for_timeout(2000)
    return page


def field_choose(page: sync_api.Page, arglist: list):
    page.locator("a").filter(has_text="显示全部").first.click()
    page.wait_for_timeout(2000)
    page.locator("a").filter(has_text="显示全部").click()
    page.locator("span").filter(has_text=re.compile(rf"^{arglist[0]}$")).click()
    page.locator("span").filter(has_text=re.compile(rf"^{arglist[1]}$")).click()
    list_a = arglist[2].split('|')
    for tip in list_a:
        page.locator("span").filter(has_text=re.compile(rf"^{tip}$")).click()
    expect(page.locator('.o-tag-label').filter(has_text=arglist[0]))
    expect(page.locator('.o-tag-label').filter(has_text=arglist[1]))
    page.wait_for_timeout(2000)
    return page


def field_search(page: sync_api.Page, arglist: list):
    page.get_by_placeholder('请输入领域应用相关信息').fill(arglist[0])
    page.keyboard.press('Enter')
    return page


def field_sort(page: sync_api.Page, arglist: list):
    page.locator("a").filter(has_text=arglist[0]).click()
    page.wait_for_timeout(2000)
    return page


def field_pagesize(page: sync_api.Page, arglist: list):
    page.locator(".el-input__wrapper").first.click()
    page.locator("li").filter(has_text=arglist[0]).click()
    page.wait_for_timeout(2000)
    return page


def field_page_change(page: sync_api.Page, arglist: list):
    page.get_by_label("页", exact=True).clear()
    page.get_by_label("页", exact=True).fill(arglist[0])
    page.wait_for_timeout(2000)
    # page.get_by_label("页", exact=True).press("Enter")
    page.keyboard.press('Enter')
    page.wait_for_timeout(5000)
    return page


def field_search_result_detail(page: sync_api.Page, arglist: list):
    page.wait_for_timeout(2000)
    with page.expect_event('popup') as expectation:
        page.get_by_role("link", name=arglist[0]).first.click()
    page1 = expectation.value
    page.close()
    # app_binary_download(page)
    return page1


# app
# 这里由于弹出页面了，所以下载做在了详情页面里
def app_binary_download(page: sync_api.Page):
    page.get_by_role("button", name="二进制包下载").click()

    with page.expect_download() as download_info:
        page.get_by_role("button", name="继续前往").click()
    download = download_info.value
    download.save_as('download/' + download.suggested_filename)
    return page


def app_image_copy(page: sync_api.Page):
    page.locator("div:nth-child(3) > .o-icon").click()
    return page


def app_feedback(page: sync_api.Page, arglist: list):
    page.locator(".o-rate-item").nth(int(arglist[0]) - 1).hover()
    page.locator(".o-rate-item").nth(int(arglist[0]) - 1).click()

    page.get_by_placeholder("请输入您的反馈").fill(arglist[1])

    if arglist[2] == '快速反馈':
        page.get_by_role("button", name="快速反馈").click()
    elif arglist[2] == '提交issue':
        page.get_by_role("button", name="提交issue").click()
        with page.expect_popup() as page_new_info:
            page.get_by_role("button", name="继续前往").click()
            page.wait_for_timeout(2000)
        page_new_info.value.close()
    return page


# RPM
def RPM_enter(page: sync_api.Page):
    page.locator("#e2e_headerNav_rpm").get_by_text("RPM").click()
    page.wait_for_timeout(2000)
    return page


def RPM_choose(page: sync_api.Page, arglist: list):
    page.locator("a").filter(has_text="显示全部").first.click()
    page.wait_for_timeout(2000)
    page.locator("a").filter(has_text="显示全部").first.click()
    page.wait_for_timeout(2000)
    page.locator("a").filter(has_text="显示全部").first.click()
    page.locator("span").filter(has_text=re.compile(rf"^{arglist[0]}$")).click()
    page.locator("span").filter(has_text=re.compile(rf"^{arglist[1]}$")).click()
    list_a = arglist[2].split('|')
    for tip in list_a:
        page.locator("span").filter(has_text=re.compile(rf"^{tip}$")).click()
    expect(page.locator('.o-tag-label').filter(has_text=arglist[0]))
    expect(page.locator('.o-tag-label').filter(has_text=arglist[1]))
    page.wait_for_timeout(2000)
    return page


def RPM_search(page: sync_api.Page, arglist: list):
    page.get_by_placeholder('请输入RPM相关信息').fill(arglist[0])
    page.keyboard.press('Enter')
    return page


def RPM_sort(page: sync_api.Page, arglist: list):
    page.locator("a").filter(has_text=arglist[0]).click()
    page.wait_for_timeout(2000)
    return page


def RPM_pagesize(page: sync_api.Page, arglist: list):
    page.locator(".el-input__wrapper").first.click()
    page.locator("li").filter(has_text=arglist[0]).click()
    page.wait_for_timeout(2000)
    return page


def RPM_page_change(page: sync_api.Page, arglist: list):
    page.get_by_label("页", exact=True).clear()
    page.get_by_label("页", exact=True).fill(arglist[0])
    page.get_by_label("页", exact=True).press("Enter")
    return page


def RPM_search_result_detail(page: sync_api.Page, arglist: list):
    page.wait_for_timeout(2000)
    with page.expect_event('popup') as expectation:
        page.get_by_role("link", name=arglist[0]).first.click()
    page1 = expectation.value
    page.close()
    # app_binary_download(page)
    return page1


# 应用镜像
def image_enter(page: sync_api.Page):
    page.locator("#e2e_headerNav_image").get_by_text("应用镜像").click()
    page.wait_for_timeout(2000)
    return page


def image_choose(page: sync_api.Page, arglist: list):
    page.locator("a").filter(has_text="显示全部").first.click()
    page.wait_for_timeout(2000)
    page.locator("span").filter(has_text=re.compile(rf"^{arglist[0]}$")).click()
    list_a = arglist[1].split('|')
    for tip in list_a:
        page.locator("span").filter(has_text=re.compile(rf"^{tip}$")).click()
    list_a = arglist[2].split('|')
    for tip in list_a:
        page.locator("span").filter(has_text=re.compile(rf"^{tip}$")).click()
    expect(page.locator('.o-tag-label').filter(has_text=arglist[0]))
    expect(page.locator('.o-tag-label').filter(has_text=arglist[1]))
    page.wait_for_timeout(2000)
    return page


def image_search(page: sync_api.Page, arglist: list):
    page.get_by_placeholder('请输入应用镜像相关信息').fill(arglist[0])
    page.keyboard.press('Enter')
    return page


def image_sort(page: sync_api.Page, arglist: list):
    page.locator("a").filter(has_text=arglist[0]).click()
    page.wait_for_timeout(2000)
    return page


def image_pagesize(page: sync_api.Page, arglist: list):
    page.locator(".el-input__wrapper").first.click()
    page.locator("li").filter(has_text=arglist[0]).click()
    page.wait_for_timeout(2000)
    return page


def image_page_change(page: sync_api.Page, arglist: list):
    page.get_by_label("页", exact=True).clear()
    page.get_by_label("页", exact=True).fill(arglist[0])
    page.get_by_label("页", exact=True).press("Enter")
    return page


def image_search_result_detail(page: sync_api.Page, arglist: list):
    page.wait_for_timeout(2000)
    with page.expect_event('popup') as expectation:
        page.get_by_role("link", name=arglist[0]).first.click()
    page1 = expectation.value
    # app_image_copy(page)
    return page1


# OEPKG
def OEPKG_enter(page: sync_api.Page):
    page.locator("#e2e_headerNav_oepkg").get_by_text("OEPKG").click()
    page.wait_for_timeout(2000)
    return page


def OEPKG_choose(page: sync_api.Page, arglist: list):
    page.locator("a").filter(has_text="显示全部").first.click()
    page.wait_for_timeout(2000)
    page.locator("a").filter(has_text="显示全部").first.click()
    page.wait_for_timeout(2000)
    page.locator("span").filter(has_text=re.compile(rf"^{arglist[0]}$")).click()
    list_a = arglist[1].split('|')
    for tip in list_a:
        page.locator("span").filter(has_text=re.compile(rf"^{tip}$")).click()
    list_a = arglist[2].split('|')
    for tip in list_a:
        page.locator("span").filter(has_text=re.compile(rf"^{tip}$")).click()
    expect(page.locator('.o-tag-label').filter(has_text=arglist[0]))
    expect(page.locator('.o-tag-label').filter(has_text=arglist[1]))
    page.wait_for_timeout(2000)
    return page


def OEPKG_search(page: sync_api.Page, arglist: list):
    page.get_by_placeholder('请输入OEPKG相关信息').fill(arglist[0])
    page.keyboard.press('Enter')
    return page


def OEPKG_sort(page: sync_api.Page, arglist: list):
    page.locator("a").filter(has_text=arglist[0]).click()
    page.wait_for_timeout(2000)
    return page


def OEPKG_pagesize(page: sync_api.Page, arglist: list):
    page.locator(".el-input__wrapper").first.click()
    page.locator("li").filter(has_text=arglist[0]).click()
    page.wait_for_timeout(2000)
    return page


def OEPKG_page_change(page: sync_api.Page, arglist: list):
    page.get_by_label("页", exact=True).clear()
    page.get_by_label("页", exact=True).fill(arglist[0])
    page.get_by_label("页", exact=True).press("Enter")
    return page


def OEPKG_search_result_detail(page: sync_api.Page, arglist: list):
    page.wait_for_timeout(2000)
    with page.expect_event('popup') as expectation:
        page.get_by_role("link", name=arglist[0]).first.click()
    page1 = expectation.value
    page.close()
    # app_binary_download(page)
    return page1


def_dict = {
    # 进入环境
    '进入生产环境': open_url,
    '进入测试环境': open_url_test,

    # 主页
    '主页搜索': home_search,
    '主页搜索无结果': home_search_not_found,
    '主页了解更多跳转': home_learn_more,
    '主页获取资源跳转': home_get_resource,
    '主页解决方案跳转': home_get_solution,
    '主页资源下载': home_download,
    '主页选择openEuler软件包': home_choose_app,
    '主页悬浮窗反馈': home_feedback,
    '主页登录': home_login,

    # 协作平台 collaboration platform
    '进入协作平台': CP_enter,
    '协作平台反馈': CP_feedback,
    '协作平台反馈历史': CP_feedback_history,
    '进入待办中心': CP_wait_center,
    '撤销申请': CP_revoke_application,
    '审批通过': CP_approve_pass,
    '审批不通过': CP_approve_not_pass,
    '查看申请详情': CP_application_detail,
    '查看审批详情': CP_approve_detail,
    '软件仓库筛选重置': CP_appstore,
    '待办中心筛选重置': CP_wait_center_choose,

    # 领域应用
    '进入领域应用': field_enter,
    '领域应用页面选择版本架构和领域': field_choose,
    '领域应用页面搜索': field_search,
    '领域应用页面查询结果排序': field_sort,
    '领域应用页面查询结果分页': field_pagesize,
    '领域应用页面查询结果切页': field_page_change,
    '领域应用页面查询结果详情': field_search_result_detail,

    # 软件包详情
    '软件包详情页面下载': app_binary_download,
    '软件包详情页面保存': '保存是同步的在下载中的',
    '软件包详情页面复制镜像': app_image_copy,
    '软件包详情页面反馈': app_feedback,

    # RPM
    '进入RPM页面': RPM_enter,
    'RPM页面选择版本架构和领域': RPM_choose,
    'RPM页面搜索': RPM_search,
    'RPM页面查询结果排序': RPM_sort,
    'RPM页面查询结果分页': RPM_pagesize,
    'RPM页面查询结果切页': RPM_page_change,
    'RPM页面查询结果详情': RPM_search_result_detail,

    # 应用镜像
    '进入应用镜像页面': image_enter,
    '应用镜像页面选择版本架构和领域': image_choose,
    '应用镜像页面搜索': image_search,
    '应用镜像页面查询结果排序': image_sort,
    '应用镜像页面查询结果分页': image_pagesize,
    '应用镜像页面查询结果切页': image_page_change,
    '应用镜像页面查询结果详情': image_search_result_detail,

    # OEPKG
    '进入OEPKG页面': OEPKG_enter,
    'OEPKG页面选择版本架构和领域': OEPKG_choose,
    'OEPKG页面搜索': OEPKG_search,
    'OEPKG页面查询结果排序': OEPKG_sort,
    'OEPKG页面查询结果分页': OEPKG_pagesize,
    'OEPKG页面查询结果切页': OEPKG_page_change,
    'OEPKG页面查询结果详情': OEPKG_search_result_detail,

}

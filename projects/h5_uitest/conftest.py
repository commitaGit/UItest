import pytest
import os
import time
from selenium import webdriver
from py._xmlgen import html
from utils.sendmsg import sendmsg
from common.h5login import H5Login
from common.adminlogin import AdminLogin

driver = None
admin_driver = None

@pytest.fixture(scope='session', autouse=True)
def drivers(request):
    global driver
    if driver is None:
        driver = webdriver.Chrome()
        driver.maximize_window()
    def fn():
        driver.quit()
        os.system("taskkill /f /im chromedriver.exe")
    request.addfinalizer(fn)
    return driver

@pytest.fixture(scope='session', autouse=True)
def admin_drivers(request):
    global admin_driver
    if admin_driver is None:
        admin_driver = webdriver.Chrome()
        admin_driver.maximize_window()
    def fn():
        admin_driver.quit()
        os.system("taskkill /f /im chromedriver.exe")
    request.addfinalizer(fn)
    return admin_driver

@pytest.fixture(scope='session', autouse=True)
def admin_login(admin_drivers):
    AdminLogin(admin_drivers).admin_sign()

@pytest.fixture(scope='session', autouse=True)
def h5_login(drivers):
    for number in range(3):
        try:
            if H5Login(drivers).h5_login():
                return
        except:
            pass

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])

    if report.when.strip() == 'call' or report.when.strip() == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = ""
            try:
                screen_img = "data:image/png;base64,{}".format(_capture_screenshot())
            except:
                pass
            if file_name:
                html = '<div><img src="{0}" alt="screenshot" style="width:1024px;height:768px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' .format(screen_img)
                extra.append(pytest_html.extras.html(html))
        report.extra = extra

# 在测试报告表格中插入列
@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例名称'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)

# 测试通过的用例不显示日志信息
@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))

def _capture_screenshot():
    '''
    截图保存为base64
    :return:
    '''
    return driver.get_screenshot_as_base64()

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果'''
    total = terminalreporter._numcollected  # 总用例数
    passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])    # 通过用例数
    failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])    # 失败用例数
    error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])      # 错误用例数
    skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])  # 跳过用例数
    successful = len(terminalreporter.stats.get('passed', []))/terminalreporter._numcollected*100   # 通过率
    successful = "%.2f%%"%successful
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime  # 运行总时间
    duration = "%.2fs" % duration
    sendmsg().send_msg("测试用例执行结束:  \n" + \
                          "**********开始打印结果********** \n" + \
                          "总运行测试用例数:%d \n" % total + \
                          "通过测试用例数:%d \n" % passed + \
                          "跳过用例数:%d \n" % skipped + \
                          '失败的测试用例数:%d \n' % failed + \
                          "错误用例数:%d \n" % error + \
                          "通过率:%s \n" % successful + \
                          "运行总时间:%s\n" % duration)

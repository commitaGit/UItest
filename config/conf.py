import os
from time import sleep
from selenium.webdriver.common.by import By
from utils.times import dt_strftime
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy

class ConfigManager(object):
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 页面元素目录
    WEB_ELEMENT_PATH = os.path.join(BASE_DIR, r'projects/', 'web_uitest/', 'PageElements')
    APP_ELEMENT_PATH = os.path.join(BASE_DIR, r'projects/', 'app_uitest/', 'PageElements')
    H5_ELEMENT_PATH = os.path.join(BASE_DIR, r'projects/', 'h5_uitest/', 'PageElements')
    APPLET_ELEMENT_PATH = os.path.join(BASE_DIR, r'projects/', 'applet_uitest/', 'PageElements')

    # 报告路径
    WEB_REPORT_PATH = os.path.join(BASE_DIR, r'projects\web_uitest\report')
    APP_REPORT_PATH = os.path.join(BASE_DIR, r'projects\app_uitest\report')
    H5_REPORT_PATH = os.path.join(BASE_DIR, r'projects\h5_uitest\report')
    APPLET_REPORT_PATH = os.path.join(BASE_DIR, r'projects\applet_uitest\report')

    # 截图路径
    SCREEN_PATH = os.path.join(BASE_DIR, 'report/screenshot')

    # web元素定位的类型
    LOCATE_MODE = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'name': By.NAME,
        'id': By.ID,
        'class': By.CLASS_NAME,
        'tag': By.TAG_NAME
    }

    # APP元素定位的类型
    APP_LOCATE_MODE = {
        'css': MobileBy.CSS_SELECTOR,
        'xpath': MobileBy.XPATH,
        'name': MobileBy.NAME,
        'id': MobileBy.ID,
        'class': By.CLASS_NAME,
        'accessibility':MobileBy.ACCESSIBILITY_ID,
        'uiautomator':MobileBy.ANDROID_UIAUTOMATOR
    }

    # 邮件信息
    EMAIL_INFO = {
        'username': 'tcjspring@163.com',
        'password': '...',
        'smtp_host': 'smtp.163.com',
        'smtp_port': 25
    }

    # 收件人
    ADDRESSEE = [
        'tanchunjie@tehang.com',
    ]

    @property
    def log_file(self):
        """日志目录"""
        log_dir = os.path.join(self.BASE_DIR, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(dt_strftime()))

    @property
    def ini_file(self):
        """配置文件"""
        ini_file = os.path.join(self.BASE_DIR, 'config', 'config.ini')
        if not os.path.exists(ini_file):
            raise FileNotFoundError("配置文件%s不存在！" % ini_file)
        return ini_file

    DESIRED_CAPS = { "platformName" : "Android",#平台名称
                "platformVersion" : "7.1.2",#平板版本号
                "deviceName" : "127.0.0.1:62001",#设备名称
                "appPackage" : "com.tehang.TMC",#测试的包名
                "appActivity" : "com.tehang.TMC.MainActivity",#测试的包活动
                'unicodeKeyboard' : True, # 是否支持unicode的键盘。如果需要输入中文，要设置为“true”
                "noReset" : False, # true:不重新安装APP，false:重新安装app
                "newCommandTimeout" : 6000  # Appium服务器待appium客户端发送新消息的时间。默认为60秒
                }

    def get_driver(self, desired_caps=DESIRED_CAPS):
        '''获取driver'''
        try:
            self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
            sleep(5)
            return self.driver
        except Exception as e:
            raise e

cm = ConfigManager()
if __name__ == '__main__':
    print(cm.BASE_DIR)
    print(cm.APPLET_ELEMENT_PATH)
    pass
from page.webpage import WebPage
from common.readelement import Element
from utils.logger import log

adminlogin = Element('web', 'web_adminlogin')


class AdminLoginPage(WebPage):
    """后台登录类"""

    def input_account(self, content):
        """输入账号"""
        log.info("输入账号")
        self.input_text(adminlogin['账号'], txt=content)

    def input_password(self, content):
        """输入密码"""
        log.info("输入密码")
        self.input_text(adminlogin['密码'], txt=content)

    def click_login(self):
        """点击登录"""
        log.info("点击登录")
        self.js_click(adminlogin['登录按钮'])

    def find_text(self):
        """标签栏文字"""
        log.info("获取标签栏文字")
        return self.element_text(adminlogin['标签栏'])

if __name__ == "__maim__":
    pass

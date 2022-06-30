from page.webpage import WebPage
from common.readelement import Element
from utils.logger import log

customerlogin = Element('web', 'web_customerlogin')


class CustomerLoginPage(WebPage):
    """前台登录登录类"""

    def verification_login(self):
        """点击验证码登录"""
        log.info("点击验证码登录")
        self.js_click(customerlogin["验证码登录"])

    def password_login(self):
        """点击密码登录"""
        log.info("点击密码登录")
        self.js_click(customerlogin["密码登录"])

    def input_account(self, content):
        """输入账号"""
        log.info("输入账号")
        self.input_text(customerlogin['账号'], txt=content)

    def click_get_verification(self):
        """点击获取验证码"""
        log.info("点击获取验证码")
        self.js_click(customerlogin["获取验证码"])

    def input_verification_code(self, content):
        """输入验证码"""
        log.info("输入验证码")
        self.input_text(customerlogin['输入验证码'], txt=content)

    def input_password(self, password):
        """输入密码"""
        log.info("输入密码")
        self.input_text(customerlogin['密码'], password)

    def click_login(self):
        """点击登录"""
        log.info("点击登录")
        self.js_click(customerlogin['登录按钮'])

    def click_remember_account(self):
        """点击记住用户名"""
        log.info("点击记住用户名")
        self.js_click(customerlogin["记住用户名"])

    def click_join(self):
        """点击确认加入"""
        log.info("点击确认加入")
        self.js_click(customerlogin["确认加入"])

    def get_greetings(self):
        """获取问候语"""
        log.info("获取问候语")
        return self.element_text(customerlogin["问候语"])

if __name__ == "__maim__":
    pass

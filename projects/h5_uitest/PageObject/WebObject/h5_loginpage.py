from page.webpage import WebPage, sleep
from common.readelement import Element
from utils.logger import log

h5login = Element('h5', 'h5_login')


class H5LoginPage(WebPage):
    """H5登录类"""
    
    def click_skip(self):
        log.info("点击跳过")
        self.js_click(h5login["跳过"])
        self.js_click(h5login["弹框"])
        sleep(0.5)
        self.js_click(h5login["弹框"])

    def password_login(self):
        log.info("点击密码登录")
        self.js_click(h5login["账号密码登录"])

    def input_account(self, content):
        log.info("输入账号")
        eles = self.find_elements(h5login['手机号'])
        eles[0].send_keys(content)

    def input_password(self, password):
        log.info("输入密码")
        eles = self.find_elements(h5login['密码'])
        eles[1].send_keys(password)

    def click_login(self):
        log.info("点击登录")
        self.js_click(h5login['登录'])

    def click_agreement(self):
        log.info("点击已读协议")
        elems = self.find_elements(h5login["协议"])
        elems[-1].click()

    def get_greetings(self):
        log.info("判断登录是否成功")
        return self.element_exist(h5login["问候语"])

if __name__ == "__maim__":
    pass
from minium import logger
from base.basepage import BasePage
from common.readconfig import ini

ACCOUNT = ini._get("APPLETACCOUNT", "ACCOUNT")
PASSWORD = ini._get("APPLETACCOUNT", "PASSWORD")

class LoginPage(BasePage):

    def need_login(self):
        logger.info("判断是否需要登录")
        if self.mini.page.element_is_exists("button", inner_text="请先登录/注册"):
            self.mini.page.get_element("button", inner_text="请先登录/注册").click()
        if self.mini.page.element_is_exists("text", inner_text="密码登录"):
            return True

    def login(self, account=ACCOUNT, password=PASSWORD):
        logger.info("登录")
        if self.need_login():
            self.mini.page.get_element("text", inner_text="密码登录").click()
            e = self.mini.page.get_element('input[data-name="mobile"]')
            e.trigger("input", {"value": account})
            elem = self.mini.page.get_element('input[data-name="password"]')
            elem.trigger("input", {"value": password})
            self.mini.page.get_element("button[role='button']", inner_text="登录").click()
            assert self.mini.page.element_is_exists("/page/view[1]/view[2]/view[1]/view[1]/view[1]"), "没找到酒店标签"  # 能看到酒店标签则认为登录成功
        return True
from page.apppage import AppPage, sleep
from common.readelement import Element
from utils.logger import log

applogin = Element('app', 'app_login')


class AppLoginPage(AppPage):
    """APP登录类"""

    def click_skip(self):
        """点击跳过"""
        log.info("点击跳过按钮")
        eles = self.find_elements(applogin['跳过'])
        eles[0].click()
        # sleep()

    def click_agree(self):
        log.info("点击隐私政策同意按钮")
        try:
            self.is_click(applogin['同意'])
        except:
            pass

    def click_password_login(self):
        """点击账号密码登录"""
        log.info("点击账号密码登录")
        self.is_click(applogin['账号密码登录'])

    def input_account(self, content):
        """输入账号"""
        log.info("输入账号")
        eles = self.find_elements(applogin['手机号'])
        eles[0].clear()
        eles[0].send_keys(content)
        log.info("输入手机号：{}".format(content))

    def input_password(self, content):
        """输入密码"""
        log.info("输入密码")
        eles = self.find_elements(applogin['密码'])
        eles[1].clear()
        eles[1].send_keys(content)
        log.info("输入密码：{}".format(content))

    def click_agreements(self):
        """点击勾选协议"""
        log.info("点击勾选协议")
        self.is_click(applogin["协议"])

    def click_login(self):
        """点击登录"""
        log.info("点击登录")
        self.is_click(applogin['登录'])
        # sleep()

    def click_display_password(self):
        """点击显示密码"""
        log.info("点击显示密码")
        self.is_click(applogin["显示密码"])

    def click_verification_login(self):
        """点击验证码登录"""
        log.info("点击验证码登录")
        self.is_click(applogin["验证码登录"])

    def click_personal_register(self):
        """点击个人注册"""
        log.info("点击个人注册")
        self.is_click(applogin["个人注册"])
        # sleep()

    def click_gp_register(self):
        """点击公务员注册"""
        log.info("点击公务员注册")
        self.is_click(applogin["公务员注册"])
        # sleep()

    def get_label(self):
        """获取首页标签名"""
        log.info("获取首页标签名")
        return self.element_text(applogin["首页"])

    def reset_app(self):
        """重启APP"""
        log.info("重启APP")
        self.driver.reset()
        sleep(10)

if __name__ == "__maim__":
    pass

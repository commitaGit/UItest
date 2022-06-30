from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element

setpassword = Element('web', 'web_setpassword')

class SetPasswordPage(WebPage):
    """前台重置密码类"""

    def head_portrait(self):
        """点击头像"""
        log.info("点击 头像")
        sleep(0.5)
        self.is_click(setpassword["头像"])

    def account_administer(self):
        """点击账号管理"""
        log.info("点击 账号管理")
        self.is_click(setpassword["账号管理"])

    def account_password(self):
        """点击账号密码"""
        log.info("点击 账号密码")
        self.js_click(setpassword["账号密码"])

    def reset_password(self):
        """点击重置密码"""
        log.info("点击 重置密码")
        self.js_click(setpassword["重置密码"])

    def get_verification_code(self):
        """点击获取验证码"""
        log.info("点击 获取验证码")
        self.js_click(setpassword["获取验证码"])

    def input_verification_code(self, code):
        """输入验证码"""
        log.info("输入验证码：{}".format(code))
        self.input_text(setpassword["输入验证码"], code)

    def input_new_password(self, password):
        """输入新密码"""
        log.info("输入新密码：{}".format(password))
        self.input_text(setpassword["新密码"], password)

    def confirm_new_password(self, password):
        """再次输入新密码"""
        log.info("再次输入新密码：{}".format(password))
        self.input_text(setpassword["确认新密码"], password)

    def click_confirm(self):
        """点击确认"""
        log.info("点击 确认")
        self.js_click(setpassword["确认"])
        sleep(0.5)

    def click_return(self):
        """点击返回"""
        log.info("点击 返回")
        self.js_click(setpassword["返回"])

    def get_hint(self):
        """获取弹框提示语"""
        log.info("获取弹框提示语")
        return self.element_text(setpassword["提示语"])

if __name__ == "__maim__":
    pass

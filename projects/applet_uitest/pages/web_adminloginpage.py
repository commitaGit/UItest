from minium import logger
from base.web_basepage import WebPage
from common.readconfig import ini

ACCOUNT = ("xpath", "//input[@placeholder='请输入手机号或邮箱']")
PASSWORD = ("xpath", "//input[@placeholder='请输入密码']")
LOGIN_BUTTON = ("xpath", "//button[@class='width-100 ant-btn ant-btn-primary ant-btn-lg']")
TAG = ("xpath", "//layout-header//li[1]/a[1]")

class AdminLoginPage(WebPage):
    """后台登录类"""

    def input_account(self, content):
        """输入账号"""
        logger.info("输入账号")
        self.input_text(ACCOUNT, txt=content)

    def input_password(self, content):
        """输入密码"""
        logger.info("输入密码")
        self.input_text(PASSWORD, txt=content)

    def click_login(self):
        """点击登录"""
        logger.info("点击登录")
        self.js_click(LOGIN_BUTTON)

    def find_text(self):
        """标签栏文字"""
        logger.info("获取标签栏文字")
        return self.element_text(TAG)

    def admin_login(self):
        logger.info("后台登录")
        self.get_url(ini._get("HOST", "ADMIN_LOGIN_HOST"))
        self.input_account(ini._get("ADMINACCOUNT", "ACCOUNT"))
        self.input_password(ini._get("ADMINACCOUNT", "PASSWORD"))
        self.click_login()
        # 判断是否登录成功
        try:
            if self.find_text() == "呼叫接入":
                logger.info("后台账号：{0}登录成功".format(ini._get("ADMINACCOUNT", "ACCOUNT")))
                return True
        except:
            logger.error("登录失败")
            return False

    def admin_logins(self):
        for number in range(3):
            if self.admin_login():
                return True
        return False

if __name__ == "__maim__":
    from selenium import webdriver
    AdminLoginPage(webdriver.Chrome()).admin_logins()
    pass

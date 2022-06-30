from projects.web_uitest.PageObject.WebObject.web_adminloginpage import AdminLoginPage
from common.readconfig import ini
from utils.logger import log

ACCOUNT = ini._get("ADMINACCOUNT", "ACCOUNT")
PASSWORD = ini._get("ADMINACCOUNT", "PASSWORD")


class AdminLogin:

    def __init__(self, drivers, account=ACCOUNT, password=PASSWORD):
        self.url = ini._get("HOST", "ADMIN_LOGIN_HOST")
        self.driver = drivers
        self.account = account
        self.password = password

    def admin_login(self):
        """登录后台"""
        adminlogin = AdminLoginPage(self.driver)
        adminlogin.get_url(self.url)
        adminlogin.input_account(self.account)
        adminlogin.input_password(self.password)
        adminlogin.click_login()
        # 判断是否登录成功
        try:
            if adminlogin.find_text() == "呼叫接入":
                log.info("后台账号：{0}登录成功".format(self.account))
                return True
        except:
            log.error("登录失败")
            return False

    def admin_sign(self):
        for number in range(3):
            if self.admin_login():
                return True
        return False


if __name__ == "__main__":
    pass



from projects.h5_uitest.PageObject.WebObject.h5_loginpage import H5LoginPage
from common.readconfig import ini
from utils.logger import log

ACCOUNT = ini._get("H5ACCOUNT", "ACCOUNT")
PASSWORD = ini._get("H5ACCOUNT", "PASSWORD")


class H5Login:

    def __init__(self, drivers, account=ACCOUNT, password=PASSWORD):
        self.url = ini._get("HOST", "H5_LOGIN_HOST")
        self.driver = drivers
        self.account = account
        self.password = password

    def h5_login(self):
        """h5账号密码登录"""
        H5_login = H5LoginPage(self.driver)
        H5_login.get_url(self.url)
        try:
            H5_login.click_skip()
        except Exception as e:
            log.warn(e)
        H5_login.password_login()
        H5_login.input_account(self.account)
        H5_login.input_password(self.password)
        H5_login.click_agreement()
        H5_login.click_login()
        # 判断是否登录成功
        try:
            if H5_login.get_greetings():
                log.info("账号：{0}登录成功".format(self.account))
                return True
        except:
            return False

if __name__ == "__main__":
    pass



from projects.web_uitest.PageObject.WebObject.web_customerloginpage import CustomerLoginPage
from common.readconfig import ini
from utils.logger import log

ACCOUNT = ini._get("CUSTOMERACCOUNT", "ACCOUNT")
PASSWORD = ini._get("CUSTOMERACCOUNT", "PASSWORD")


class CustomerLogin:

    def __init__(self, drivers, account=ACCOUNT, password=PASSWORD):
        self.url = ini._get("HOST", "CUSTOMER_LOGIN_HOST")
        self.driver = drivers
        self.account = account
        self.password = password

    def customer_login(self):
        """前台账号密码登录"""
        customerlogin = CustomerLoginPage(self.driver)
        customerlogin.get_url(self.url)
        customerlogin.input_account(self.account)
        customerlogin.input_password(self.password)
        customerlogin.click_login()
        # 判断是否登录成功
        try:
            if "你好！"  in customerlogin.get_greetings():
                log.info("前台账号：{0}登录成功".format(self.account))
                return True
        except:
            return False


if __name__ == "__main__":
    pass



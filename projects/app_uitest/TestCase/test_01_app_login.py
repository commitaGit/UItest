import pytest
from app_uitest.PageObject.AppObject.app_loginpage import AppLoginPage
from common.readconfig import ini
from utils.excel import OperateExcel

# 前台测试账号
operate_excel = OperateExcel("register.xls", "机构注册")
ACCOUNT = operate_excel.get_row_data(1)[6]
PASSWORD = "a1111111"

class TestAppLogin:

    def login(self, APPLOGIN, account=ACCOUNT, password=PASSWORD):
        APPLOGIN.reset_app()
        APPLOGIN.click_skip()
        APPLOGIN.click_agree()
        APPLOGIN.click_password_login()
        APPLOGIN.input_account(account)
        APPLOGIN.input_password(password)
        APPLOGIN.click_agreements()
        APPLOGIN.click_login()

    @pytest.mark.dependency(depends=["set_password"], scope='session')
    def test_001(self, app_drivers):
        """APP-新注册账号登录"""
        APPLOGIN = AppLoginPage(app_drivers)
        self.login(APPLOGIN)
        assert "首页" in APPLOGIN.get_label()

    def test_002(self, app_drivers):
        """APP-测试账号登录"""
        APPLOGIN = AppLoginPage(app_drivers)
        self.login(APPLOGIN, ini._get("APPACCOUNT", "ACCOUNT"), ini._get("APPACCOUNT", "PASSWORD"))
        assert "首页" in APPLOGIN.get_label()

if __name__ == '__main__':
    pytest.main(['testcase/test_app_login.py'])
    pass
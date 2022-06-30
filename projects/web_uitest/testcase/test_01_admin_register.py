import pytest
from selenium import webdriver
from projects.web_uitest.PageObject.WebObject.web_customerloginpage import CustomerLoginPage
from projects.web_uitest.PageObject.WebObject.web_msmquerypage import SmsQueryPage
from projects.web_uitest.PageObject.WebObject.web_registerpage import RegisterPage
from projects.web_uitest.PageObject.WebObject.web_setpasswordpage import SetPasswordPage
from common.readconfig import ini
from common.adminlogin import AdminLogin
from common.customerlogin import CustomerLogin

REG_ACCOUNT = "11178546982"
PASSWORD = ini._get("CUSTOMERACCOUNT", "PASSWORD")  # 密码用同一个


class TestRegister:

    def get_veri_code(self, phone):
        """从后台短信记录中获取验证码"""
        # 浏览器后台运行
        # option=webdriver.ChromeOptions()
        # option.add_argument('headless')
        # drivers=webdriver.Chrome(chrome_options=option)
        drivers=webdriver.Chrome()
        sms = SmsQueryPage(drivers)
        AdminLogin(drivers).admin_sign()
        sms.order_processing()
        sms.information_service()
        sms.sms_query()
        verification_code = sms.get_verification_code(phone)
        drivers.quit()
        return verification_code

    def verification_code_login(self, drivers, ACCOUNT, NEW=True):
        """前台验证码登录"""
        customerlogin = CustomerLoginPage(drivers)
        customerlogin.get_url(ini._get("HOST", "CUSTOMER_LOGIN_HOST"))
        customerlogin.verification_login()
        customerlogin.input_account(ACCOUNT)
        customerlogin.click_get_verification()
        code = self.get_veri_code(ACCOUNT)
        customerlogin.input_verification_code(code)
        customerlogin.click_login()
        if NEW:  # 若有邀请链接
            customerlogin.click_join()
        # 判断是否登录成功
        try:
            return customerlogin.get_greetings()
        except:
            return "登录失败"

    def set_password(self, drivers, phone):
        """重置前台登录密码"""
        setpassword = SetPasswordPage(drivers)
        setpassword.head_portrait()
        setpassword.account_administer()
        setpassword.account_password()
        setpassword.reset_password()
        setpassword.get_verification_code()
        veri_code = self.get_veri_code(phone)
        assert veri_code, "获取验证码失败"
        setpassword.input_verification_code(veri_code)
        setpassword.input_new_password(PASSWORD)
        setpassword.confirm_new_password(PASSWORD)
        setpassword.click_confirm()
        return setpassword.get_hint()

    @pytest.mark.dependency(name="code_login")
    def test_001(self, drivers):
        """WEB-测试账号验证码登录"""
        assert "你好！" in self.verification_code_login(drivers, ini._get("CUSTOMERACCOUNT", "ACCOUNT"), NEW=False)

    @pytest.mark.dependency(name="register", depends=["code_login"])
    # @pytest.mark.skip(reason="注册产生数据")
    def test_002(self, drivers):
        """WEB-后台注册机构客户"""
        global REG_ACCOUNT
        AdminLogin(drivers).admin_sign()
        register = RegisterPage(drivers)
        register.travel_dep_add()
        register.customer_type_tmc()
        company_name = register.full_customer_name()
        register.member_id()
        register.customer_info()
        register.specific_address()
        register.service_info()
        register.contact_name()
        REG_ACCOUNT = register.contact_phone_and_mail()
        register.open_products()
        register.save_corp()
        assert register.get_corp_name()==company_name

    @pytest.mark.dependency(name="set_password", depends=["register"])
    def test_003(self, drivers):
        """WEB-注册账号前台验证码登录后重置密码"""
        assert "你好！" in self.verification_code_login(drivers, REG_ACCOUNT)
        assert "密码已重置" in self.set_password(drivers, REG_ACCOUNT)

    @pytest.mark.dependency(depends=["set_password"])
    def test_004(self, drivers):
        """WEB-注册账号前台账号密码登录"""
        assert CustomerLogin(drivers, REG_ACCOUNT, PASSWORD).customer_login(), "前台账号密码登录失败"

if __name__ == '__main__':
    pytest.main(['testcase/test_admin_register.py'])

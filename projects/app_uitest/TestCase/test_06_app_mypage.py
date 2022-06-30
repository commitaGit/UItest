import pytest
from app_uitest.PageObject.AppObject.app_mypage import AppMyPage

class TestAppMyPage:

    def test_001(self, app_drivers):
        """APP-我的订单页面校验"""
        my_page = AppMyPage(app_drivers)
        my_page.click_my_page()
        my_page.click_my_order()
        pytest.assume(my_page.check_order_list())
        my_page.click_processing()
        my_page.click_all()
        my_page.click_be_paid()
        my_page.click_wait_travel()
        my_page.click_refund_cancel()
        my_page.click_return()

    def test_002(self, app_drivers):
        """APP-常用信息页面校验"""
        my_page = AppMyPage(app_drivers)
        my_page.click_common_information()
        my_page.click_passenger()
        my_page.click_address()
        my_page.click_invoice()
        my_page.click_return()

    def test_003(self, app_drivers):
        """APP-关于我们页面校验"""
        my_page = AppMyPage(app_drivers)
        my_page.click_about_us()
        my_page.click_user_instructions()
        pytest.assume(my_page.check_user_instructions())
        my_page.click_return()
        my_page.click_service_agreement()
        pytest.assume(my_page.check_service_agreement())
        my_page.click_return()
        my_page.click_privacy_policy()
        pytest.assume(my_page.check_privacy_policy())
        my_page.click_return()
        my_page.click_return()

    def test_004(self, app_drivers):
        """APP-积分页面校验"""
        my_page = AppMyPage(app_drivers)
        my_page.click_integral()
        my_page.click_integral_rule()
        pytest.assume(my_page.check_integral_use())
        pytest.assume(my_page.check_get_integral())
        my_page.click_return()
        my_page.click_return()

    def test_005(self, app_drivers):
        """APP-设置页面校验"""
        my_page = AppMyPage(app_drivers)
        my_page.click_setting()
        pytest.assume(my_page.check_my_info())
        pytest.assume(my_page.check_reset_password())
        pytest.assume(my_page.check_bind_phone())
        pytest.assume(my_page.check_clear_cache())
        my_page.click_return()

if __name__ == '__main__':
    pytest.main(['testcase/test_06_app_mypage.py'])
    pass


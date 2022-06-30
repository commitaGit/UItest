import pytest
from projects.web_uitest.PageObject.WebObject.web_managementpage import ManagementPage
from common.customerlogin import CustomerLogin


class TestManagement:

    def test_01(self, drivers):
        """WEB-商旅管理--差旅政策页面校验"""
        CustomerLogin(drivers).customer_login()
        management = ManagementPage(drivers)
        management.click_management()
        management.click_travel_settings()
        management.click_travel_policy()
        pytest.assume(management.travel_policy_name())
        pytest.assume(management.basic_travel_policy())
        pytest.assume(management.book_setting())
        pytest.assume(management.add_travel_policy())

    def test_02(self, drivers):
        """WEB-商旅管理--预订设置页面校验"""
        management = ManagementPage(drivers)
        pytest.assume(management.click_book_setting())
        pytest.assume(management.domestic_flight_setting())
        pytest.assume(management.insurance())
        pytest.assume(management.refund_reason())
        pytest.assume(management.change_reason())
        management.train_setting()
        pytest.assume(management.insurance())
        management.iflight_setting()
        pytest.assume(management.refund_reason())
        pytest.assume(management.change_reason())
        management.click_travel_setting_back()

    def test_03(self, drivers):
        """WEB-商旅管理--新增差旅政策页面校验"""
        management = ManagementPage(drivers)
        management.click_add_travel_policy()
        pytest.assume(management.domestic_flight_policy())
        pytest.assume(management.domestic_hotel_policy())
        management.click_open()
        pytest.assume(management.price_limit())
        pytest.assume(management.book_time_limit())
        pytest.assume(management.discount_limit())
        pytest.assume(management.bunk_limit())
        pytest.assume(management.depart_time_limit())
        pytest.assume(management.additional_remark())
        pytest.assume(management.first_tier_cities())
        pytest.assume(management.second_tier_cities())
        pytest.assume(management.third_tier_cities())
        pytest.assume(management.other_cities())
        pytest.assume(management.city_setting_button())

    def test_04(self, drivers):
        """WEB-商旅管理--事前审批配置页面"""
        management = ManagementPage(drivers)
        management.click_approval_setting()
        pytest.assume(management.setting_approval_role())
        pytest.assume(management.add_approval_process())
        pytest.assume(management.employees_without_approval())
        pytest.assume(management.basic_approval_policy())

    def test_05(self, drivers):
        """WEB-商旅管理--新增审批流程页面"""
        management = ManagementPage(drivers)
        management.click_add_approval_process()
        pytest.assume(management.personal_approval_process())
        pytest.assume(management.departmental_approval_process())
        management.click_approval_close()

    def test_06(self, drivers):
        """WEB-商旅管理--事中授权页面"""
        management = ManagementPage(drivers)
        management.refresh_page()
        management.click_authorization_settings()
        pytest.assume(management.employees_without_authorization())
        pytest.assume(management.basic_authorization_policy())

    def test_07(self, drivers):
        """WEB-商旅管理--新增授权流程页面"""
        management = ManagementPage(drivers)
        management.click_add_authorization_policy()
        pytest.assume(management.personal_authorization_process())
        pytest.assume(management.project_authorization_process())
        pytest.assume(management.departmental_authorization_process())
        management.click_authorization_close()

    def test_08(self, drivers):
        """WEB-商旅管理--事后知会设置页面"""
        management = ManagementPage(drivers)
        management.refresh_page()
        management.click_notification_settings()
        pytest.assume(management.employees_without_notification())
        pytest.assume(management.basic_notification_policy())

    def test_09(self, drivers):
        """WEB-商旅管理--新增知会流程页面"""
        management = ManagementPage(drivers)
        management.click_add_notification_policy()
        pytest.assume(management.personal_notification_process())
        pytest.assume(management.project_notification_process())
        pytest.assume(management.departmental_notification_process())
        management.click_notification_close()

    def test_10(self, drivers):
        """WEB-商旅管理--设置知会规则页面"""
        management = ManagementPage(drivers)
        management.refresh_page()
        management.click_setting_notification_rule()
        pytest.assume(management.open_notification_process())
        management.click_notification1_close()

    def test_11(self, drivers):
        """WEB-商旅管理--企业项目页面（包括新增和关联）"""
        management = ManagementPage(drivers)
        management.refresh_page()
        management.click_enterprise_project()
        management.click_add_project()
        pytest.assume(management.project_name())
        management.click_project_close()
        management.click_project_association_settings()
        pytest.assume(management.associated_project())
        management.click_associated_project_back()

    def test_12(self, drivers):
        """WEB-商旅管理--绿色通道页面"""
        management = ManagementPage(drivers)
        management.click_green_channel()
        management.click_add_green_channel_staff()
        management.click_cancel()

    def test_13(self, drivers):
        """WEB-商旅管理--城市等级页面"""
        management = ManagementPage(drivers)
        management.click_city_level()
        pytest.assume(management.first_tier_city())
        pytest.assume(management.second_tier_city())
        pytest.assume(management.third_tier_city())
        pytest.assume(management.other_city())

if __name__ == '__main__':
    pytest.main(['testcase/test_09_web_management.py'])



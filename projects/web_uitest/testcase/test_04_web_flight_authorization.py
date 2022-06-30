import pytest
from common.adminflight import AdminFlight
from common.adminlogin import AdminLogin
from common.customerlogin import CustomerLogin
from projects.web_uitest.PageObject.WebObject.web_authorizationH5page import AuthorizationPage
from projects.web_uitest.PageObject.WebObject.web_authorizationsettingpage import AuthorizationSettingPage
from projects.web_uitest.PageObject.WebObject.web_bookflightpage import BookFlightPage
from projects.web_uitest.PageObject.WebObject.web_changeflightpage import ChangeFlightPage
from projects.web_uitest.PageObject.WebObject.web_msmquerypage import SmsQueryPage
from projects.web_uitest.PageObject.WebObject.web_multiplesearchpage import MultipleSearchPage
from projects.web_uitest.PageObject.WebObject.web_returnflightpage import ReturnFlightPage

ORDER_ID = ""

@pytest.fixture(scope='module')
def flight_stub(drivers):
    AdminFlight().flight_stub(drivers)

class TestAuthorization:

    def book_flight(self, drivers, departure_city="深圳", arrive_city="北京"):
        """预订国内机票"""
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        book = BookFlightPage(drivers)
        assert "支付完成" in book.book_one_way(departure_city, arrive_city)
        ORDER_ID = book.get_order_id()
        return True

    def get_authorize_url(self, drivers, order_id):
        """获取H5授权链接"""
        login_result = AdminLogin(drivers).admin_sign()
        if not login_result:
            return False
        sms = SmsQueryPage(drivers)
        sms.to_sms_query()
        return sms.get_authorization_H5_URL(order_id)

    def authorize_agree(self, drivers, order_id):
        """订单授权通过"""
        H5_URL = self.get_authorize_url(drivers, order_id)
        authorize = AuthorizationPage(drivers)
        authorize.get_url(H5_URL)
        authorize.click_agree()

    def authorize_refuse(self, drivers, order_id):
        """订单授权拒绝"""
        H5_URL = self.get_authorize_url(drivers, order_id)
        authorize = AuthorizationPage(drivers)
        authorize.get_url(H5_URL)
        authorize.click_refuse()

    def flight_change_apply(self, drivers):
        """国内机票提交改签申请"""
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        result = ChangeFlightPage(drivers).submit_change_apply()
        ORDER_ID = result[1][:9]
        return result

    def search_order_status(self, drivers, order_id):
        """后台综合查询中查询订单状态"""
        search = MultipleSearchPage(drivers)
        search.flight()
        search.order_id_search(order_id)
        return search.get_order_status()

    def flight_return_apply(self, drivers):
        """国内机票提交退票申请"""
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        result = ReturnFlightPage(drivers).submit_flight_return_apply()
        ORDER_ID = result[1][:9]
        return result

    @pytest.mark.dependency(name="open_authorize")
    def test_001(self, drivers):
        """WEB-开启授权流程"""
        CustomerLogin(drivers).customer_login()
        setting = AuthorizationSettingPage(drivers)
        setting.to_authorization_setting()
        setting.set_authorization_rule()
        if not setting.authorization_open_status():
            setting.click_authorization_switch()
            setting.click_save()
            assert "保存成功" in setting.save_result()

    @pytest.mark.dependency(name="one_level")
    def test_002(self, drivers):
        """WEB-设置只需一级授权"""
        CustomerLogin(drivers).customer_login()
        setting = AuthorizationSettingPage(drivers)
        setting.to_authorization_setting()
        if setting.secondary_authorizer_exist():
            setting.click_basics_change()
            setting.clear_secondary_authorizer()
            setting.click_save()
        assert not setting.secondary_authorizer_exist()

    @pytest.mark.dependency(name="book_flight")
    def test_003(self, drivers, flight_stub):
        """WEB-授权--国内机票预订"""
        assert self.book_flight(drivers)

    @pytest.mark.dependency(name="book_authorize", depends=["open_authorize", "book_flight"])
    def test_004(self, drivers):
        """WEB-国内机票预订--一级授权通过"""
        self.authorize_agree(drivers, ORDER_ID)
        authorize = AuthorizationPage(drivers)
        assert "授权通过" in authorize.authorize_status_one()

    @pytest.mark.dependency(name="ticket_confirm", depends=["book_flight", "one_level"])
    def test_005(self, drivers):
        """WEB-授权--国内机票出票"""
        assert AdminFlight().flight_ticket_confirm(drivers, ORDER_ID)

    @pytest.mark.dependency(name="change_apply", depends=["ticket_confirm"])
    def test_006(self, drivers):
        """WEB-授权--国内机票提交改签申请"""
        assert "改签申请已提交" in self.flight_change_apply(drivers)[0]

    @pytest.mark.dependency(name="change_offer", depends=["change_apply"])
    def test_007(self, drivers):
        """WEB-授权--国内机票完成改签报价任务"""
        assert AdminFlight().change_offer(drivers, ORDER_ID)

    @pytest.mark.dependency(name="change_refuse", depends=["change_offer"])
    def test_008(self, drivers):
        """WEB-国内机票改签--一级授权拒绝"""
        self.authorize_refuse(drivers, ORDER_ID)
        authorize = AuthorizationPage(drivers)
        assert "授权拒绝" in authorize.authorize_status_one()
        AdminLogin(drivers).admin_sign()
        assert "已取消" in self.search_order_status(drivers, ORDER_ID)

    @pytest.mark.dependency(name="change_authorization1", depends=["change_offer", "change_refuse"])
    def test_009_01(self, drivers):
        """WEB-国内机票改签单--一级授权通过-提交改签申请"""
        self.flight_change_apply(drivers)

    @pytest.mark.dependency(name="change_authorization2", depends=["change_authorization1"])
    def test_009_02(self, drivers):
        """WEB-国内机票改签单--一级授权通过-完成改签报价任务"""
        assert AdminFlight().change_offer(drivers, ORDER_ID)

    @pytest.mark.dependency(name="change_authorization", depends=["change_authorization2"])
    def test_009_03(self, drivers):
        """WEB-国内机票改签单--一级授权通过-一级授权通过"""
        self.authorize_agree(drivers, ORDER_ID)
        authorize = AuthorizationPage(drivers)
        assert "授权通过" in authorize.authorize_status_one()

    @pytest.mark.dependency(name="change_confirm", depends=["change_authorization"])
    def test_010(self, drivers):
        """WEB-国内机票改签单--完成改签确认出票"""
        assert AdminFlight().change_confirm(drivers, ORDER_ID), "完成改签确认任务失败"
        order_status = self.search_order_status(drivers, ORDER_ID)
        assert order_status == "已出票"

    @pytest.mark.dependency(name="return_apply", depends=["change_confirm"])
    def test_011(self, drivers):
        """WEB-授权--国内机票退票申请提交"""
        assert "退票申请已提交" in self.flight_return_apply(drivers)[0]

    @pytest.mark.dependency(name="return_refuse", depends=["return_apply"])
    def test_012(self, drivers):
        """WEB-国内机票退票--一级授权拒绝"""
        self.authorize_refuse(drivers, ORDER_ID)
        authorize = AuthorizationPage(drivers)
        assert "授权拒绝" in authorize.authorize_status_one()
        AdminLogin(drivers).admin_sign()
        assert "已出票" in self.search_order_status(drivers, ORDER_ID)

    @pytest.mark.dependency(name="return_authorization1", depends=["return_apply", "return_refuse"])
    def test_013_01(self, drivers):
        """WEB-国内机票退票单--一级授权通过-提交退票申请"""
        assert "退票申请已提交" in self.flight_return_apply(drivers)[0]

    @pytest.mark.dependency(name="return_authorization", depends=["return_authorization1"])
    def test_013_02(self, drivers):
        """WEB-国内机票退票单--一级授权通过-一级授权通过"""
        self.authorize_agree(drivers, ORDER_ID)
        authorize = AuthorizationPage(drivers)
        assert "授权通过" in authorize.authorize_status_one()

    @pytest.mark.dependency(depends=["return_authorization"])
    def test_014(self, drivers):
        """WEB-授权--国内机票退票确认"""
        assert AdminFlight().return_confirm(drivers, ORDER_ID), "完成退票确认任务失败"
        order_status = self.search_order_status(drivers, ORDER_ID)
        assert order_status == "已退票"

    @pytest.mark.dependency(depends=["book_flight"])
    def test_015(self, drivers):
        """WEB-国内机票预订--一级授权拒绝"""
        assert self.book_flight(drivers), "预订机票失败"
        self.authorize_refuse(drivers, ORDER_ID)
        authorize = AuthorizationPage(drivers)
        assert "授权拒绝" in authorize.authorize_status_one()
        AdminLogin(drivers).admin_sign()
        assert "已取消" in self.search_order_status(drivers, ORDER_ID)

    @pytest.mark.dependency(name="two_level")
    def test_016(self, drivers):
        """WEB-设置二级授权人"""
        CustomerLogin(drivers).customer_login()
        setting = AuthorizationSettingPage(drivers)
        setting.to_authorization_setting()
        if not setting.secondary_authorizer_exist():
            setting.click_basics_change()
            setting.input_secondary_authorizer()
            setting.click_save()
        assert setting.secondary_authorizer_exist()

    @pytest.mark.dependency(name='two_level_book', depends=["book_flight", "two_level"])
    def test_017(self, drivers):
        """WEB-国内机票预订--二级授权通过"""
        self.book_flight(drivers)
        try: # 重试的时候可能已经授权了
            self.authorize_agree(drivers, ORDER_ID)
            self.authorize_agree(drivers, ORDER_ID)
        except:
            pass
        authorize = AuthorizationPage(drivers)
        assert "授权通过" in authorize.authorize_status_two()
        assert AdminFlight().flight_ticket_confirm(drivers, ORDER_ID)
        assert "已出票" in self.search_order_status(drivers, ORDER_ID)

    @pytest.mark.dependency(name="two_level_change_refuse1", depends=["change_offer", "two_level_book"])
    def test_018_01(self, drivers):
        """WEB-国内机票改签--二级授权拒绝-提交改签申请"""
        assert "改签申请已提交" in self.flight_change_apply(drivers)[0]

    @pytest.mark.dependency(name="two_level_change_refuse2", depends=["two_level_change_refuse1"])
    def test_018_02(self, drivers):
        """WEB-国内机票改签--二级授权拒绝-完成改签报价任务"""
        assert AdminFlight().change_offer(drivers, ORDER_ID)

    @pytest.mark.dependency(name="two_level_change_refuse", depends=["two_level_change_refuse2"])
    def test_018_03(self, drivers):
        """WEB-国内机票改签--二级授权拒绝-审批拒绝"""
        try:
            self.authorize_agree(drivers, ORDER_ID)
        finally:
            self.authorize_refuse(drivers, ORDER_ID)
        authorize = AuthorizationPage(drivers)
        assert "授权拒绝" in authorize.authorize_status_two()
        AdminLogin(drivers).admin_sign()
        assert "已取消" in self.search_order_status(drivers, ORDER_ID)

    @pytest.mark.dependency(name="two_level_change1", depends=["two_level_change_refuse"])
    def test_019_01(self, drivers):
        """WEB-国内机票改签--二级授权通过-提交改签申请"""
        assert "改签申请已提交" in self.flight_change_apply(drivers)[0]

    @pytest.mark.dependency(name="two_level_change2", depends=["two_level_change1"])
    def test_019_02(self, drivers):
        """WEB-国内机票改签--二级授权通过-完成改签报价任务"""
        assert AdminFlight().change_offer(drivers, ORDER_ID)

    @pytest.mark.dependency(name="two_level_change", depends=["two_level_change2"])
    def test_019_03(self, drivers):
        """WEB-国内机票改签--二级授权通过-授权通过"""
        try: # 重试的时候可能已经授权了
            self.authorize_agree(drivers, ORDER_ID)
            self.authorize_agree(drivers, ORDER_ID)
        except:
            pass
        authorize = AuthorizationPage(drivers)
        assert "授权通过" in authorize.authorize_status_two()
        assert AdminFlight().change_confirm(drivers, ORDER_ID), "完成改签确认任务失败"
        assert "已出票" in self.search_order_status(drivers, ORDER_ID)

    @pytest.mark.dependency(name="two_level_return_refuse1", depends=["return_apply", "two_level_change"])
    def test_020_01(self, drivers):
        """WEB-国内机票退票--二级授权拒绝-提交退票申请"""
        assert "退票申请已提交" in self.flight_return_apply(drivers)[0]

    @pytest.mark.dependency(name="two_level_return_refuse", depends=["two_level_return_refuse1"])
    def test_020_02(self, drivers):
        """WEB-国内机票退票--二级授权拒绝-授权拒绝"""
        try:
            self.authorize_agree(drivers, ORDER_ID)
        finally:
            self.authorize_refuse(drivers, ORDER_ID)
        authorize = AuthorizationPage(drivers)
        assert "授权拒绝" in authorize.authorize_status_two()
        AdminLogin(drivers).admin_sign()
        assert "已出票" in self.search_order_status(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["two_level_return_refuse"], name="two_level_return_pass")
    def test_021_01(self, drivers):
        """WEB-国内机票退票--二级授权通过-提交退票申请"""
        assert "退票申请已提交" in self.flight_return_apply(drivers)[0]

    @pytest.mark.dependency(depends=["two_level_return_pass"])
    def test_021_02(self, drivers):
        """WEB-国内机票退票--二级授权通过-授权通过"""
        try: # 重试的时候可能已经授权了
            self.authorize_agree(drivers, ORDER_ID)
            self.authorize_agree(drivers, ORDER_ID)
        except:
            pass
        authorize = AuthorizationPage(drivers)
        assert "授权通过" in authorize.authorize_status_two()
        assert AdminFlight().return_confirm(drivers, ORDER_ID), "完成退票确认任务失败"
        assert "已退票" in self.search_order_status(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["book_flight", "two_level"])
    def test_022(self, drivers):
        """WEB-国内机票预订--二级授权拒绝"""
        self.book_flight(drivers)
        self.authorize_agree(drivers, ORDER_ID)
        self.authorize_refuse(drivers, ORDER_ID)
        authorize = AuthorizationPage(drivers)
        assert "授权拒绝" in authorize.authorize_status_two()
        AdminLogin(drivers).admin_sign()
        assert "已取消" in self.search_order_status(drivers, ORDER_ID)

    def test_023(self, drivers):
        """WEB-关闭授权流程"""
        CustomerLogin(drivers).customer_login()
        setting = AuthorizationSettingPage(drivers)
        setting.to_authorization_setting()
        setting.set_authorization_rule()
        if setting.authorization_open_status():
            setting.click_authorization_switch()
            setting.click_save()
            assert "保存成功" in setting.save_result()

if __name__ == '__main__':
    pytest.main(['testcase/test_04_web_authorization.py'])

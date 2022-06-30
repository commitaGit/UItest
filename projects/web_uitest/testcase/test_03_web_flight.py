import pytest
from common.adminflight import AdminFlight
from common.adminlogin import AdminLogin
from common.customerlogin import CustomerLogin
from projects.web_uitest.PageObject.WebObject.web_authorizationsettingpage import AuthorizationSettingPage
from projects.web_uitest.PageObject.WebObject.web_bookflightpage import BookFlightPage
from projects.web_uitest.PageObject.WebObject.web_changeflightpage import ChangeFlightPage
from projects.web_uitest.PageObject.WebObject.web_flightorderhandlepage import FlightOrderHandlePage
from projects.web_uitest.PageObject.WebObject.web_multiplesearchpage import MultipleSearchPage
from projects.web_uitest.PageObject.WebObject.web_returnflightpage import ReturnFlightPage

ORDER_ID = ""

@pytest.fixture(scope='module')
def close_authorization(drivers):
    """WEB-关闭授权流程"""
    CustomerLogin(drivers).customer_login()
    setting = AuthorizationSettingPage(drivers)
    setting.to_authorization_setting()
    setting.set_authorization_rule()
    if setting.authorization_open_status():
        setting.click_authorization_switch()
        setting.click_save()
        assert "保存成功" in setting.save_result()

@pytest.fixture(scope='module')
def flight_stub(drivers):
    """国内机票测试桩全开启为成功"""
    AdminFlight().flight_stub(drivers)

class TestFlight:

    def book_flight(self, drivers, departure_city="深圳", arrive_city="北京", check=True):
        """预订国内机票"""
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        book = BookFlightPage(drivers)
        assert "支付完成" in book.book_one_way(departure_city, arrive_city, check)
        ORDER_ID = book.get_order_id()
        return True

    def search_order_status(self, drivers, order_id):
        """后台综合查询中查询订单状态"""
        search = MultipleSearchPage(drivers)
        search.flight()
        search.order_id_search(order_id)
        return search.get_order_status()

    def submit_change_apply(self, drivers):
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        result = ChangeFlightPage(drivers).submit_change_apply()
        ORDER_ID = result[1][:9]
        return result[0]

    def submit_return_apply(self, drivers):
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        result = ReturnFlightPage(drivers).submit_flight_return_apply()
        ORDER_ID = result[1][:9]
        return result[0]

    @pytest.mark.dependency(name="book_flight")
    def test_001(self, drivers, flight_stub, close_authorization):
        """WEB-国内机票--预订"""
        assert self.book_flight(drivers)

    @pytest.mark.dependency(name="ticket_confirm", depends=["book_flight"])
    def test_002(self, drivers):
        """WEB-国内机票--出票"""
        assert AdminFlight().flight_ticket_confirm(drivers, ORDER_ID)

    @pytest.mark.dependency(name="change_apply", depends=["ticket_confirm"])
    def test_003(self, drivers):
        """WEB-国内机票--提交改签申请"""
        assert "改签申请已提交" in self.submit_change_apply(drivers)

    @pytest.mark.dependency(name="change_offer", depends=["change_apply"])
    def test_004(self, drivers):
        """WEB-国内机票--改签报价取消"""
        AdminLogin(drivers).admin_sign()
        change_offer = FlightOrderHandlePage(drivers)
        assert change_offer.change_offer_cancel(ORDER_ID), "改签报价取消任务失败"
        assert change_offer.task_submit_result(), "没有调出任务按钮"
        order_status = self.search_order_status(drivers, ORDER_ID)
        assert order_status == "已取消"

    @pytest.mark.dependency(name="change_offer1", depends=["change_offer"])
    def test_005_01(self, drivers):
        """WEB-国内机票--完成改签报价任务-提交改签申请"""
        assert "改签申请已提交" in self.submit_change_apply(drivers)

    @pytest.mark.dependency(name="change_offer2", depends=["change_offer1"])
    def test_005_02(self, drivers):
        """WEB-国内机票--完成改签报价任务-完成改签报价任务"""
        assert AdminFlight().change_offer(drivers, ORDER_ID)

    @pytest.mark.dependency(name="change_confirm", depends=["change_offer2"])
    def test_006(self, drivers):
        """WEB-国内机票改签单--改签确认取消"""
        change_confirm = FlightOrderHandlePage(drivers)
        assert change_confirm.change_confirm_cancel(ORDER_ID), "完成改签确认取消任务失败"
        assert change_confirm.task_submit_result(), "没有调出任务按钮"
        order_status = self.search_order_status(drivers, ORDER_ID)
        assert order_status == "已取消"

    @pytest.mark.dependency(name="change_confirm1", depends=["change_offer2"])
    def test_007_01(self, drivers):
        """WEB-国内机票改签单--完成改签确认出票-提交改签申请"""
        assert "改签申请已提交" in self.submit_change_apply(drivers)

    @pytest.mark.dependency(name="change_confirm2", depends=["change_confirm1"])
    def test_007_02(self, drivers):
        """WEB-国内机票改签单--完成改签确认出票-完成改签报价任务"""
        assert AdminFlight().change_offer(drivers, ORDER_ID)

    @pytest.mark.dependency(name="change_confirm3", depends=["change_confirm2"])
    def test_007_03(self, drivers):
        """WEB-国内机票改签单--完成改签确认出票-完成改签确认任务"""
        change = FlightOrderHandlePage(drivers)
        assert change.change_confirm(ORDER_ID), "完成改签确认任务失败"
        assert change.task_submit_result(), "没有调出任务按钮"
        order_status = self.search_order_status(drivers, ORDER_ID)
        assert order_status == "已出票"

    @pytest.mark.dependency(name="return_apply", depends=["change_confirm3"])
    def test_008(self, drivers):
        """WEB-国内机票--提交退票申请"""
        assert "退票申请已提交" in self.submit_return_apply(drivers)

    @pytest.mark.dependency(depends=["return_apply"])
    def test_009(self, drivers):
        """WEB-国内机票--退票取消"""
        AdminLogin(drivers).admin_sign()
        return_confirm = FlightOrderHandlePage(drivers)
        assert return_confirm.return_confirm_cancel(ORDER_ID), "完成退票取消任务失败"
        assert return_confirm.task_submit_result(), "没有调出任务按钮"
        order_status = self.search_order_status(drivers, ORDER_ID)
        assert order_status == "已出票"

    @pytest.mark.dependency(depends=["return_apply"], name="return_confirm1")
    def test_010_01(self, drivers):
        """WEB-国内机票--退票确认-提交退票申请"""
        assert "退票申请已提交" in self.submit_return_apply(drivers)

    @pytest.mark.dependency(depends=["return_confirm1"])
    def test_010_02(self, drivers):
        """WEB-国内机票--退票确认-完成退票确认任务"""
        assert AdminFlight().return_confirm(drivers, ORDER_ID)
        order_status = self.search_order_status(drivers, ORDER_ID)
        assert order_status == "已退票"

    @pytest.mark.dependency(name="round_book")
    def test_011(self, drivers):
        """WEB-国内机票--预订往返程机票"""
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        book = BookFlightPage(drivers)
        assert "支付完成" in book.book_round_trip(departure_city="深圳", arrive_city="北京")
        ORDER_ID = book.get_order_id()

    @pytest.mark.dependency(name="round_confirm", depends=["round_book"])
    def test_012(self, drivers):
        """WEB-国内机票--返程机票出票"""
        assert AdminFlight().round_trip_ticket_confirm(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["round_confirm"], name="go_return1")
    def test_013_01(self, drivers):
        """WEB-国内机票--去程退票-提交退票申请"""
        CustomerLogin(drivers).customer_login()
        assert "退票申请已提交" in ReturnFlightPage(drivers).go_trip_return_apply(ORDER_ID)

    @pytest.mark.dependency(depends=["go_return1"])
    def test_013_02(self, drivers):
        """WEB-国内机票--去程退票-完成退票任务"""
        assert AdminFlight().return_confirm(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["round_confirm"], name="back_return1")
    def test_014_01(self, drivers):
        """WEB-国内机票--返程退票"""
        CustomerLogin(drivers).customer_login()
        assert "退票申请已提交" in ReturnFlightPage(drivers).return_trip_return_apply(ORDER_ID)

    @pytest.mark.dependency(depends=["back_return1"])
    def test_014_02(self, drivers):
        """WEB-国内机票--返程退票"""
        assert AdminFlight().return_confirm(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["round_confirm"], name="round_return")
    def test_015_01(self, drivers):
        """WEB-国内机票--往返一起退票-提交退票申请"""
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        result =  ReturnFlightPage(drivers).round_trip_return_apply()
        assert "退票申请已提交" in result[0]
        ORDER_ID = result[1]

    @pytest.mark.dependency(depends=["round_return"])
    def test_015_02(self, drivers):
        """WEB-国内机票--往返一起退票-完成退票任务"""
        AdminLogin(drivers).admin_sign()
        return_confirm = FlightOrderHandlePage(drivers)
        assert return_confirm.round_trip_return_confirm(ORDER_ID)

    @pytest.mark.dependency(name="persons")
    def test_016(self, drivers):
        """WEB-国内机票--预订多人单程机票"""
        assert self.book_flight(drivers,check=False), "预订机票失败"
        assert AdminFlight().flight_ticket_confirm(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["persons"], name="persons_return1")
    def test_017_01(self, drivers):
        """WEB-国内机票--多人订单--一人退票-提交退票申请"""
        CustomerLogin(drivers).customer_login()
        assert "退票申请已提交" in ReturnFlightPage(drivers).go_trip_return_apply(ORDER_ID)

    @pytest.mark.dependency(depends=["persons_return1"])
    def test_017_02(self, drivers):
        """WEB-国内机票--多人订单--一人退票-完成退票任务"""
        assert AdminFlight().return_confirm(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["persons"], name="persons_return2")
    def test_018_01(self, drivers):
        """WEB-国内机票--多人订单--多次多人退票-提交退票申请"""
        CustomerLogin(drivers).customer_login()
        assert "退票申请已提交" in ReturnFlightPage(drivers).many_people_return_apply()

    @pytest.mark.dependency(depends=["persons_return2"])
    def test_018_02(self, drivers):
        """WEB-国内机票--多人订单--多次多人退票-完成退票任务"""
        assert AdminFlight().return_confirm(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["book_flight"])
    def test_019(self, drivers):
        """WEB--国内机票--未支付订单取消"""
        CustomerLogin(drivers).customer_login()
        book = BookFlightPage(drivers)
        book.place_order(departure_city="深圳", arrive_city="北京")
        book.get_order_id()
        assert "已取消" in book.cancel_order()

if __name__ == '__main__':
    pytest.main(['testcase/test_03_web_flight.py'])


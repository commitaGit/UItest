import pytest
from app_uitest.PageObject.AppObject.app_changeflightpage import AppChangeFlight
from app_uitest.PageObject.AppObject.app_returnflightpage import AppReturnFlight
from app_uitest.PageObject.AppObject.app_bookflightpage import AppBookFlight
from common.readconfig import ini
from app_uitest.PageObject.WebObject.web_multiplesearchpage import MultipleSearchPage
from app_uitest.PageObject.WebObject.web_flightorderhandlepage import FlightOrderHandlePage
from common.adminlogin import AdminLogin
from time import sleep

# APP测试账号
ACCOUNT = ini._get("APPACCOUNT", "ACCOUNT")
PASSWORD = ini._get("APPACCOUNT", "PASSWORD")
ORDER_ID = ""

class TestAppFlight:

    def book_flight(self, app_drivers, departure_city="深圳", arrive_city="北京"):
        global ORDER_ID
        book = AppBookFlight(app_drivers)
        book.launch_app()
        book.click_flight_product()
        book.choose_departure_city(departure_city)
        book.choose_arrive_city(arrive_city)
        book.click_search()
        book.click_flight()
        book.click_book()
        book.passenger_by_add_staff()
        book.place_order()
        book.click_pay()
        book.click_credit_pay()
        assert "支付成功" in book.get_pay_result()
        book.click_view_order()
        ORDER_ID = book.get_order_id()
        return True

    def flight_ticket_confirm(self, drivers, order_id):
        """国内机票出票"""
        AdminLogin(drivers).admin_sign()
        order_status = self.search_order_status(drivers, order_id)
        n = 0
        while n < 10:
            if order_status == "已出票":
                break
            order_status = MultipleSearchPage(drivers).get_order_status()
            n += 1
            sleep(0.5)
        if order_status != "已出票":
            return FlightOrderHandlePage(drivers).ticket_confirm(ORDER_ID, "出票")
        return True

    def search_order_status(self, drivers, order_id):
        """后台综合查询中查询订单状态"""
        search = MultipleSearchPage(drivers)
        search.flight()
        search.order_id_search(order_id)
        return search.get_order_status()

    @pytest.mark.dependency(name="book_flight")
    def test_001(self, app_drivers):
        """APP-国内机票--预订"""
        assert self.book_flight(app_drivers)

    @pytest.mark.dependency(name="ticket_confirm", depends=["book_flight"])
    def test_002(self, drivers):
        """WEB-国内机票--出票"""
        assert self.flight_ticket_confirm(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["ticket_confirm"])
    def test_003(self, app_drivers):
        """APP-国内机票--提交改签申请"""
        CHANGE = AppChangeFlight(app_drivers)
        CHANGE.click_change_button()
        CHANGE.choose_passenger()
        CHANGE.choose_route()
        CHANGE.choose_departure_date()
        CHANGE.click_search()
        CHANGE.choose_flight()
        CHANGE.change_confirm()
        assert "待改签" in CHANGE.get_order_status()

    def test_004(self, app_drivers, drivers):
        """APP-国内机票--提交退票申请"""
        assert self.book_flight(app_drivers)
        assert self.flight_ticket_confirm(drivers, ORDER_ID)
        RETURN = AppReturnFlight(app_drivers)
        RETURN.click_return_button()
        RETURN.choose_passenger()
        RETURN.choose_route()
        assert "待退票" in RETURN.get_order_status()

if __name__ == '__main__':
    pytest.main(['testcase/test_app_flight.py'])
    pass


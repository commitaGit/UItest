import pytest
from common.adminflight import AdminFlight
from h5_uitest.PageObject.WebObject.h5_flightpage import FlightPage
from h5_uitest.PageObject.WebObject.web_systemmanagepage import FlightTestStubPage
from h5_uitest.PageObject.WebObject.web_multiplesearchpage import MultipleSearchPage
from h5_uitest.PageObject.WebObject.web_flightorderhandlepage import FlightOrderHandlePage

ORDER_ID = ""

@pytest.fixture(scope='module')
def flight_stub(admin_drivers):
    """国内机票测试桩全开启为成功"""
    FlightTestStubPage(admin_drivers).flight_stub_setting()

class TestFlight:

    def book_flight(self, drivers, departure_city="深圳", arrive_city="北京", check=True):
        """预订国内机票"""
        global ORDER_ID
        book = FlightPage(drivers)
        assert "支付成功" in book.flight_one_way(departure_city, arrive_city, check)
        ORDER_ID = book.get_order_id()
        return True

    def search_order_status(self, admin_drivers, order_id):
        """后台综合查询中查询订单状态"""
        search = MultipleSearchPage(admin_drivers)
        search.flight()
        search.order_id_search(order_id)
        return search.get_order_status()

    def submit_change_apply(self, drivers):
        global ORDER_ID
        ORDER_ID = FlightPage(drivers).submit_change_apply()
        return True

    def submit_return_apply(self, drivers):
        global ORDER_ID
        ORDER_ID = FlightPage(drivers).submit_return_apply()
        return True

    @pytest.mark.dependency(name="book_flight")
    def test_001(self, drivers, flight_stub):
        """WEB-国内机票--预订"""
        assert self.book_flight(drivers)

    @pytest.mark.dependency(name="ticket_confirm", depends=["book_flight"])
    def test_002(self, admin_drivers):
        """WEB-国内机票--出票"""
        assert AdminFlight().flight_ticket_confirm(admin_drivers, ORDER_ID)

    @pytest.mark.dependency(name="change_apply", depends=["ticket_confirm"])
    def test_003(self, drivers):
        """WEB-国内机票--提交改签申请"""
        assert self.submit_change_apply(drivers)

    @pytest.mark.dependency(name="change_confirm1", depends=["change_apply"])
    def test_004(self, admin_drivers):
        """WEB-国内机票改签单--完成改签报价任务"""
        change = FlightOrderHandlePage(admin_drivers)
        assert change.change_offer(ORDER_ID)
        assert change.task_submit_result()

    @pytest.mark.dependency(name="change_confirm2", depends=["change_confirm1"])
    def test_005(self, admin_drivers):
        """WEB-国内机票改签单--完成改签确认任务"""
        change = FlightOrderHandlePage(admin_drivers)
        assert change.change_confirm(ORDER_ID)
        assert change.task_submit_result()
        order_status = self.search_order_status(admin_drivers, ORDER_ID)
        assert order_status == "已出票"

    @pytest.mark.dependency(name="return_apply", depends=["change_confirm2"])
    def test_006(self, drivers):
        """WEB-国内机票--提交退票申请"""
        assert self.submit_return_apply(drivers)

    @pytest.mark.dependency(depends=["return_apply"])
    def test_007(self, admin_drivers):
        """WEB-国内机票--退票确认-完成退票确认任务"""
        return_confirm = FlightOrderHandlePage(admin_drivers)
        assert return_confirm.return_confirm(ORDER_ID)
        assert return_confirm.task_submit_result()
        order_status = self.search_order_status(admin_drivers, ORDER_ID)
        assert order_status == "已退票"

    @pytest.mark.dependency(name="round_book")
    def test_008(self, drivers):
        """WEB-国内机票--预订往返程机票"""
        global ORDER_ID
        book = FlightPage(drivers)
        assert "支付成功" in book.flight_round_trip(departure_city="深圳", arrive_city="上海")
        ORDER_ID = book.get_order_id()

    @pytest.mark.dependency(name="round_confirm", depends=["round_book"])
    def test_009(self, admin_drivers):
        """WEB-国内机票--返程机票出票"""
        assert AdminFlight().round_trip_ticket_confirm(admin_drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["round_confirm"], name="go_return1")
    def test_010(self, drivers):
        """WEB-国内机票--去程退票-提交退票申请"""
        global ORDER_ID
        ORDER_ID = FlightPage(drivers).go_trip_return()

    @pytest.mark.dependency(depends=["go_return1"])
    def test_011(self, admin_drivers):
        """WEB-国内机票--去程退票-完成退票任务"""
        return_confirm = FlightOrderHandlePage(admin_drivers)
        assert return_confirm.return_confirm(ORDER_ID)
        assert return_confirm.task_submit_result()

    @pytest.mark.dependency(depends=["round_confirm"], name="back_return1")
    def test_012(self, drivers):
        """WEB-国内机票--返程退票--提交退票申请"""
        global ORDER_ID
        ORDER_ID = FlightPage(drivers).back_trip_return()

    @pytest.mark.dependency(depends=["back_return1"])
    def test_013(self, admin_drivers):
        """WEB-国内机票--返程退票--完成退票任务"""
        return_confirm = FlightOrderHandlePage(admin_drivers)
        assert return_confirm.return_confirm(ORDER_ID)
        assert return_confirm.task_submit_result()

    @pytest.mark.dependency(depends=["round_confirm"], name="round_return")
    def test_014(self, drivers):
        """WEB-国内机票--往返一起退票-提交退票申请"""
        global ORDER_ID
        ORDER_ID = FlightPage(drivers).round_trip_return()

    @pytest.mark.dependency(depends=["round_return"])
    def test_015(self, admin_drivers):
        """WEB-国内机票--往返一起退票-完成退票任务"""
        return_confirm = FlightOrderHandlePage(admin_drivers)
        assert return_confirm.round_trip_return_confirm(ORDER_ID)

    @pytest.mark.dependency(depends=["book_flight"])
    def test_016(self, drivers):
        """WEB--国内机票--未支付订单取消"""
        book = FlightPage(drivers)
        book.place_order(departure_city="深圳", arrive_city="上海")
        assert "已取消" in book.cancel_order()

if __name__ == '__main__':
    pytest.main(['testcase/test_01_h5_flight.py'])

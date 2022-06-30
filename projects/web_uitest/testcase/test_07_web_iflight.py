import pytest
from projects.web_uitest.PageObject.WebObject.web_iflightpage import IntFlightPage
from projects.web_uitest.PageObject.WebObject.web_systemmanagepage import FlightTestStubPage
from projects.web_uitest.PageObject.WebObject.web_multiplesearchpage import MultipleSearchPage
from projects.web_uitest.PageObject.WebObject.web_iflightorderhandlepage import IntFlightOrderHandlePage
from common.adminlogin import AdminLogin
from common.customerlogin import CustomerLogin

ORDER_ID = ""

@pytest.fixture(scope='module')
def flight_stub(drivers):
    login_result = AdminLogin(drivers).admin_sign()
    if not login_result:
        return False
    FlightTestStubPage(drivers).iflight_stub_setting()

class TestIntFlight:

    def book_iflight(self, drivers, departure_city="香港", arrive_city="曼谷"):
        """预订国际机票"""
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        BOOK = IntFlightPage(drivers)
        BOOK.generate_order(departure_city, arrive_city)
        BOOK.click_credit_pay()
        pay_result = BOOK.get_pay_result()
        assert "支付成功" in pay_result
        ORDER_ID = BOOK.get_order_id()
        return True

    @pytest.mark.dependency(name="book")
    def test_001(self, drivers, flight_stub):
        """WEB-国际机票--前台预订"""
        assert self.book_iflight(drivers)

    @pytest.mark.dependency(name="ticket_apply", depends=["book"])
    def test_002(self, drivers):
        """WEB-国际机票--提交出票申请"""
        AdminLogin(drivers).admin_sign()
        handle = IntFlightOrderHandlePage(drivers)
        assert handle.ticket_apply(ORDER_ID)
        assert handle.task_submit_result()

    @pytest.mark.dependency(name="ticket_confirm", depends=["ticket_apply"])
    def test_003(self, drivers):
        """WEB-国际机票--完成出票确认任务"""
        handle = IntFlightOrderHandlePage(drivers)
        assert handle.ticket_confirm(ORDER_ID)
        assert handle.task_submit_result()

    @pytest.mark.dependency(name="change", depends=["ticket_confirm"])
    def test_004(self, drivers):
        """WEB-国际机票--提交改签申请"""
        CustomerLogin(drivers).customer_login()
        assert "提交改签申请成功" in IntFlightPage(drivers).submit_change_apply()

    @pytest.mark.dependency(name="change_cancel", depends=["change"])
    def test_005(self, drivers):
        """WEB-国际机票--完成改签申请取消任务"""
        AdminLogin(drivers).admin_sign()
        handle = IntFlightOrderHandlePage(drivers)
        handle.change_apply_cancel(ORDER_ID)
        assert handle.task_submit_result()

    @pytest.mark.dependency(name="change1", depends=["change_cancel"])
    def test_006_01(self, drivers):
        """WEB-国际机票--完成改签申请-提交改签申请"""
        CustomerLogin(drivers).customer_login()
        assert "提交改签申请成功" in IntFlightPage(drivers).submit_change_apply()

    @pytest.mark.dependency(name="change_apply", depends=["change1"])
    def test_006_02(self, drivers):
        """WEB-国际机票--完成改签申请任务"""
        AdminLogin(drivers).admin_sign()
        handle = IntFlightOrderHandlePage(drivers)
        assert handle.change_apply(ORDER_ID)
        assert handle.task_submit_result()

    @pytest.mark.dependency(name="change_confirm", depends=["change_apply"])
    def test_007(self, drivers):
        """WEB-国际机票--完成改签确认任务"""
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        ORDER_ID = IntFlightPage(drivers).get_change_order_id()
        AdminLogin(drivers).admin_sign()
        handle = IntFlightOrderHandlePage(drivers)
        assert handle.change_confirm(ORDER_ID)
        assert handle.task_submit_result()

    @pytest.mark.dependency(name="return_apply", depends=["change_confirm"])
    def test_008(self, drivers):
        """WEB-国际机票--提交退票申请"""
        CustomerLogin(drivers).customer_login()
        assert "提交退票申请成功" in IntFlightPage(drivers).submit_return_apply()

    @pytest.mark.dependency(name="return_apply_cancel", depends=["return_apply"])
    def test_009(self, drivers):
        """WEB-国际机票--完成退票申请取消任务"""
        AdminLogin(drivers).admin_sign()
        handle = IntFlightOrderHandlePage(drivers)
        handle.return_apply_cancel(ORDER_ID)
        assert handle.task_submit_result()

    @pytest.mark.dependency(name="return_apply1", depends=["return_apply_cancel"])
    def test_010_01(self, drivers):
        """WEB-国际机票--退票确认取消-提交退票申请"""
        CustomerLogin(drivers).customer_login()
        assert "提交退票申请成功" in IntFlightPage(drivers).submit_return_apply()

    @pytest.mark.dependency(name="return_apply_complete", depends=["return_apply1"])
    def test_010_02(self, drivers):
        """WEB-国际机票--退票确认取消-完成退票申请"""
        AdminLogin(drivers).admin_sign()
        handle = IntFlightOrderHandlePage(drivers)
        assert handle.return_apply(ORDER_ID)
        assert handle.task_submit_result()

    @pytest.mark.dependency(name="return_confirm_cancel", depends=["return_apply_complete"])
    def test_011(self, drivers):
        """WEB-国际机票--完成退票确认取消任务"""
        handle = IntFlightOrderHandlePage(drivers)
        handle.return_confirm_cancel(ORDER_ID)
        assert handle.task_submit_result()

    @pytest.mark.dependency(name="return_apply2", depends=["return_confirm_cancel"])
    def test_012_01(self, drivers):
        """WEB-国际机票--退票确认-提交退票申请"""
        CustomerLogin(drivers).customer_login()
        assert "提交退票申请成功" in IntFlightPage(drivers).submit_return_apply()

    @pytest.mark.dependency(name="return_apply_complete1", depends=["return_apply2"])
    def test_012_02(self, drivers):
        """WEB-国际机票--退票确认-完成退票申请"""
        AdminLogin(drivers).admin_sign()
        handle = IntFlightOrderHandlePage(drivers)
        assert handle.return_apply(ORDER_ID)
        assert handle.task_submit_result()

    @pytest.mark.dependency(depends=["return_apply_complete1"])
    def test_012_03(self, drivers):
        """WEB-国际机票--完成退票确认任务"""
        handle = IntFlightOrderHandlePage(drivers)
        assert handle.return_confirm(ORDER_ID)
        assert handle.task_submit_result()

    @pytest.mark.dependency(name="cancel_apply")
    def test_013(self, drivers):
        """WEB-国际机票--预订取消"""
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        BOOK = IntFlightPage(drivers)
        BOOK.generate_order()
        ORDER_ID = BOOK.build_order_id()
        BOOK.to_order_list()
        BOOK.go_order_detail(ORDER_ID)
        BOOK.cancel_order()

    @pytest.mark.dependency(depends=["cancel_apply"])
    def test_014(self, drivers):
        """WEB-国际机票--完成预订取消任务"""
        AdminLogin(drivers).admin_sign()
        handle = IntFlightOrderHandlePage(drivers)
        handle.cancel_order(ORDER_ID)
        assert handle.task_submit_result()

if __name__ == '__main__':
    pytest.main(['testcase/test_07_web_iflight.py'])

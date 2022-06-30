import pytest
from common.admininthotel import AdminIntHotel
from common.customerlogin import CustomerLogin
from projects.web_uitest.PageObject.WebObject.web_ihotelpage import IntHotelTPage

ORDER_ID = ""

class TestIntHotel:

    def book_int_hotel(self, drivers):
        """预订国际酒店"""
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        int_hotel = IntHotelTPage(drivers)
        assert int_hotel.book_int_hotel(), "预订酒店失败"
        int_hotel.click_view_book_order()
        ORDER_ID = int_hotel.get_order_id()
        return True

    @pytest.mark.dependency(name='book')
    def test_001(self, drivers):
        """WEB-国际酒店--预订"""
        assert self.book_int_hotel(drivers)

    @pytest.mark.dependency(name="confirm", depends=["book"])
    def test_002(self, drivers):
        """WEB-国际酒店--完成订房"""
        assert AdminIntHotel().reservation_confirmation(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["confirm"], name="all_return1")
    def test_003_01(self, drivers):
        """WEB-国际酒店--全部退订-提交退订申请"""
        CustomerLogin(drivers).customer_login()
        int_hotel = IntHotelTPage(drivers)
        int_hotel.all_cancel()
        assert "退订申请已提交" in int_hotel.get_cancel_apply_result()

    @pytest.mark.dependency(depends=["all_return1"])
    def test_003_02(self, drivers):
        """WEB-国际酒店--全部退订-完成退订任务"""
        assert AdminIntHotel().all_cancel_confirm(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["confirm"], name="partial_return1")
    def test_004_01(self, drivers):
        """WEB-国际酒店--部分退订-预订酒店"""
        self.book_int_hotel(drivers)
        assert AdminIntHotel().reservation_confirmation(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["partial_return1"], name="partial_return2")
    def test_004_02(self, drivers):
        """WEB-国际酒店--部分退订-提交退订申请"""
        CustomerLogin(drivers).customer_login()
        int_hotel = IntHotelTPage(drivers)
        int_hotel.partial_cancel()
        assert "退订申请已提交" in int_hotel.get_cancel_apply_result()

    @pytest.mark.dependency(depends=["partial_return2"])
    def test_004_03(self, drivers):
        """WEB-国际酒店--部分退订-完成退订任务"""
        assert AdminIntHotel().partial_cancel_confirm(drivers, ORDER_ID)

    def test_005(self, drivers):
        """WEB-国际酒店--取消订单"""
        CustomerLogin(drivers).customer_login()
        int_hotel = IntHotelTPage(drivers)
        int_hotel.build_int_hotel_order()
        int_hotel.to_int_hotel_orders()
        int_hotel.cancel_order()
        assert "已取消" in int_hotel.get_order_status()

if __name__ == '__main__':
    pytest.main(['testcase/test_08_web_ihotel.py'])




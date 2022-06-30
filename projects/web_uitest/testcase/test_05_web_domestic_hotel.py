import pytest
from common.adminhotel import AdminHotel
from common.customerlogin import CustomerLogin
from projects.web_uitest.PageObject.WebObject.web_domestichotelpage import DomesticHotelTPage

ORDER_ID = ""

class TestDomesticHotel:

    def book_domestic_hotel(self, drivers):
        """预订国内酒店"""
        global ORDER_ID
        CustomerLogin(drivers).customer_login()
        domestic_hotel = DomesticHotelTPage(drivers)
        assert domestic_hotel.book_domestic_hotel()
        ORDER_ID = domestic_hotel.get_order_id()

    @pytest.mark.dependency(name='book')
    def test_001(self, drivers):
        """WEB-国内酒店--预订"""
        self.book_domestic_hotel(drivers)
        domestic_hotel = DomesticHotelTPage(drivers)
        assert "付款成功" in domestic_hotel.get_pay_status()

    @pytest.mark.dependency(name="confirm", depends=["book"])
    def test_002(self, drivers):
        """WEB-国内酒店--完成订房"""
        assert AdminHotel().reservation_confirmation(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["confirm"], name="partial_return1")
    def test_003_01(self, drivers):
        """WEB-国内酒店--全部退订-提交退订申请"""
        CustomerLogin(drivers).customer_login()
        domestic_hotel = DomesticHotelTPage(drivers)
        domestic_hotel.all_cancel()
        assert "退订申请已提交" in domestic_hotel.get_cancel_apply_result()

    @pytest.mark.dependency(depends=["partial_return1"])
    def test_003_02(self, drivers):
        """WEB-国内酒店--全部退订-完成退订任务"""
        assert AdminHotel().all_cancel_confirm(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["confirm"], name="book1")
    def test_004_01(self, drivers):
        """WEB-国内酒店--部分退订-预定酒店"""
        self.book_domestic_hotel(drivers)
        assert AdminHotel().reservation_confirmation(drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["book1"], name="return_apply1")
    def test_004_02(self, drivers):
        """WEB-国内酒店--部分退订-提交退订申请"""
        CustomerLogin(drivers).customer_login()
        domestic_hotel = DomesticHotelTPage(drivers)
        domestic_hotel.partial_cancel()
        assert "退订申请已提交" in domestic_hotel.get_cancel_apply_result()

    @pytest.mark.dependency(depends=["return_apply1"])
    def test_004_03(self, drivers):
        """WEB-国内酒店--部分退订-完成退订任务"""
        assert AdminHotel().partial_cancel_confirm(drivers, ORDER_ID)

    def test_005(self, drivers):
        """WEB-国内酒店--订单取消"""
        CustomerLogin(drivers).customer_login()
        domestic_hotel = DomesticHotelTPage(drivers)
        domestic_hotel.build_hotel_order()
        domestic_hotel.cancel_order()
        assert "已取消" in domestic_hotel.get_order_status()

if __name__ == '__main__':
    pytest.main(['testcase/test_05_web_domestic_hotel.py'])


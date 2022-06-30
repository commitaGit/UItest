import pytest
from app_uitest.PageObject.AppObject.app_domestichotelpage import AppDomesticHotelTPage


class TestAppDomesticHotel:

    @pytest.mark.dependency(name="book")
    def test_001(self, app_drivers):
        """APP-国内酒店预订"""
        domestic_hotel = AppDomesticHotelTPage(app_drivers)
        domestic_hotel.launch_app()
        assert domestic_hotel.book_domestic_hotel("深圳")
        assert "支付成功" in domestic_hotel.get_pay_status()

    @pytest.mark.dependency(depends=["book"])
    def test_002(self, app_drivers):
        """APP--国内酒店提交全部退订申请"""
        domestic_hotel = AppDomesticHotelTPage(app_drivers)
        domestic_hotel.click_view_book_order()
        assert "提交成功" in domestic_hotel.all_cancel()

    @pytest.mark.dependency(depends=["book"])
    def test_003(self, app_drivers):
        """APP--国内酒店提交部分退订申请"""
        domestic_hotel = AppDomesticHotelTPage(app_drivers)
        domestic_hotel.launch_app()
        assert domestic_hotel.book_domestic_hotel("深圳")
        domestic_hotel.click_view_book_order()
        assert "提交成功" in domestic_hotel.part_cancel()

if __name__ == '__main__':
    pytest.main(['testcase/test_04_app_domestichotel.py'])
    pass


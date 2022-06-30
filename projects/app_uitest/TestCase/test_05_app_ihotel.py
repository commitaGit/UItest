import pytest
from app_uitest.PageObject.AppObject.app_ihotelpage import AppIHotelTPage


class TestAppDomesticHotel:

    @pytest.mark.dependency(name="book")
    def test_001(self, app_drivers):
        """APP-国际酒店预订"""
        domestic_hotel = AppIHotelTPage(app_drivers)
        domestic_hotel.launch_app()
        assert domestic_hotel.book_ihotel("曼谷")
        assert "支付成功" in domestic_hotel.get_pay_status()

    @pytest.mark.dependency(depends=["book"])
    def test_002(self, app_drivers):
        """APP--国际酒店提交全部退订申请"""
        domestic_hotel = AppIHotelTPage(app_drivers)
        domestic_hotel.click_view_book_order()
        assert "成功" in domestic_hotel.all_cancel()

    @pytest.mark.dependency(depends=["book"])
    def test_003(self, app_drivers):
        """APP--国际酒店提交部分退订申请"""
        domestic_hotel = AppIHotelTPage(app_drivers)
        domestic_hotel.launch_app()
        assert domestic_hotel.book_ihotel("曼谷")
        domestic_hotel.click_view_book_order()
        assert "成功" in domestic_hotel.part_cancel()

if __name__ == '__main__':
    pytest.main(['testcase/test_05_app_ihotel.py'])
    pass


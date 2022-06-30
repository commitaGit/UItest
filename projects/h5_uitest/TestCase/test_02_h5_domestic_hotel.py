import pytest
from h5_uitest.PageObject.WebObject.h5_domestichotelpage import DomesticHotelTPage
from h5_uitest.PageObject.WebObject.web_multiplesearchpage import MultipleSearchPage
from h5_uitest.PageObject.WebObject.web_domestichotelhandlepage import DomesticHotelOrderHandlePage
from time import sleep

ORDER_ID = ""

class TestDomesticHotel:

    def book_domestic_hotel(self, drivers):
        """预订国内酒店"""
        global ORDER_ID
        domestic_hotel = DomesticHotelTPage(drivers)
        assert domestic_hotel.book_domestic_hotel()
        domestic_hotel.click_view_order()
        ORDER_ID = domestic_hotel.get_order_id()
        return True

    def search_order_status(self, admin_drivers, order_id, status):
        """查询订单状态"""
        search = MultipleSearchPage(admin_drivers)
        order_status = search.domestic_hotel_order_status(order_id)
        check = False
        n = 0
        while n < 15:
            if status in order_status:
                check = True
                break
            search.click_search()
            order_status = search.get_domestic_hotel_status()
            n += 1
            sleep(1)
        return check

    def part_cancel_room_confirm(self, admin_drivers, order_id): #TODO：部分退订失败无需查询状态，直接完成任务
        """国内酒店部分退房确认"""
        if not self.search_order_status(admin_drivers, order_id, "已退订"):
            return DomesticHotelOrderHandlePage(admin_drivers).part_cancel_room(order_id)
        return True

    def all_cancel_room_confirm(self, admin_drivers, order_id):
        """国内酒店全部退房确认"""
        if not self.search_order_status(admin_drivers, order_id, "已退订"):
            return DomesticHotelOrderHandlePage(admin_drivers).all_cancel_room(order_id)
        return True

    def reservation_confirmation(self, admin_drivers, order_id):
        """国内酒店订房确认"""
        if not self.search_order_status(admin_drivers, order_id, "已确认"):
            return DomesticHotelOrderHandlePage(admin_drivers).reservation_confirm(order_id)
        return True

    @pytest.mark.dependency(name='book')
    def test_001(self, drivers):
        """WEB-国内酒店--预订"""
        assert self.book_domestic_hotel(drivers)

    @pytest.mark.dependency(name="confirm", depends=["book"])
    def test_002(self, admin_drivers):
        """WEB-国内酒店--完成订房"""
        assert self.reservation_confirmation(admin_drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["confirm"], name="partial_return1")
    def test_003_01(self, drivers):
        """WEB-国内酒店--全部退订-提交退订申请"""
        global ORDER_ID
        domestic_hotel = DomesticHotelTPage(drivers)
        ORDER_ID =  domestic_hotel.all_cancel()

    @pytest.mark.dependency(depends=["partial_return1"])
    def test_003_02(self, admin_drivers):
        """WEB-国内酒店--全部退订-完成退订任务"""
        assert self.all_cancel_room_confirm(admin_drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["confirm"], name="book1")
    def test_004_01(self, drivers, admin_drivers):
        """WEB-国内酒店--部分退订-预定酒店"""
        assert self.book_domestic_hotel(drivers)
        assert self.reservation_confirmation(admin_drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["book1"], name="return_apply1")
    def test_004_02(self, drivers): # TODO：部分退订申请，提交后却是全部退订申请
        """WEB-国内酒店--部分退订-提交退订申请"""
        global ORDER_ID
        domestic_hotel = DomesticHotelTPage(drivers)
        ORDER_ID = domestic_hotel.partial_cancel()

    @pytest.mark.dependency(depends=["return_apply1"])
    def test_004_03(self, admin_drivers):
        """WEB-国内酒店--部分退订-完成退订任务"""
        assert self.part_cancel_room_confirm(admin_drivers, ORDER_ID)

    def test_005(self, drivers):
        """WEB-国内酒店--订单取消"""
        int_hotel = DomesticHotelTPage(drivers)
        int_hotel.build_hotel_order()
        assert "提交成功" in int_hotel.cancel_order()

if __name__ == '__main__':
    pytest.main(['testcase/test_02_h5_domestic_hotel.py'])


import pytest
from h5_uitest.PageObject.WebObject.web_ihotelorderhandlepage import IntHotelOrderHandlePage
from h5_uitest.PageObject.WebObject.h5_ihotelpage import IntHotelTPage
from h5_uitest.PageObject.WebObject.web_multiplesearchpage import MultipleSearchPage
from time import sleep

ORDER_ID = ""

class TestIntHotel:

    def book_int_hotel(self, drivers):
        """预订国际酒店"""
        global ORDER_ID
        int_hotel = IntHotelTPage(drivers)
        assert int_hotel.book_int_hotel()
        int_hotel.click_view_book_order()
        ORDER_ID = int_hotel.get_order_id()
        return True

    def search_order_status(self, admin_drivers, order_id, status):
        """查询订单状态"""
        search = MultipleSearchPage(admin_drivers)
        order_status = search.ihotel_order_status(order_id)
        check = False
        n = 0
        while n < 15:
            if status in order_status:
                check = True
                break
            search.click_search()
            order_status = search.ihotel_status()
            n += 1
            sleep(0.5)
        return check

    def part_cancel_room_confirm(self, admin_drivers, order_id):
        """国际酒店部分退房确认"""
        assert "任务成功" in IntHotelOrderHandlePage(admin_drivers).cancel_room(order_id)
        return True

    def all_cancel_room_confirm(self, admin_drivers, order_id):
        """国际酒店全部退房确认"""
        if not self.search_order_status(admin_drivers, order_id, "已退订"):
            assert "任务成功" in IntHotelOrderHandlePage(admin_drivers).cancel_room(order_id)
        return True

    def reservation_confirmation(self, admin_drivers, order_id):
        """国际酒店订房确认"""
        if not self.search_order_status(admin_drivers, order_id, "已确认"):
            assert "订房成功" in IntHotelOrderHandlePage(admin_drivers).book_room(order_id)
        return True

    @pytest.mark.dependency(name='book')
    def test_001(self, drivers):
        """WEB-国际酒店--预订"""
        assert self.book_int_hotel(drivers)

    @pytest.mark.dependency(name="confirm", depends=["book"])
    def test_002(self, admin_drivers):
        """WEB-国际酒店--完成订房"""
        assert self.reservation_confirmation(admin_drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["confirm"], name="all_return1")
    def test_003_01(self, drivers):
        """WEB-国际酒店--全部退订-提交退订申请"""
        global ORDER_ID
        int_hotel = IntHotelTPage(drivers)
        ORDER_ID = int_hotel.all_cancel()

    @pytest.mark.dependency(depends=["all_return1"])
    def test_003_02(self, admin_drivers):
        """WEB-国际酒店--全部退订-完成退订任务"""
        assert self.all_cancel_room_confirm(admin_drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["confirm"], name="partial_return1")
    def test_004_01(self, drivers, admin_drivers):
        """WEB-国际酒店--部分退订-预订酒店"""
        self.book_int_hotel(drivers)
        assert self.reservation_confirmation(admin_drivers, ORDER_ID)

    @pytest.mark.dependency(depends=["partial_return1"], name="partial_return2")
    def test_004_02(self, drivers):
        """WEB-国际酒店--部分退订-提交退订申请"""
        global ORDER_ID
        int_hotel = IntHotelTPage(drivers)
        ORDER_ID = int_hotel.partial_cancel()

    @pytest.mark.dependency(depends=["partial_return2"])
    def test_004_03(self, admin_drivers):
        """WEB-国际酒店--部分退订-完成退订任务"""
        assert self.part_cancel_room_confirm(admin_drivers, ORDER_ID)

    def test_005(self, drivers):
        """WEB-国际酒店--取消订单"""
        int_hotel = IntHotelTPage(drivers)
        int_hotel.build_int_hotel_order()
        assert "已取消" in int_hotel.cancel_order()

if __name__ == '__main__':
    pytest.main(['testcase/test_03_h5_ihotel.py'])




from projects.web_uitest.PageObject.WebObject.web_ihotelorderhandlepage import IntHotelOrderHandlePage
from projects.web_uitest.PageObject.WebObject.web_multiplesearchpage import MultipleSearchPage
from common.adminlogin import AdminLogin
from time import sleep

class AdminIntHotel:
    """国际酒店后台操作类"""

    def search_order_status(self, drivers, order_id, status):
        """查询订单状态"""
        AdminLogin(drivers).admin_sign()
        search = MultipleSearchPage(drivers)
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

    def partial_cancel_confirm(self, drivers, order_id):
        """国际酒店部分退房确认"""
        AdminLogin(drivers).admin_sign()
        assert "任务成功" in IntHotelOrderHandlePage(drivers).cancel_room(order_id)
        return True

    def all_cancel_confirm(self, drivers, order_id):
        """国际酒店全部退房确认"""
        if not self.search_order_status(drivers, order_id, "已退订"):
            assert "任务成功" in IntHotelOrderHandlePage(drivers).cancel_room(order_id)
        return True

    def reservation_confirmation(self, drivers, order_id):
        """国际酒店订房确认"""
        if not self.search_order_status(drivers, order_id, "已确认"):
            assert "订房成功" in IntHotelOrderHandlePage(drivers).book_room(order_id)
        return True

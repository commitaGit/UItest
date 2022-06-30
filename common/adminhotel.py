from common.adminlogin import AdminLogin
from projects.web_uitest.PageObject.WebObject.web_multiplesearchpage import MultipleSearchPage
from projects.web_uitest.PageObject.WebObject.web_domestichotelhandlepage import DomesticHotelOrderHandlePage
from time import sleep


class AdminHotel:
    """后台国内酒店操作类"""

    def search_order_status(self, drivers, order_id, status):
        """查询订单状态"""
        AdminLogin(drivers).admin_sign()
        search = MultipleSearchPage(drivers)
        order_status = search.domestic_hotel_order_status(order_id)
        check = False
        n = 0
        while n < 20:
            if status in order_status:
                check = True
                break
            search.click_search()
            order_status = search.get_domestic_hotel_status()
            n += 1
            sleep(1)
        return check

    def partial_cancel_confirm(self, drivers, order_id):
        """国内酒店部分退房确认"""
        AdminLogin(drivers).admin_sign()
        return DomesticHotelOrderHandlePage(drivers).part_cancel_room(order_id)

    def all_cancel_confirm(self, drivers, order_id):
        """国内酒店全部退房确认"""
        if not self.search_order_status(drivers, order_id, "已退订"):
            return DomesticHotelOrderHandlePage(drivers).all_cancel_room(order_id)
        return True

    def reservation_confirmation(self, drivers, order_id):
        """国内酒店订房确认"""
        if not self.search_order_status(drivers, order_id, "已确认"):
            return DomesticHotelOrderHandlePage(drivers).reservation_confirm(order_id)
        return True

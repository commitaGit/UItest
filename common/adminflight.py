from projects.web_uitest.PageObject.WebObject.web_systemmanagepage import FlightTestStubPage
from projects.web_uitest.PageObject.WebObject.web_multiplesearchpage import MultipleSearchPage
from projects.web_uitest.PageObject.WebObject.web_flightorderhandlepage import FlightOrderHandlePage
from time import sleep
from common.adminlogin import AdminLogin


class AdminFlight:
    """后台国内机票操作类"""

    def flight_stub(self, drivers):
        """国内机票测试桩全开启为成功"""
        login_result = AdminLogin(drivers).admin_sign()
        if not login_result:
            return False
        FlightTestStubPage(drivers).flight_stub_setting()

    def flight_ticket_confirm(self, drivers, order_id):
        """单程国内机票出票"""
        AdminLogin(drivers).admin_sign()
        order_status = self.search_order_status(drivers, order_id)
        n = 0
        while n < 15:
            if order_status == "已出票":
                break
            order_status = MultipleSearchPage(drivers).get_order_status()
            n += 1
            sleep(0.5)
        if order_status != "已出票":
            return FlightOrderHandlePage(drivers).ticket_confirm(order_id, "出票")
        return True

    def round_trip_ticket_confirm(self, drivers, order_id):
        """往返国内机票出票"""
        AdminLogin(drivers).admin_sign()
        order_status = MultipleSearchPage(drivers).round_trip_flight_status(order_id)
        n = 0
        while n < 10:
            if order_status[0] == "已出票" and order_status[1] == "已出票":
                break
            order_status = MultipleSearchPage(drivers).get_two_order_status()
            n += 1
            sleep(0.5)
        if (order_status[0] != "已出票") or (order_status[1] != "已出票"):
            return FlightOrderHandlePage(drivers).round_trip_ticket_confirm(order_id, "出票")
        return True

    def search_order_status(self, drivers, order_id):
        """后台综合查询中查询订单状态"""
        search = MultipleSearchPage(drivers)
        search.flight()
        search.order_id_search(order_id)
        return search.get_order_status()

    def change_offer(self, drivers, order_id):
        """"完成改签报价任务"""
        AdminLogin(drivers).admin_sign()
        change_offer = FlightOrderHandlePage(drivers)
        assert change_offer.change_offer(order_id), "完成改签报价任务失败"
        return change_offer.task_submit_result()

    def change_confirm(self, drivers, order_id):
        """完成改签确认任务"""
        AdminLogin(drivers).admin_sign()
        change = FlightOrderHandlePage(drivers)
        assert change.change_confirm(order_id), "完成改签确认任务失败"
        return change.task_submit_result()

    def return_confirm(self, drivers, order_id):
        """完成退票确认任务"""
        AdminLogin(drivers).admin_sign()
        return_confirm = FlightOrderHandlePage(drivers)
        assert return_confirm.return_confirm(order_id), "完成退票任务失败"
        return return_confirm.task_submit_result()
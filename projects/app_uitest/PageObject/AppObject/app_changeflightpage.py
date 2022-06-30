from page.apppage import AppPage, sleep
from common.readelement import Element
from utils.logger import log

changeflight = Element('app', 'app_flightchange')

class AppChangeFlight(AppPage):
    """app改签国内机票类"""

    def click_change_button(self):
        """点击改签"""
        log.info("点击改签按钮")
        self.swipe_down()
        self.is_click(changeflight["改签"])

    def choose_passenger(self):
        """选择乘机人"""
        log.info("选择乘机人")
        self.is_click(changeflight["选乘机人"])
        self.is_click(changeflight["下一步"])
        # sleep()

    def choose_route(self):
        """选择行程"""
        log.info("选择行程")
        self.is_click(changeflight["下一步"])
        # sleep()

    def choose_departure_date(self):
        """选择出发时间"""
        log.info("选择出发时间")
        self.is_click(changeflight["出发时间"])
        self.find_elements(changeflight["选中出发时间"])[1].click()
        # sleep()

    def click_search(self):
        """"点击查询"""
        log.info("点击查询")
        self.is_click(changeflight["查询"])
        # sleep(5)

    def choose_flight(self):
        """选中航班"""
        log.info("选中第一个航班")
        self.is_click(changeflight["选中航班"])
        # sleep(2)

    def change_confirm(self):
        """点击改签按钮"""
        log.info("点击确认改签")
        self.is_click(changeflight["改签按钮"])
        # sleep()
        self.is_click(changeflight["确认改签"])
        # sleep(6)

    def get_order_status(self):
        """获取订单状态"""
        log.info("进入订单详情获取订单状态")
        self.is_click(changeflight["查看订单"])
        # sleep()
        return self.element_text(changeflight["订单状态"])


if __name__ == "__maim__":
    pass

from page.webpage import WebPage
from utils.logger import log
from common.readelement import Element

search = Element('web', 'web_multiplesearch')

class MultipleSearchPage(WebPage):
    """后台综合查询类"""

    def click_multiple_search(self):
        log.info("点击综合查询")
        self.js_click(search["综合查询"])

    def flight(self):
        log.info("到国内机票查询页面")
        self.click_multiple_search()
        self.js_click(search["国内机票"])

    def order_id_search(self, order_id):
        log.info("输入查询订单号：{0}".format(order_id))
        self.input_text(search["订单号"], order_id)

    def click_search(self):
        log.info("点击查询")
        self.js_click(search["查询"])

    def get_order_status(self):
        log.info("获取机票订单状态")
        self.click_search()
        return self.element_text(search["机票订单状态"])

    def domestic_hotel(self):
        log.info("到国内酒店查询页面")
        self.click_multiple_search()
        self.js_click(search["国内酒店"])

    def domestic_hotel_order_status(self, order_id):
        log.info("获取国内酒店订单状态")
        self.domestic_hotel()
        self.hotel_order_id_search(order_id)
        self.click_search()
        return self.get_domestic_hotel_status()

    def get_domestic_hotel_status(self):
        log.info("获取国内酒店订单状态")
        return self.element_text(search["国内酒店订单状态"])

    def hotel_order_id_search(self, order_id):
        log.info("输入查询订单号：{0}".format(order_id))
        self.input_text(search["酒店订单号"], order_id)

    def iflight(self):
        log.info("到国际机票订单查询页面")
        self.click_multiple_search()
        self.js_click(search["国际机票"])

    def iflight_order_status(self, order_id):
        log.info("获取国际机票订单状态")
        self.iflight()
        self.order_id_search(order_id)
        self.click_search()
        return self.element_text(search["机票订单状态"])

    def ihotel(self):
        log.info("到国际酒店订单查询页面")
        self.click_multiple_search()
        self.js_click(search["国际酒店"])

    def ihotel_order_status(self, order_id):
        log.info("获取国际酒店订单状态")
        self.ihotel()
        self.input_text(search["国际酒店订单号"], order_id)
        self.click_search()
        return self.ihotel_status()

    def ihotel_status(self):
        return self.element_text(search["国际酒店订单状态"])

    def round_trip_flight_status(self, order_id):
        log.info("查询往返机票订单的订单状态")
        self.flight()
        self.order_id_search(order_id)
        return self.get_two_order_status()

    def get_two_order_status(self):
        log.info("获取两个订单的订单状态")
        self.click_search()
        status_one = self.get_order_status()
        status_two = self.element_text(search["机票订单状态二"])
        return status_one, status_two

if __name__ == "__maim__":
    pass

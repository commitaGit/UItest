from base.web_basepage import WebPage
from minium import logger as log

MULTIPLE_SEARCH = ("xpath", "//a[contains(text(), '综合查询')]")
FLIGHT = ("xpath", "//a[@href='/search/domestic-flight']")
ORDER_ID = ("name", "orderNoLike")
SEARCH_BUTTON = ("xpath", "//span[contains(text(),'查询')]/..")
FLIGHT_ORDER_STATUS = ("xpath", "//tbody/tr[1]/td[10]/span[2]/span[1]") # 第一个订单的订单状态
FLIGHT_ORDER_STATUS1 = ("xpath", "//tbody/tr[3]/td[10]/span[2]/span[1]") # 第二个订单的订单状态

DOMESTIC_HOTEL = ("xpath", "//a[@href='/search/domestic-hotel-orders']")
HOTEL_ORDER_ID = ("xpath", "//input[@formcontrolname='orderNoLike']")
HOTEL_ORDER_STATUS = ("xpath", "//tbody/tr[1]/td[8]/span[2]") # 有空格

INT_FLIGHT = ("xpath", "//a[@href='/search/intflight']")
INT_HOTEL = ("xpath", "//a[@href='/search/int-hotel']")
INT_HOTEL_STATUS = ("xpath", "//tbody/tr[1]/td[11]/span[2]")
INT_HOTEL_ORDER = ("xpath", "//input[@formcontrolname='orderNoLike']")


class MultipleSearchPage(WebPage):
    """后台综合查询类"""

    def click_multiple_search(self):
        log.info("点击综合查询")
        self.js_click(MULTIPLE_SEARCH)

    def flight(self):
        log.info("到国内机票查询页面")
        self.click_multiple_search()
        self.js_click(FLIGHT)

    def order_id_search(self, order_id):
        log.info("输入查询订单号：{0}".format(order_id))
        self.input_text(ORDER_ID, order_id)

    def click_search(self):
        log.info("点击查询")
        self.js_click(SEARCH_BUTTON)

    def get_order_status(self):
        log.info("获取机票订单状态")
        self.click_search()
        return self.element_text(FLIGHT_ORDER_STATUS)

    def domestic_hotel(self):
        log.info("到国内酒店查询页面")
        self.click_multiple_search()
        self.js_click(DOMESTIC_HOTEL)

    def domestic_hotel_order_status(self, order_id):
        log.info("获取国内酒店订单状态")
        self.domestic_hotel()
        self.hotel_order_id_search(order_id)
        self.click_search()
        return self.get_domestic_hotel_status()

    def get_domestic_hotel_status(self):
        log.info("获取国内酒店订单状态")
        return self.element_text(HOTEL_ORDER_STATUS)

    def hotel_order_id_search(self, order_id):
        log.info("输入查询订单号：{0}".format(order_id))
        self.input_text(HOTEL_ORDER_ID, order_id)

    def iflight(self):
        log.info("到国际机票订单查询页面")
        self.click_multiple_search()
        self.js_click(INT_FLIGHT)

    def iflight_order_status(self, order_id):
        log.info("获取国际机票订单状态")
        self.iflight()
        self.order_id_search(order_id)
        self.click_search()
        return self.element_text(FLIGHT_ORDER_STATUS)

    def ihotel(self):
        log.info("到国际酒店订单查询页面")
        self.click_multiple_search()
        self.js_click(INT_HOTEL)

    def ihotel_order_status(self, order_id):
        log.info("获取国际酒店订单状态")
        self.ihotel()
        self.input_text(INT_HOTEL_ORDER, order_id)
        self.click_search()
        return self.ihotel_status()

    def ihotel_status(self):
        return self.element_text(INT_HOTEL_STATUS)

    def round_trip_flight_status(self, order_id):
        log.info("查询往返机票订单的订单状态")
        self.flight()
        self.order_id_search(order_id)
        return self.get_two_order_status()

    def get_two_order_status(self):
        log.info("获取两个订单的订单状态")
        self.click_search()
        status_one = self.get_order_status()
        status_two = self.element_text(FLIGHT_ORDER_STATUS1)
        return status_one, status_two

if __name__ == "__maim__":
    pass

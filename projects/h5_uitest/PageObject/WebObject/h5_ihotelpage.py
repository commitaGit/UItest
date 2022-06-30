from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element
from common.readconfig import ini

int_hotel = Element('h5', 'h5_ihotel')
NAME = ini._get("STAFF", "IHOTELPERSON")


class IntHotelTPage(WebPage):
    """h5国际酒店类"""
    def click_int_hotel(self):
        log.info("点击国际酒店")
        self.refresh()
        sleep()
        self.js_click(int_hotel["酒店产品"])
        sleep()
        self.js_click(int_hotel["国际酒店"])

    def int_hotel_city(self, destination="曼谷"):
        log.info("酒店城市选择")
        self.js_click(int_hotel["目的地"])
        sleep(1)
        self.input_text(int_hotel["城市输入"], destination)
        self.js_click(int_hotel["第一个城市"])

    def choose_date(self):
        log.info("日期选择")
        self.js_click(int_hotel["日期选择"])
        self.js_click(int_hotel["入住日期"])
        self.js_click(int_hotel["离店日期"])

    def check_in_person(self):
        log.info("每间入住人数选择")
        self.js_click(int_hotel["每间入住人数"])
        sleep(0.5)
        self.find_elements(int_hotel["确定"])[-1].click()

    def click_search(self):
        log.info("点击查询")
        self.js_click(int_hotel["查询"])

    def click_first_hotel(self):
        log.info("点击第一个酒店")
        self.js_click(int_hotel["第一个酒店"])

    def click_book(self):
        log.info("预订第一个可退订房型")
        room_numbers = self.find_elements(int_hotel["房型数量"])
        for row_number in range(0, len(room_numbers)):  # 循环房型
            room_locator = (int_hotel["房型展开"][0], int_hotel["房型展开"][1].format(row_number+1))
            self.js_click(room_locator)
            book_locators = (int_hotel["可预订数量"][0], int_hotel["可预订数量"][1].format(row_number+1))
            book_numbers = self.find_elements(book_locators)
            for book_number in range(0, len(book_numbers)): # 循环每个房型可预订数量
                rule_locator = (int_hotel["退订规则"][0], int_hotel["退订规则"][1].format(row_number+1, book_number+1))
                return_rules = self.element_text(rule_locator)
                print("退订规则: ", return_rules)
                if "不可退订" not in return_rules:
                    book_locator = (int_hotel["预订按钮"][0], int_hotel["预订按钮"][1].format(row_number+1, book_number+1))
                    self.js_click(book_locator)
                    return True
        return False

    def choose_check_in_person(self, name=NAME):
        log.info("选中员工")
        self.is_click(int_hotel["入住人"])
        self.input_text(int_hotel["员工搜索"], name)
        sleep()
        self.is_click(int_hotel["第一个员工"])

    def click_submit(self):
        log.info("点击提交订单")
        self.roll_to_tagert(int_hotel["提交订单"])
        self.is_click(int_hotel["提交订单"])

    def credit_pay(self):
        log.info("授信支付")
        self.js_click(int_hotel["支付"])

    def click_view_book_order(self):
        log.info("点击查看订单详情")
        self.js_click(int_hotel["查看订单"])

    def get_order_id(self):  # 订单详情中获取
        log.info("获取订单号--订单详情中获取")
        return self.element_text(int_hotel["订单号"])[4:]

    def build_int_hotel_order(self):
        log.info("前台预订生成国际酒店订单")
        self.click_int_hotel()
        self.int_hotel_city()
        self.choose_date()
        self.check_in_person()
        self.click_search()
        self.click_first_hotel()
        if not self.click_book():
            return False
        self.choose_check_in_person()
        self.click_submit()
        assert self.element_exist(int_hotel["提交结果"])
        return True

    def book_int_hotel(self):
        log.info("预订国际酒店")
        if not self.build_int_hotel_order():
            return False
        self.credit_pay()
        return self.element_exist(int_hotel["支付成功"])

    def click_first_order(self):
        log.info("点击进入第一个已确认的订单详情")
        self.find_elements(int_hotel["列表已确认订单"])[0].click()
        sleep(0.5)

    def click_return_button(self):
        log.info("点击订单详情的退订按钮")
        self.js_click(int_hotel["退订"])

    def click_modify_cancel_info(self):
        log.info("点击修改退订信息")
        self.js_click(int_hotel["修改退订信息"])

    def uncheck_date(self):
        log.info("取消 第一个日期选中")
        self.js_click(int_hotel["第一个日期"])
        self.js_click(int_hotel["确定退订"])

    def click_next(self):
        log.info("点击下一步")
        self.js_click(int_hotel["下一步"])

    def click_confirm_return(self):
        log.info("点击 确认退订")
        self.js_click(int_hotel["确认退订"])

    def to_order_list(self):
        log.info("进入我的订单列表")
        self.refresh()
        sleep(1)
        log.info("点击 我的")
        self.js_click(int_hotel["我的"])
        log.info("点击 全部订单")
        self.js_click(int_hotel["全部订单"])

    def partial_cancel(self):
        log.info("提交部分退订申请")
        self.to_order_list()
        self.click_first_order()
        order_id = self.get_order_id()
        print("order_id",order_id)
        self.click_return_button()
        self.click_modify_cancel_info()
        self.uncheck_date()
        self.click_confirm_return()
        assert self.element_exist(int_hotel["退订成功"])
        return order_id

    def all_cancel(self):
        log.info("提交全部退订申请")
        self.to_order_list()
        self.click_first_order()
        order_id = self.get_order_id()
        self.click_return_button()
        self.click_next()
        self.click_confirm_return()
        assert self.element_exist(int_hotel["退订成功"])
        return order_id

    def cancel_order(self):
        log.info("订单详情中点击取消按钮取消订单")
        self.refresh()
        sleep()
        self.to_order_list()
        self.find_elements(int_hotel["列表待付款订单"])[0].click()
        sleep(0.5)
        self.js_click(int_hotel["取消订单"])
        self.js_click(int_hotel["确认取消"])
        return self.element_text(int_hotel["订单状态"])
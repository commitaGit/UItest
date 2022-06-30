import calendar
from datetime import datetime
from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element
from common.readconfig import ini

domestic_hotel = Element('h5', 'h5_domestichotel')
NAME = ini._get("STAFF", "HOTELPERSON")


class DomesticHotelTPage(WebPage):
    """h5国内酒店类"""
    def click_domestic_hotel(self):
        log.info("点击国内酒店")
        self.refresh()
        sleep()
        self.js_click(domestic_hotel["酒店产品"])

    def domestic_hotel_city(self, city_name):
        log.info("酒店城市选择")
        self.js_click(domestic_hotel["城市"])
        self.input_text(domestic_hotel["城市输入"], city_name)
        self.js_click(domestic_hotel["第一个城市"])

    def choose_date(self):
        log.info("日期选择")
        self.js_click(domestic_hotel["日期"])
        days = self.get_remain_days()
        if days < 5: # 当前月剩余天数少于5天，则预订下个月酒店
            self.js_click(domestic_hotel["下月入住日期"])
            self.js_click(domestic_hotel["下月离店日期"])
        else: # 如果当前月剩余天数不少于5天，则预订当前日后三天的两晚
            self.js_click(domestic_hotel["入住日期"])
            self.js_click(domestic_hotel["离店日期"])

    def get_remain_days(self):
        log.info("获取当前月份剩余天数")
        d = datetime.now()
        month_range = calendar.monthrange(d.year, d.month)[1]
        return month_range - d.day

    def click_search(self):
        log.info("点击 查询")
        self.js_click(domestic_hotel["查询"])

    def click_view_detail(self):
        log.info("点击 进入第一个酒店详情")
        self.js_click(domestic_hotel["第一个酒店"])

    def book_room(self):
        log.info("预订酒店")
        log.info("代理商B")
        self.is_click(domestic_hotel["代理商B"])
        if self.book_can_cancel_room():# 如果代理商A有可预订房型
            return True
        log.info("代理商A")
        self.is_click(domestic_hotel["代理商A"]) # 如果代理商A无可预订房型，则预订代理商B
        return self.book_can_cancel_room()

    def book_can_cancel_room(self):
        log.info("预订第一个可退订床型")
        eles = self.find_elements(domestic_hotel["可预订数量"])
        for room_number in range(0, len(eles)):
            rule_locator = (domestic_hotel["退订规则"][0], domestic_hotel["退订规则"][1].format(room_number+1))
            self.roll_to_tagert(rule_locator)
            return_rules = self.element_text(rule_locator)
            if ("限时退订" in return_rules) or ("免费退订" in return_rules):
                book_locator = (domestic_hotel["预订"][0], domestic_hotel["预订"][1].format(room_number+1))
                self.roll_to_tagert(book_locator)
                self.js_click(book_locator)
                return True
        return False

    def choose_check_in_person(self, name=NAME):
        log.info("选中员工")
        self.js_click(domestic_hotel["入住人选择"])
        sleep(0.5)
        self.input_text(domestic_hotel["员工搜索"], name)
        sleep(0.5)
        self.js_click(domestic_hotel["第一个员工"])
        self.js_click(domestic_hotel["确定"])

    def click_submit(self):
        log.info("点击提交订单")
        self.roll_to_tagert(domestic_hotel["提交订单"])
        self.is_click(domestic_hotel["提交订单"])

    def credit_pay(self):
        log.info("授信支付")
        self.js_click(domestic_hotel["支付"])

    def click_view_order(self):
        log.info("点击 查看订单")
        self.js_click(domestic_hotel["查看订单"])

    def get_order_id(self):
        log.info("获取订单号--订单详情页面")
        sleep(1)
        return self.element_text(domestic_hotel["订单号"])[4:]

    def build_hotel_order(self, city_name="深圳"):
        log.info("生成国内酒店订单")
        self.click_domestic_hotel()
        self.domestic_hotel_city(city_name)
        self.choose_date()
        self.click_search()
        self.click_view_detail()
        if not self.book_room():
            return False
        self.choose_check_in_person()
        self.click_submit()
        return self.element_exist(domestic_hotel["提交结果"])

    def book_domestic_hotel(self):
        log.info("预订国内酒店")
        if not self.build_hotel_order():
            return False
        self.credit_pay()
        return self.element_exist(domestic_hotel["支付成功"])

    def click_first_order(self):
        log.info("点击进入第一个已确认的订单详情")
        self.find_elements(domestic_hotel["列表已确认订单"])[0].click()

    def click_cancel_button(self):
        log.info("点击订单详情的退订按钮")
        self.js_click(domestic_hotel["退订"])

    def click_modify_cancel_info(self):
        log.info("点击修改退订信息")
        self.js_click(domestic_hotel["修改退订信息"])

    def uncheck_date(self):
        log.info("取消 第一个日期选中")
        self.js_click(domestic_hotel["第一个日期"])
        sleep(0.3)

    def click_next(self):
        log.info("点击下一步")
        self.js_click(domestic_hotel["下一步"])

    def to_order_list(self):
        log.info("进入我的订单列表")
        self.refresh()
        sleep(1)
        log.info("点击 我的")
        self.js_click(domestic_hotel["我的"])
        log.info("点击 全部订单")
        self.js_click(domestic_hotel["全部订单"])

    def partial_cancel(self):
        log.info("提交部分退订申请")
        self.to_order_list()
        self.click_first_order()
        order_id = self.get_order_id()
        self.click_cancel_button()
        self.click_modify_cancel_info()
        self.uncheck_date()
        self.click_next()
        assert self.element_exist(domestic_hotel["提交成功"])
        return order_id

    def all_cancel(self):
        log.info("提交全部退订申请")
        self.to_order_list()
        self.click_first_order()
        order_id = self.get_order_id()
        self.click_cancel_button()
        self.click_next()
        assert self.element_exist(domestic_hotel["提交成功"])
        return order_id

    def cancel_order(self):
        log.info("订单详情中点击取消按钮取消订单")
        self.refresh()
        sleep()
        self.to_order_list()
        self.find_elements(domestic_hotel["列表待付款订单"])[0].click()
        sleep(0.5)
        self.js_click(domestic_hotel["取消订单"])
        self.js_click(domestic_hotel["继续取消"])
        return self.element_text(domestic_hotel["取消结果"])

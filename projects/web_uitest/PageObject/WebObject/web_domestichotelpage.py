import datetime
import random
from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element
from common.readconfig import ini

domestic_hotel = Element('web', 'web_domestichotel')
NAME = ini._get("STAFF", "HOTELPERSON")


class DomesticHotelTPage(WebPage):
    """国内酒店类"""
    def click_domestic_hotel(self):
        log.info("点击国内酒店")
        self.js_click(domestic_hotel["国内酒店"])

    def domestic_hotel_city(self):
        log.info("酒店城市选择")
        self.js_click(domestic_hotel["城市"])
        self.js_click(domestic_hotel["深圳"])

    def choose_date(self):
        log.info("日期选择")
        date_result = self.random_book_date()
        locator1 = (domestic_hotel["入住日期选择"][0], domestic_hotel["入住日期选择"][1].format(date_result[0]))
        locator2 = (domestic_hotel["离店日期选择"][0], domestic_hotel["离店日期选择"][1].format(date_result[2]))
        self.check_in_date(locator1, date_result[1])
        self.check_out_date(locator2)

    def check_in_date(self, locator, check):
        log.info("入住时间选择")
        eles = self.find_elements(domestic_hotel["入住日期"])
        eles[0].click()
        if check:
            self.js_click(domestic_hotel["下个月"])
        self.js_click(locator)

    def check_out_date(self, locator):
        log.info("离店时间选择")
        eles = self.find_elements(domestic_hotel["离店日期"])
        eles[0].click()
        self.js_click(locator)

    def random_book_date(self):
        """
        locator1:入住日期的title
        check1：入住日期是否当月
        locator2：离店日期的title
        check2：离店日期是否当月
        """
        log.info("生成随机日期")
        random_number = random.randint(2,20)
        locator1, check1 = self.get_date(random_number)
        locator2, check2 = self.get_date(random_number+2)
        return locator1, check1, locator2, check2

    def get_date(self, random_number):
        """
        check:若获取的月份是下个月，则返回1，若是当月，则返回0
        """
        log.info("获取日期")
        temp_date = datetime.datetime.now()
        cur_month = temp_date.strftime("%Y%m%d")[4:6]
        date = (temp_date + datetime.timedelta(days=+random_number)).strftime("%Y%m%d")
        month = date[4:6]
        check = int(month) - int(cur_month) # 判断是否为下个月，或是下个月，则需先点击日历的下个月
        if month[0] == '0':
            month = month[1]
        day = date[6:]
        if day[0] == '0':
            day = day[1]
        return "{0}年{1}月{2}日".format(date[:4],month,day), check

    def click_search(self):
        log.info("点击搜索")
        self.js_click(domestic_hotel["搜索"])

    def click_view_detail(self):
        log.info("点击查看详情")
        eles = self.find_elements(domestic_hotel["查看详情"])
        eles[0].click()
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])

    def click_book(self):
        log.info("预订第一个可退订床型")
        log.info("推荐产品")
        if self.book_can_cancel_room():# 如果推荐产品有可预订
            return True
        log.info("代理商A")
        self.is_click(domestic_hotel["代理商A"])
        if self.book_can_cancel_room():# 如果代理商A有可预订房型
            return True
        log.info("代理商B")
        self.is_click(domestic_hotel["代理商B"]) # 如果代理商A无可预订房型，则预订代理商B
        return self.book_can_cancel_room()

    def book_can_cancel_room(self):
        log.info("预订第一个可退订床型")
        bed_numbers = self.find_elements(domestic_hotel["床型数量"])
        for room_number in range(1, len(bed_numbers)+1):
            price_locator = (domestic_hotel["可预订价格数"][0], domestic_hotel["可预订价格数"][1].format(room_number))
            price_numbers = self.find_elements(price_locator)
            for bed_number in range(1, len(price_numbers)+1):
                if self.room_can_return(domestic_hotel["退订规则1"], room_number, bed_number):
                    self.click_book_button(domestic_hotel["预订按钮1"], room_number, bed_number)
                    return True
                if self.room_can_return(domestic_hotel["退订规则2"], room_number, bed_number):
                    self.click_book_button(domestic_hotel["预订按钮2"], room_number, bed_number)
                    return True
        return False

    def room_can_return(self, rule_locator, room_number, bed_number):
        log.info("判断酒店政策是否可退订")
        rule_locator = (rule_locator[0], rule_locator[1].format(room_number, bed_number))
        return_rule =self.element_text(rule_locator)
        if ("限时退订" in return_rule) or ("免费退订" in return_rule):
            return True
        return False

    def click_book_button(self, book_locator, room_number, bed_number):
        log.info("点击预订按钮")
        book_locator = (book_locator[0], book_locator[1].format(room_number, bed_number))
        self.roll_to_tagert(book_locator)
        self.is_click(book_locator)

    def choose_check_in_person(self, name=NAME):
        log.info("选中员工")
        self.js_click(domestic_hotel["姓名"])
        self.input_text(domestic_hotel["姓名"], name)
        sleep(0.5)
        self.js_click(domestic_hotel["感应员工信息"])

    def click_submit(self):
        log.info("点击提交订单")
        self.roll_to_tagert(domestic_hotel["提交订单"])
        self.js_click(domestic_hotel["提交订单"])

    def credit_pay(self):
        log.info("授信支付")
        self.js_click(domestic_hotel["授信支付"])

    def get_pay_status(self):
        log.info("获取支付结果")
        return self.element_text(domestic_hotel["支付结果"])

    def get_order_id(self):
        log.info("获取订单号--下单完成页面")
        return self.element_text(domestic_hotel["订单号"])

    def click_view_book_order(self):
        log.info("点击查看订单详情")
        self.js_click(domestic_hotel["查看订单详情"])
        self.refresh()

    def get_order_status(self):
        log.info("获取订单状态")
        return self.element_text(domestic_hotel["订单状态"])

    def build_hotel_order(self):
        log.info("生成国内酒店订单")
        self.click_domestic_hotel()
        self.domestic_hotel_city()
        self.choose_date()
        self.click_search()
        self.click_view_detail()
        if not self.click_book():
            return False
        self.choose_check_in_person()
        self.click_submit()
        self.find_element(domestic_hotel["提交成功"])
        return True

    def book_domestic_hotel(self):
        log.info("预订国内酒店")
        if not self.build_hotel_order():
            return False
        self.credit_pay()
        return True

    def click_cancel_button(self):
        log.info("点击订单列表的退订按钮")
        eles = self.find_elements(domestic_hotel["退订按钮"])
        eles[0].click()

    def click_modify_cancel_info(self):
        log.info("点击修改退订信息")
        self.js_click(domestic_hotel["修改退订信息"])

    def uncheck_date(self):
        log.info("取消部分日期选中")
        eles = self.find_elements(domestic_hotel["退订日期"])
        eles[-1].click()

    def click_next(self):
        log.info("点击下一步")
        self.js_click(domestic_hotel["下一步"])

    def click_confirm_next(self):
        log.info("点击 确定，下一步")
        self.js_click(domestic_hotel["确认下一步"])

    def choose_cancel_reason(self):
        log.info("选中退订原因")
        self.js_click(domestic_hotel["退订原因"])

    def click_cancel_submit(self):
        log.info("点击退订提交按钮")
        self.js_click(domestic_hotel["退订提交"])
        sleep()

    def get_cancel_apply_result(self):
        log.info("获取退订申请提交结果")
        return self.element_text(domestic_hotel["提交结果"])

    def to_domestic_hotel_orders(self):
        log.info("进入国内酒店订单列表")
        self.js_click(domestic_hotel["我的特航"])
        self.js_click(domestic_hotel["国内酒店订单"])

    def partial_cancel(self):
        log.info("提交部分退订申请")
        self.to_domestic_hotel_orders()
        self.click_cancel_button()
        self.click_modify_cancel_info()
        self.uncheck_date()
        self.click_confirm_next()
        self.choose_cancel_reason()
        self.click_cancel_submit()

    def all_cancel(self):
        log.info("提交全部退订申请")
        self.to_domestic_hotel_orders()
        self.click_cancel_button()
        self.click_next()
        self.choose_cancel_reason()
        self.click_cancel_submit()

    def cancel_order(self):
        log.info("进入订单详情点击取消按钮取消订单")
        self.to_domestic_hotel_orders()
        self.js_click(domestic_hotel["第一个订单号"])
        self.js_click(domestic_hotel["取消"])
        self.js_click(domestic_hotel["取消确认"])
        self.js_click(domestic_hotel["提示按钮"])

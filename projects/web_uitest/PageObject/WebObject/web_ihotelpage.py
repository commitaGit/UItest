import datetime
import random
from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element
from common.readconfig import ini

int_hotel = Element('web', 'web_ihotel')
NAME = ini._get("STAFF", "IHOTELPERSON")


class IntHotelTPage(WebPage):
    """前台国际酒店类"""
    def click_int_hotel(self):
        log.info("点击国际酒店")
        self.js_click(int_hotel["国际酒店"])

    def int_hotel_city(self):
        log.info("酒店城市选择")
        self.js_click(int_hotel["目的地"])
        self.js_click(int_hotel["曼谷"])

    def choose_date(self):
        log.info("日期选择")
        date_result = self.random_book_date()
        locator1 = (int_hotel["入住日期选择"][0], int_hotel["入住日期选择"][1].format(date_result[0]))
        locator2 = (int_hotel["离店日期选择"][0], int_hotel["离店日期选择"][1].format(date_result[2]))
        self.check_in_date(locator1, date_result[1])
        self.check_out_date(locator2)

    def check_in_date(self, locator, check):
        log.info("入住时间选择")
        eles = self.find_elements(int_hotel["入住日期"])
        eles[0].click()
        if check:
            self.js_click(int_hotel["下个月"])
        self.js_click(locator)

    def check_out_date(self, locator):
        log.info("离店时间选择")
        eles = self.find_elements(int_hotel["离店日期"])
        eles[1].click()
        self.js_click(locator)

    def random_book_date(self):
        """
        locator1:入住日期的title
        check1：入住日期是否当月
        locator2：离店日期的title
        check2：离店日期是否当月
        """
        log.info("生成随机日期")
        random_number = random.randint(10,30)
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
        self.js_click(int_hotel["搜索"])

    def click_view_detail(self):
        log.info("点击查看详情")
        eles = self.find_elements(int_hotel["查看详情"])
        eles[0].click()

    def click_book(self):
        log.info("预订第一个可退订房型")
        room_numbers = self.find_elements(int_hotel["房型数"])
        for room_number in range(2, len(room_numbers)):
            bed_locator = (int_hotel["床型数量"][0], int_hotel["床型数量"][1].format(room_number))
            bed_numbers = self.find_elements(bed_locator)
            for bed_number in range(0, len(bed_numbers)):
                rule_locator = (int_hotel["退订规则"][0], int_hotel["退订规则"][1].format(room_number, bed_number+1))
                return_rules = self.element_text(rule_locator)
                if "不可退订" not in return_rules:
                    book_locator = (int_hotel["预订"][0], int_hotel["预订"][1].format(room_number, bed_number+1))
                    self.js_click(book_locator)
                    return True
        return False

    def choose_check_in_person(self, name=NAME):
        log.info("选中员工")
        self.input_text(int_hotel["姓"], name)
        self.is_click(int_hotel["感应员工信息"])

    def click_submit(self):
        log.info("点击提交订单")
        self.roll_to_tagert(int_hotel["提交订单"])
        self.is_click(int_hotel["提交订单"])
        # try:
        #     self.js_click(int_hotel["继续预订"])
        # except:
        #     pass

    def credit_pay(self):
        log.info("授信支付")
        self.js_click(int_hotel["授信支付"])

    def get_pay_status(self):
        log.info("获取支付结果")
        return self.element_text(int_hotel["支付结果"])

    def click_view_book_order(self):
        log.info("点击查看订单详情")
        self.js_click(int_hotel["查看订单详情"])

    def get_order_id(self):  # 订单详情中获取
        log.info("获取订单号--订单详情中获取")
        return self.element_text(int_hotel["订单号"])

    def get_order_status(self):
        log.info("获取订单状态")
        return self.element_text(int_hotel["订单状态"])

    def build_int_hotel_order(self):
        log.info("前台预订生成国际酒店订单")
        self.click_int_hotel()
        self.int_hotel_city()
        self.choose_date()
        self.click_search()
        self.click_view_detail()
        if not self.click_book():
            return False
        self.choose_check_in_person()
        self.click_submit()
        self.find_element(int_hotel["授信支付"])
        return True

    def book_int_hotel(self):
        log.info("预订国际酒店")
        if not  self.build_int_hotel_order():
            return False
        self.credit_pay()
        return True

    def click_cancel_button(self):
        log.info("点击订单列表的退订按钮")
        eles = self.find_elements(int_hotel["退订按钮"])
        eles[0].click()

    def click_modify_cancel_info(self):
        log.info("点击修改退订信息")
        self.js_click(int_hotel["修改退订信息"])

    def uncheck_date(self):
        log.info("取消部分日期选中")
        eles = self.find_elements(int_hotel["退订日期"])
        eles[-1].click()

    def click_next(self):
        log.info("点击下一步")
        self.js_click(int_hotel["下一步"])

    def click_confirm_next(self):
        log.info("点击 确定，下一步")
        self.js_click(int_hotel["确认下一步"])

    def choose_cancel_reason(self):
        log.info("选中退订原因")
        self.js_click(int_hotel["退订原因"])

    def click_cancel_submit(self):
        log.info("点击退订提交按钮")
        self.js_click(int_hotel["退订提交"])
        sleep()

    def get_cancel_apply_result(self):
        log.info("获取退订申请提交结果")
        return self.element_text(int_hotel["提交结果"])

    def to_int_hotel_orders(self):
        log.info("进入国际酒店订单列表")
        self.js_click(int_hotel["我的商旅"])
        self.js_click(int_hotel["国际酒店订单"])

    def partial_cancel(self):
        log.info("提交部分退订申请")
        self.to_int_hotel_orders()
        self.click_cancel_button()
        self.click_modify_cancel_info()
        self.uncheck_date()
        self.click_confirm_next()
        self.choose_cancel_reason()
        self.click_cancel_submit()

    def all_cancel(self):
        log.info("提交全部退订申请")
        self.to_int_hotel_orders()
        self.click_cancel_button()
        self.click_next()
        self.choose_cancel_reason()
        self.click_cancel_submit()

    def cancel_order(self):
        log.info("订单详情中点击取消按钮取消订单")
        self.js_click(int_hotel["第一个订单号"])
        self.js_click(int_hotel["取消"])
        self.js_click(int_hotel["取消确认"])
        self.js_click(int_hotel["提示确定"])
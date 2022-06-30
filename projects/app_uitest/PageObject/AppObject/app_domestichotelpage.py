from page.apppage import AppPage, sleep
from utils.logger import log
from common.readelement import Element
from common.readconfig import ini

domestic_hotel = Element('app', 'app_domestichotel')
NAME = ini._get("STAFF", "HOTELPERSON")


class AppDomesticHotelTPage(AppPage):
    """APP国内酒店类"""
    def click_domestic_hotel(self):
        log.info("点击国内酒店")
        self.is_click(domestic_hotel["酒店"])

    def domestic_hotel_city(self, city):
        log.info("酒店城市选择")
        self.is_click(domestic_hotel["城市"])
        self.input_text(domestic_hotel["输入城市"], city)
        self.is_click(domestic_hotel["选中城市"])

    def choose_date(self):
        log.info("日期选择")
        self.is_click(domestic_hotel["时间"])
        self.is_click(domestic_hotel["开始时间"])
        self.is_click(domestic_hotel["结束时间"])

    def click_search(self):
        log.info("点击查询")
        self.is_click(domestic_hotel["查询"])
        sleep(3)

    def choose_hotel(self):
        log.info("选中酒店及房型")
        self.is_click(domestic_hotel["选中酒店"])
        sleep()
        self.is_click(domestic_hotel["房型"])

    def click_book(self):
        log.info("查看预订规则，并预订第一个可退订房间")
        eles = self.find_elements(domestic_hotel["可预订数量"])
        for row_number in range(2, len(eles)):
            rule_locator = (domestic_hotel["退订规则"][0], domestic_hotel["退订规则"][1].format(row_number))
            return_rules = self.element_text(rule_locator)
            if "限时退订" in return_rules:
                book_locator = (domestic_hotel["预订"][0], domestic_hotel["预订"][1].format(row_number))
                self.is_click(book_locator)
                return True
        return False

    def choose_check_in_person(self, name=NAME):
        log.info("选中入住人")
        self.is_click(domestic_hotel["入住人"])
        try:
            self.is_click(domestic_hotel["最近选择"])
        except:
            self.input_text(domestic_hotel["搜索员工"], name)
            self.is_click(domestic_hotel["选中员工"])
        self.is_click(domestic_hotel["确定"])

    def click_submit(self):
        log.info("点击提交订单")
        self.is_click(domestic_hotel["提交订单"])

    def credit_pay(self):
        log.info("授信支付")
        self.is_click(domestic_hotel["授信支付"])

    def get_pay_status(self):
        log.info("获取支付结果")
        return self.element_text(domestic_hotel["支付结果"])

    def click_view_book_order(self):
        log.info("点击查看订单详情")
        sleep(3)
        self.is_click(domestic_hotel["查看订单"])

    def book_domestic_hotel(self, city):
        log.info("预订国内酒店")
        self.click_domestic_hotel()
        self.domestic_hotel_city(city)
        self.choose_date()
        self.click_search()
        self.choose_hotel()
        if not self.click_book():
            return False
        self.choose_check_in_person()
        self.click_submit()
        self.credit_pay()
        return True

    def launch_app(self):
        log.info("重新打开APP")
        self.driver.launch_app()

    def click_cancel(self):
        log.info("点击订单详情的退订按钮")
        self.is_click(domestic_hotel["退订"])

    def click_next(self):
        log.info("点击下一步")
        self.is_click(domestic_hotel["下一步"])
        sleep()

    def get_cancel_apply_result(self):
        log.info("获取退票申请提交结果")
        return self.element_text(domestic_hotel["提交结果"])

    def all_cancel(self):
        log.info("提交全部退订申请")
        self.click_cancel()
        self.click_next()
        return self.get_cancel_apply_result()

    def part_cancel(self):
        log.info("提交部分退订申请")
        self.click_cancel()
        self.is_click(domestic_hotel["修改退订信息"])
        self.is_click(domestic_hotel["取消房间"])
        self.click_next()
        return self.get_cancel_apply_result()

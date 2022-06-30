from page.apppage import AppPage, sleep
from utils.logger import log
from common.readelement import Element
from common.readconfig import ini


ihotel = Element('app', 'app_ihotel')
NAME = ini._get("STAFF", "IHOTELPERSON")


class AppIHotelTPage(AppPage):
    """APP国际酒店类"""
    def click_ihotel(self):
        log.info("点击国际酒店")
        self.is_click(ihotel["酒店"])
        self.is_click(ihotel["国际酒店"])

    def ihotel_city(self, city):
        log.info("酒店城市选择")
        self.is_click(ihotel["城市"])
        sleep()
        self.input_text(ihotel["输入城市"], city)
        self.is_click(ihotel["选中城市"])

    def choose_date(self):
        log.info("日期选择")
        self.is_click(ihotel["时间"])
        x1 = 777/2160
        y1 = 3404/3840
        x2 = 1295/2160
        self.touch_location(x1, y1)
        self.touch_location(x2, y1)

    def choose_occupancy(self):
        log.info("每间入住人数")
        self.is_click(ihotel["每间人数"])
        self.is_click(ihotel["确定"])

    def click_search(self):
        log.info("点击查询")
        self.is_click(ihotel["查询"])
        sleep(3)

    def choose_hotel(self):
        log.info("选中酒店及房型")
        self.is_click(ihotel["选中酒店"])
        sleep()
        self.is_click(ihotel["第一个房型"])

    def click_book(self):
        log.info("查看预订规则，并预订第一个可退订房间")
        eles = self.find_elements(ihotel["可预订数量"])
        for row_number in range(2, len(eles)):
            rule_locator = (ihotel["预订规则"][0], ihotel["预订规则"][1].format(row_number))
            return_rules = self.element_text(rule_locator)
            if "不可退订" not in return_rules:
                book_locator = (ihotel["预订按钮"][0], ihotel["预订按钮"][1].format(row_number))
                self.is_click(book_locator)
                return True
        return False

    def choose_check_in_person(self, name=NAME):
        log.info("选中入住人")
        self.is_click(ihotel["入住人"])
        try:
            self.is_click(ihotel["最近选择"])
        except:
            self.input_text(ihotel["搜索员工"], name)
            self.is_click(ihotel["选中员工"])

    def click_submit(self):
        log.info("点击提交订单")
        self.is_click(ihotel["提交订单"])

    def credit_pay(self):
        log.info("授信支付")
        self.is_click(ihotel["授信支付"])

    def get_pay_status(self):
        log.info("获取支付结果")
        return self.element_text(ihotel["支付结果"])

    def click_view_book_order(self):
        log.info("点击查看订单详情")
        sleep(3)
        self.is_click(ihotel["查看订单"])

    def book_ihotel(self, city):
        log.info("预订国际酒店")
        self.click_ihotel()
        self.ihotel_city(city)
        self.choose_occupancy()
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
        self.is_click(ihotel["退订"])

    def click_next(self):
        log.info("点击下一步")
        self.is_click(ihotel["下一步"])
        sleep()
        
    def click_confirm_return(self):
        log.info("点击确认退订")
        self.is_click(ihotel["确认退订"])

    def get_cancel_apply_result(self):
        log.info("获取退票申请提交结果")
        return self.element_text(ihotel["提交结果"])

    def all_cancel(self):
        log.info("提交全部退订申请")
        self.click_cancel()
        self.click_next()
        self.click_confirm_return()
        return self.get_cancel_apply_result()

    def part_cancel(self):
        log.info("提交部分退订申请")
        self.click_cancel()
        self.is_click(ihotel["修改退订信息"])
        self.is_click(ihotel["取消房间"])
        self.is_click(ihotel["确定退订"])
        self.click_confirm_return()
        return self.get_cancel_apply_result()

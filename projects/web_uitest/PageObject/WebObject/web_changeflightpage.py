import random
from page.webpage import WebPage, sleep
from common.readelement import Element
from utils.logger import log

change = Element('web', 'web_flightchange')

class ChangeFlightPage(WebPage):
    """国内机票改签申请提交类"""

    def click_my_travel(self):
        log.info("点击我的商旅")
        self.js_click(change["我的商旅"])

    def click_first_change(self):
        log.info("点击第一个改签按钮")
        self.js_click(change["改签按钮"])

    def click_next(self):
        log.info("点击 下一步")
        self.js_click(change["下一步"])

    def click_date(self):
        log.info("点击日期")
        self.find_elements(change["日期"])[0].click()
        self.js_click(change["下个月"])

    def pick_date(self):
        log.info("点击选中日期")
        self.js_click(self.ramdom_date(change["日期选择"]))

    def ramdom_date(self, locator):
        log.info("随机生成15-28的日期定位")
        day = random.randint(15,28)
        log.info("日期:{0}".format(day))
        return locator[0], locator[1].format(day)

    def choose_date(self):
        log.info("选中日期")
        self.click_date()
        self.pick_date()
        sleep()

    def click_search(self):
        log.info("点击搜索按钮")
        self.roll_to_tagert(change["搜索按钮"])
        self.js_click(change["搜索按钮"])

    def click_change(self):
        log.info("点击第一个航班的第一个可改签舱位")
        self.js_click(change["改签"])

    def click_confirm_change(self):
        log.info("点击确认改签")
        self.roll_to_tagert(change["确认改签"])
        self.js_click(change["确认改签"])

    def click_credit_pay(self): # 有差价才需支付
        log.info("点击授信支付的支付按钮")
        self.js_click(change["授信支付"])

    def get_pay_result(self):
        log.info("获取支付结果")
        return self.element_text(change["支付结果"]) # 订单支付完成

    def click_view_order(self):
        log.info("点击查看订单")
        self.js_click(change["查看订单"])

    def apply_status(self):
        log.info("获取改签申请提交状态")
        return self.element_text(change["申请提交状态"])

    def get_order_id(self):
        log.info("获取订单号")
        text = self.element_text(change["订单号"])
        return text[4:]

    def submit_change_apply(self):
        log.info("提交改签申请")
        self.click_my_travel()
        self.click_first_change()
        self.click_next()
        self.choose_date()
        self.click_search()
        self.click_change()
        self.click_confirm_change()
        apply_status = self.apply_status()
        self.click_view_order()
        order_id = self.get_order_id()
        return apply_status, order_id


if __name__ == "__maim__":
    pass

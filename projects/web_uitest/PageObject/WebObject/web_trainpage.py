import datetime
import random
from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element
from common.readconfig import ini

train = Element('web', 'web_train')
NAME = ini._get("STAFF", "TRAINPASSENGER")

class TrainPage(WebPage):
    """火车票类"""

    def random_book_date(self):
        temp_date = datetime.datetime.now()
        date = (temp_date + datetime.timedelta(days=+random.randint(2,7))).strftime("%Y%m%d")
        year = date[:4]
        month = date[4:6]
        if month[0] == '0':
            month = month[1]
        day = date[6:]
        if day[0] == '0':
            day = day[1]
        return "{0}年{1}月{2}日".format(year, month, day)

    def click_train(self):
        log.info("点击火车票")
        self.js_click(train["火车票"])

    def departure_place(self):
        log.info("出发地选择")
        self.find_elements(train["出发地"])[0].click()
        self.js_click(train["广州"])

    def arrival_place(self):
        log.info("到达地选择")
        self.find_elements(train["出发地"])[1].click()
        self.js_click(train["深圳"])

    def choose_date(self):
        log.info("日期选择")
        self.js_click(train["日期"])
        locator = (train["日期选择"][0], train["日期选择"][1].format(self.random_book_date()))
        self.js_click(locator)

    def click_search(self):
        log.info("点击搜索")
        self.js_click(train["搜索"])

    def click_book(self):
        log.info("预订第一个可预订车次")
        eles = self.find_elements(train["预订按钮"])
        for ele in eles:
            if not ele.get_attribute("disabled"):
                ele.click()
                break

    def choose_passenger(self, name=NAME):
        log.info("选中乘车人")
        self.input_text(train["姓名"], name)
        self.js_click(train["感应员工信息"])

    def click_direct_book(self):
        log.info("点击直接预订")
        self.roll_to_tagert(train["直接预订"])
        self.js_click(train["直接预订"])

    def credit_pay(self):
        log.info("授信支付")
        self.js_click(train["授信支付"])

    def get_pay_status(self):
        log.info("获取支付结果")
        return self.element_text(train["支付结果"])

    def click_view_book_order(self):
        log.info("点击查看订单")
        self.js_click(train["查看订单"])

    def get_order_status(self):
        log.info("获取订单状态")
        sleep(2)
        self.refresh()
        sleep()
        return self.element_text(train["订单状态"])

    def get_order_id(self):
        log.info("获取订单号")
        return self.element_text(train["订单号"])[4:]

    def submit_change_apply(self):
        log.info("提交改签申请")
        self.js_click(train["改签"])
        self.click_change()
        self.js_click(train["确认改签"])
        try:
            self.js_click(train["改签支付"])
        except:
            pass
        return self.element_text(train["改签申请提交结果"])

    def click_view_change_order(self):
        log.info("点击查看改签订单")
        self.js_click(train["查看改签订单"])
        self.refresh()

    def click_change(self):
        log.info("预订第一个可改签车次")
        eles = self.find_elements(train["改签按钮"])
        for ele in eles:
            if not ele.get_attribute("disabled"):
                ele.click()
                return True
        return False

    def submit_return_apply(self):
        log.info("提交退票申请")
        self.js_click(train["退票"])
        self.js_click(train["确认退票"])
        return self.element_text(train["退票申请提交结果"])

    def book_train(self):
        log.info("预订火车票")
        self.click_train()
        self.departure_place()
        self.arrival_place()
        self.choose_date()
        self.click_search()
        self.click_book()
        self.choose_passenger()
        self.click_direct_book()
        self.credit_pay()
        return self.get_pay_status()

    def click_view_return_order(self):
        log.info("点击查看退票订单")
        self.js_click(train["查看退票订单"])
        sleep(2)
        self.refresh()
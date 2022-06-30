import random
from page.webpage import WebPage, sleep
from common.readelement import Element
from faker import Faker
from utils.logger import log
from common.readconfig import ini

fake = Faker()
book = Element('web', 'web_iflight')
STAFF = ini._get("STAFF", "IFLIGHTPERSON")

class IntFlightPage(WebPage):
    """web国际机票类"""

    def click_iflight_product(self):
        """点击机票产品"""
        log.info("点击国际机票产品")
        self.js_click(book["国际机票"])
        sleep()

    def click_on_business(self):
        """点击因公"""
        log.info("点击因公")
        self.js_click(book["因公"])

    def click_on_personal(self):
        """点击因私"""
        log.info("点击因私")
        self.js_click(book["因私"])

    def input_departure_city(self, departure_city):
        """输入出发地"""
        log.info("输入出发地")
        eles = self.find_elements(book["出发地"])
        log.info("输入内容：{0}".format(departure_city))
        eles[0].send_keys(departure_city)

    def pick_departure_city(self):
        """选中出发地"""
        log.info("选中出发地")
        self.is_click(book["出发地选择"])

    def departure_city(self, departure_city):
        """输入并选中出发地"""
        log.info("输入并选中出发地")
        self.input_departure_city(departure_city)
        self.pick_departure_city()

    def input_arrive_city(self, arrive_city):
        """输入到达地"""
        log.info("输入到达地")
        eles = self.find_elements(book["到达地"])
        log.info("输入内容：{0}".format(arrive_city))
        eles[1].send_keys(arrive_city)

    def pick_arrive_city(self):
        """选中到达城市"""
        log.info("选中到达地")
        self.is_click(book["到达地选择"])

    def arrive_city(self, arrive_city):
        log.info("输入并选中到达")
        self.input_arrive_city(arrive_city)
        self.pick_arrive_city()

    def click_date(self):
        """点击日期"""
        log.info("点击日期")
        self.find_elements(book["出发日期"])[0].click()
        self.js_click(book["下个月"])

    def pick_date(self):
        """点击选中日期"""
        log.info("点击选中日期")
        self.js_click(self.random_date(book["日期选择"]))

    def random_date(self, locator):
        """日期生成随机日期"""
        day = random.randint(15,28)
        log.info("日期:{0}".format(day))
        return locator[0], locator[1].format(day)

    def choose_date(self):
        """选中日期"""
        log.info("选中日期")
        self.click_date()
        self.pick_date()
        sleep()

    def click_search(self):
        """点击查询"""
        log.info("点击查询")
        self.js_click(book["查询"])

    def click_book(self):
        """点击预订"""
        log.info("点击预订")
        eles = self.find_elements(book["预订"])
        eles[0].click()

    def input_staff_name(self):
        """输入员工姓名"""
        log.info("输入员工姓名")
        name_list = fake.name().split(" ")
        self.input_text(book["姓"], name_list[1])
        self.input_text(book["名"], name_list[0])

    def input_passport_number(self):
        log.info("输入护照号码")
        self.input_text(book["证件号"], "P{0}".format(random.randint(1000000, 9999999)))

    def choose_terminal_date(self):
        log.info("选择证件有效期")
        self.js_click(book["证件有效期"])
        self.js_click(book["下一年"])
        self.js_click(book["下一年"])
        self.js_click(book["选中有效期"])

    def choose_nationality(self):
        log.info("选择国际")
        self.js_click(book["国籍"])
        self.js_click(book["中国大陆"])

    def choose_staff_department(self):
        """选择员工部门"""
        log.info("选择员工部门")
        self.roll_to_tagert(book["费用部门"])
        self.js_click(book["费用部门"])
        self.js_click(book["选中部门"])

    def click_build_order(self):
        """点击生成订单"""
        log.info("点击提交订单订单")
        self.roll_to_tagert(book["提交订单"])
        self.is_click(book["提交订单"])

    def click_credit_pay(self):
        """点击授信支付"""
        log.info("点击授信支付的支付按钮")
        self.js_click(book["授信支付"])

    def get_pay_result(self):
        """获取支付结果"""
        log.info("获取支付结果")
        return self.element_text(book["支付结果"])

    def get_order_id(self):
        """获取订单号"""
        log.info("获取订单号")
        text = self.element_text(book["订单号"])
        return text[4:]

    def choose_staff(self, name=STAFF):
        log.info("输入并选中员工")
        self.input_text(book["姓"], name)
        self.is_click(book["选中员工"])

    def to_order_list(self):
        log.info("进入国际机票订单列表")
        self.js_click(book["我的特航"])
        self.js_click(book["国际机票订单列表"])

    def submit_change_apply(self):
        log.info("提交改签申请")
        self.to_order_list()
        eles = self.find_elements(book["改签"])
        eles[0].click()
        self.js_click(book["选择日期"])
        self.js_click(book["改签下个月"])
        self.js_click(self.random_date(book["具体日期选中"]))
        self.js_click(book["提交改签申请"])
        self.js_click(book["确认提交改签申请"])
        return self.element_text(book["改签申请提交结果"])

    def submit_return_apply(self):
        log.info("提交退票申请")
        self.to_order_list()
        eles = self.find_elements(book["退票"])
        eles[0].click()
        eles = self.find_elements(book["退票类型"])
        eles[0].click()
        self.js_click(book["提交退票申请"])
        self.js_click(book["确认提交退票申请"])
        return self.element_text(book["退票申请提交结果"])

    def get_change_order_id(self):
        log.info("获取生成的改签单的订单号")
        self.to_order_list()
        return self.element_text(book["第一个订单号"])[0:9]

    def generate_order(self, departure_city="香港", arrive_city="曼谷"):
        log.info("生成订单")
        self.click_iflight_product()
        self.departure_city(departure_city)
        self.arrive_city(arrive_city)
        self.choose_date()
        self.click_search()
        self.click_book()
        self.choose_staff()
        self.click_build_order()

    def build_order_id(self):
        log.info("订单生成页面订单号")
        return self.element_text(book["支付页面订单号"])

    def go_order_detail(self, order_id):
        log.info("点击订单号进入订单详情")
        locator = (book["点击订单号"][0], book["点击订单号"][1].format(order_id))
        self.js_click(locator)

    def cancel_order(self):
        log.info("在订单详情页点击取消按钮取消订单")
        self.js_click(book["取消"])
        self.js_click(book["取消确认"])

if __name__ == "__maim__":
    pass

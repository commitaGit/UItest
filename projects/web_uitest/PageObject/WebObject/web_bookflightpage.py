import random
import datetime
from page.webpage import WebPage, sleep
from common.readelement import Element
from utils.buildIDnumber import generate_id as ID
from faker import Faker
from utils.logger import log

fake = Faker(locale='zh_CN')
book = Element('web', 'web_flightbook')

class BookFlightPage(WebPage):
    """web预订国内机票类"""

    def click_flight_product(self):
        """点击机票产品"""
        log.info("点击机票产品")
        self.refresh()
        self.js_click(book["机票产品"])
        sleep()

    def click_one_way(self):
        """点击单程"""
        log.info("点击单程")
        self.js_click(book["单程"])

    def click_round_trip(self):
        """点击往返"""
        log.info("点击往返")
        self.js_click(book["往返"])

    def click_on_business(self):
        """点击因公"""
        log.info("点击因公")
        self.js_click(book["因公"])

    def click_on_personal(self):
        """点击因私"""
        log.info("点击因私")
        self.js_click(book["因私"])

    def input_departure_city(self, departure_city):
        """输入出发城市"""
        log.info("输入出发城市")
        eles = self.find_elements(book["出发城市"])
        log.info("输入内容：{0}".format(departure_city))
        eles[0].send_keys(departure_city)
        eles[0].click()

    def pick_departure_city(self):
        """选中出发城市"""
        log.info("选中出发城市")
        self.js_click(book["出发城市选择"])

    def departure_city(self, departure_city):
        """输入并选中出发城市"""
        log.info("输入并选中出发城市")
        self.input_departure_city(departure_city)
        self.pick_departure_city()

    def input_arrive_city(self, arrive_city):
        """输入到达城市"""
        log.info("输入到达城市")
        eles = self.find_elements(book["到达城市"])
        log.info("输入内容：{0}".format(arrive_city))
        eles[1].send_keys(arrive_city)
        eles[1].click()

    def pick_arrive_city(self):
        """选中到达城市"""
        log.info("选中到达城市")
        self.js_click(book["到达城市选择"])

    def arrive_city(self, arrive_city):
        log.info("输入并选中到达城市")
        self.input_arrive_city(arrive_city)
        self.pick_arrive_city()

    def click_date(self):
        """点击日期"""
        log.info("点击日期")
        self.find_elements(book["日期"])[0].click()

    def pick_date(self):
        """点击选中日期"""
        log.info("点击选中日期")
        locator = book["日期选择"]
        date_result = self.get_date(random.randint(10,40))
        log.info("日期：{0}".format(date_result[0]))
        if date_result[1]:
            self.js_click(book["下个月"])
        self.js_click((locator[0], locator[1].format(date_result[0])))

    def choose_date(self):
        """选中日期"""
        log.info("选中日期")
        self.click_date()
        self.pick_date()
        sleep()

    def choose_round_trip_date(self):
        log.info("选中往返时间")
        date_result = self.random_book_date()
        locator1 = (book["日期选择"][0], book["日期选择"][1].format(date_result[0]))
        locator2 = (book["日期选择"][0], book["日期选择"][1].format(date_result[2]))
        eles = self.find_elements(book["日期"])
        eles[0].click()
        if date_result[1]:
            self.js_click(book["下个月"])
        self.js_click(locator1)
        eles[1].click()
        if date_result[3]:
            self.js_click(book["下个月"])
        self.js_click(locator2)

    def random_book_date(self):
        """
        locator1:出发日期的title
        check1：出发日期是否当月
        locator2：返程日期的title
        check2：返程日期是否当月
        """
        log.info("生成随机日期")
        random_number = random.randint(10,40)
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
        """点击查询"""
        log.info("点击查询")
        self.js_click(book["查询"])

    def click_book(self, button_name="预订"):
        """点击预订"""
        log.info("点击预订--随机点预订按钮")
        elements = self.find_elements(book["弹框确认"])
        for i in range(len(elements)):
            self.element_js_click(elements[i])
        book_elements = self.find_elements(book[button_name])
        number = random.randint(0, len(book_elements)-1)
        book_elements[number].click()

    def input_staff_name(self):
        """输入员工姓名"""
        log.info("输入员工姓名")
        self.input_text(book["姓名"], fake.name())

    def choose_staff_department(self):
        """选择员工部门"""
        log.info("选择员工部门")
        self.roll_to_tagert(book["费用部门"])
        self.js_click(book["费用部门"])
        self.js_click(book["选中部门"])

    def input_id_number(self):
        """输入身份证号码"""
        log.info("输入身份证号")
        self.input_text(book["身份证号"], ID())
        # sleep()

    def click_build_order(self):
        """点击生成订单"""
        log.info("点击提交订单订单")
        self.roll_to_tagert(book["提交订单"])
        self.js_click(book["阅读并接受"])
        self.js_click(book["提交订单"])

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
        sys_order_id = self.driver.current_url[-18:]
        log.info("系统订单号: {0}".format(sys_order_id))
        self.js_click(book["我的商旅"])
        self.js_click(book["国内机票第一个订单"])
        assert sys_order_id == self.driver.current_url[-18:]  # 如果第一个订单id不是刚下单的订单id，则报错
        text = self.element_text(book["订单号"])
        return text[4:13]

    def passenger_by_add_staff(self):
        """通过新增添加乘机人"""
        log.info("通过新增添加乘机人")
        self.input_staff_name()
        # try:  # 若有感应员工，则不新增
        #     self.js_click(book["第一个感应员工"])
        # except:
        #     self.input_id_number()
        #     self.choose_staff_department()
        self.input_id_number()
        self.choose_staff_department()

    def add_passenger(self):
        log.info("添加乘机人")
        self.roll_to_tagert(book["添加乘机人"])
        self.js_click(book["添加乘机人"])
        name = fake.name()
        log.info("输入姓名：{0}".format(name))
        self.find_elements(book["姓名"])[-1].send_keys(name)
        try:
            self.js_click(book["第一个感应员工"])
        except:
            ID_number = ID()
            log.info("输入身份证号：{0}".format(ID_number))
            self.find_elements(book["身份证号"])[-1].send_keys(ID_number)
            log.info("选中部门")
            self.find_elements(book["费用部门"])[-1].click()
            self.js_click(book["选中部门"])

    def place_order(self, departure_city, arrive_city, one_person=True):
        log.info("生成待支付订单")
        self.click_flight_product()
        self.click_one_way()
        self.departure_city(departure_city)
        self.arrive_city(arrive_city)
        self.choose_date()
        self.click_search()
        self.click_book()
        self.passenger_by_add_staff()
        if not one_person:
            self.add_passenger()
            self.add_passenger()
        self.click_build_order()
        assert "订单已提交成功" in self.element_text(book["订单提交结果"])

    def book_one_way(self, departure_city, arrive_city, one_person=True):
        log.info("预订单程机票")
        self.place_order(departure_city, arrive_city, one_person)
        self.click_credit_pay()
        return self.get_pay_result()

    def book_round_trip(self, departure_city, arrive_city):
        log.info("预订往返机票")
        self.click_flight_product()
        self.js_click(book["往返"])
        self.departure_city(departure_city)
        self.arrive_city(arrive_city)
        self.choose_round_trip_date()
        self.click_search()
        self.click_book("选择去程") # 去程
        sleep(3)
        self.click_book("选择返程") # 返程
        self.passenger_by_add_staff()
        self.add_passenger()
        self.click_build_order()
        self.click_credit_pay()
        return self.get_pay_result()

    def cancel_order(self):
        log.info("点击订单详情的取消按钮取消订单")
        self.js_click(book["取消按钮"])
        self.js_click(book["确定取消"])
        sleep(0.5)
        return self.element_text(book["订单状态"])

if __name__ == "__maim__":
    pass

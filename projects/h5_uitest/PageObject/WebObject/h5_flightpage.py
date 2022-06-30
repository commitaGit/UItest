import random
import datetime
from page.webpage import WebPage, sleep
from common.readelement import Element
from utils.buildIDnumber import generate_id as ID
from faker import Faker
from utils.logger import log

fake = Faker(locale='zh_CN')
flight = Element('h5', 'h5_flight')

class FlightPage(WebPage):
    """h5国内机票类"""

    def click_flight_product(self):
        """点击机票产品"""
        log.info("点击机票产品")
        self.refresh()
        sleep()
        self.js_click(flight["机票产品"])

    def click_one_way(self):
        """点击单程"""
        log.info("点击单程")
        self.js_click(flight["单程"])

    def click_round_trip(self):
        """点击往返"""
        log.info("点击往返")
        self.js_click(flight["往返"])

    def departure_city(self, departure_city):
        """输入出发城市"""
        log.info("选择出发城市")
        self.js_click(flight["出发城市"])
        sleep(0.5)
        log.info("输入内容：{0}".format(departure_city))
        self.input_text(flight["城市输入"], departure_city)
        self.js_click(flight["第一个城市"]) 

    def arrive_city(self, arrive_city):
        log.info("输入并选中到达城市")
        log.info("选择出发城市")
        self.js_click(flight["到达城市"])
        sleep(0.5)
        log.info("输入内容：{0}".format(arrive_city))
        self.input_text(flight["城市输入"], arrive_city)
        self.js_click(flight["第一个城市"]) 

    def choose_date(self):
        log.info("选中日期")
        self.js_click(flight["日历"]) 
        self.js_click(flight["日期选择"]) 

    def choose_round_trip_date(self):
        log.info("选中往返时间")
        self.js_click(flight["日历"])
        self.js_click(flight["去程日期"])
        self.js_click(flight["返程日期"])

    def click_search(self):
        """点击查询"""
        log.info("点击查询")
        self.js_click(flight["查询"])

    def click_book(self):
        log.info("预订第一个航班的第二个舱位")
        self.js_click(flight["第一个航班"])
        sleep()
        self.js_click(flight["第一个舱位"])

    def add_passenger(self):
        log.info("添加乘机人")
        self.roll_to_tagert(flight["添加乘机人"])
        self.js_click(flight["添加乘机人"])
        self.js_click(flight["新增员工"])
        name = fake.name()
        log.info("输入姓名：{0}".format(name))
        self.find_elements(flight["姓名"])[-1].send_keys(name)
        ID_number = ID()
        log.info("输入身份证号：{0}".format(ID_number))
        self.find_elements(flight["身份证号"])[-1].send_keys(ID_number)
        log.info("选中总部")
        self.js_click(flight["部门"])
        self.js_click(flight["总部"])
        # self.js_click(flight["部门确定"])
        self.js_click(flight["添加确定"])

    def click_build_order(self):
        """点击生成订单"""
        log.info("点击提交订单订单")
        self.roll_to_tagert(flight["协议"])
        self.js_click(flight["协议"])
        self.js_click(flight["去付款"])

    def click_credit_pay(self):
        """点击授信支付"""
        log.info("点击授信支付的支付按钮")
        self.js_click(flight["支付"])
        elems = self.find_elements(flight["支付"])
        elems[-1].click()

    def get_pay_result(self):
        """获取支付结果"""
        log.info("获取支付结果")
        elems = self.find_elements(flight["支付结果"])
        return elems[0].text

    def get_order_id(self):
        """获取订单号"""
        log.info("获取订单号")
        self.js_click(flight["查看订单"])
        text = self.element_text(flight["订单号"])
        return text[5:]

    def get_order_status(self):
        log.info("获取订单状态")
        return self.element_text(flight["订单状态"])

    def click_left_return(self):
        log.info("点击左上角返回按钮")
        self.js_click(flight["详情左上角返回"])

    def place_order(self, departure_city, arrive_city, one_person=True):
        log.info("生成待支付订单")
        self.click_flight_product()
        self.is_click(flight["单程"])
        self.departure_city(departure_city)
        self.arrive_city(arrive_city)
        self.choose_date()
        self.click_search()
        self.click_book()
        self.add_passenger()
        if not one_person:
            self.add_passenger()
            self.add_passenger()
        self.click_build_order()
        assert self.element_exist(flight["明细"])

    def flight_one_way(self, departure_city, arrive_city, one_person=True):
        log.info("预订单程机票")
        self.place_order(departure_city, arrive_city, one_person)
        self.click_credit_pay()
        return self.get_pay_result()

    def flight_round_trip(self, departure_city, arrive_city):
        log.info("预订往返机票")
        self.click_flight_product()
        self.is_click(flight["往返"])
        self.departure_city(departure_city)
        self.arrive_city(arrive_city)
        self.choose_round_trip_date()
        self.click_search()
        self.click_book() # 去程
        sleep(3)
        self.js_click(flight["返程第一个航班"])
        self.is_click(flight["返程第一个舱位"])
        self.add_passenger()
        self.add_passenger()
        self.click_build_order()
        self.click_credit_pay()
        return self.get_pay_result()

    def to_order_list(self):
        log.info("进入我的订单列表")
        self.refresh()
        sleep(1)
        log.info("点击 我的")
        self.js_click(flight["我的"])
        log.info("点击 全部订单")
        self.js_click(flight["全部订单"])

    def choose_first_order(self):
        log.info("选中第一个已出票订单")
        self.find_elements(flight["列表已出票订单"])[0].click()

    def choose_first_passenger(self):
        log.info("退改选中第一个乘机人")
        self.find_elements(flight["乘机人勾选"])[0].click()
        self.find_elements(flight["下一步"])[-1].click()
        sleep()
        self.find_elements(flight["下一步"])[-1].click()

    def submit_change_apply(self):
        log.info("提交改签申请")
        self.to_order_list()
        self.choose_first_order()
        self.js_click(flight["改签"])
        self.choose_first_passenger()
        self.js_click(flight["选择出发时间"])
        self.js_click(flight["日期选择"])
        self.click_search()
        self.click_book()
        self.js_click(flight["确认改签按钮"])
        assert self.element_exist(flight["退/改签结果"])
        return self.get_order_id()

    def submit_return_apply(self):
        log.info("提交退票申请")
        self.to_order_list()
        self.choose_first_order()
        order_id = self.element_text(flight["订单号"])[5:]
        self.js_click(flight["退票"])
        self.choose_first_passenger()
        assert self.element_exist(flight["退/改签结果"])
        return order_id

    def go_trip_return(self):
        log.info("去程提交退票申请")
        self.to_order_list()
        self.choose_first_order()
        order_id = self.element_text(flight["订单号"])[5:]
        self.js_click(flight["退票"])
        self.find_elements(flight["下一步"])[-1].click()
        self.choose_first_passenger()
        assert self.element_exist(flight["退/改签结果"])
        return order_id

    def back_trip_return(self):
        log.info("返程提交退票申请")
        self.to_order_list()
        self.find_elements(flight["列表多状态订单"])[0].click()
        order_id = self.element_text(flight["订单号"])[5:]
        self.js_click(flight["退票"])
        self.js_click(flight["退票去程"])
        self.js_click(flight["退票返程"])
        self.find_elements(flight["下一步"])[-1].click()
        self.choose_first_passenger()
        assert self.element_exist(flight["退/改签结果"])
        return order_id

    def round_trip_return(self):
        log.info("往返程提交退票申请")
        self.to_order_list()
        self.roll_to_tagert(flight["第二个订单状态"])
        self.find_elements(flight["列表多状态订单"])[0].click()
        order_id = self.element_text(flight["订单号"])[5:]
        self.js_click(flight["退票"])
        self.js_click(flight["退票返程"])
        self.find_elements(flight["下一步"])[-1].click()
        self.choose_first_passenger()
        assert self.element_exist(flight["退/改签结果"])
        return order_id

    def cancel_order(self):
        log.info("点击订单详情的取消按钮取消订单")
        self.to_order_list()
        self.find_elements(flight["列表待确认订单"])[0].click()
        self.js_click(flight["取消按钮"])
        self.js_click(flight["取消确定"])
        sleep(0.5)
        return self.element_text(flight["订单状态"])


if __name__ == "__maim__":
    pass

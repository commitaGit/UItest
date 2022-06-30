from page.apppage import AppPage, sleep
from common.readelement import Element
from utils.buildIDnumber import generate_id as ID
from faker import Faker
from utils.logger import log

fake = Faker(locale='zh_CN')
bookflight = Element('app', 'app_flightbook')

class AppBookFlight(AppPage):
    """app预订国内机票类"""

    def click_flight_product(self):
        """点击机票产品"""
        log.info("点击机票产品")
        self.is_click(bookflight["机票产品"])

    def click_one_way(self):
        """点击单程"""
        log.info("点击单程")
        self.is_click(bookflight["单程"])

    def click_round_trip(self):
        """点击往返"""
        log.info("点击往返")
        self.is_click(bookflight["往返"])

    def click_on_business(self):
        """点击因公"""
        log.info("点击因公")
        self.is_click(bookflight["因公"])

    def click_on_personal(self):
        """点击因私"""
        log.info("点击因私")
        self.is_click(bookflight["因私"])

    def click_departure_city(self):
        """点击出发城市"""
        log.info("点击出发城市")
        self.is_click(bookflight["出发城市"])

    def input_departure_city(self, departure_city):
        """输入出发城市"""
        log.info("输入出发城市")
        self.input_text(bookflight["出发城市搜索"], departure_city)
        # sleep(2)

    def pick_departure_city(self):
        """选中出发城市"""
        log.info("选中出发城市")
        self.is_click(bookflight["出发城市选择"])
        # sleep()

    def choose_departure_city(self, departure_city):
        """输入并选中出发城市"""
        self.click_departure_city()
        self.input_departure_city(departure_city)
        self.pick_departure_city()

    def click_arrive_city(self):
        """点击到达城市"""
        log.info("点击到达城市")
        self.is_click(bookflight["到达城市"])

    def input_arrive_city(self, arrive_city):
        """输入到达城市"""
        log.info("输入到达城市")
        self.input_text(bookflight["到达城市搜索"], arrive_city)
        # sleep(2)

    def pick_arrive_city(self):
        """选中到达城市"""
        log.info("选中到达城市")
        self.is_click(bookflight["到达城市选择"])
        # sleep()

    def choose_arrive_city(self, arrive_city):
        """输入并选中到达城市"""
        self.click_arrive_city()
        self.input_arrive_city(arrive_city)
        self.pick_arrive_city()

    def click_date(self):
        """点击日期"""
        log.info("点击日期")
        self.is_click(bookflight["日期"])

    def pick_date(self):
        """点击选中日期"""
        eles = self.find_elements(bookflight["日期选择"])
        if len(eles) == 1:
            eles[1].click()
        else :
            eles[2].click()

    def click_search(self):
        """点击查询"""
        log.info("点击查询")
        self.is_click(bookflight["查询"])
        # sleep(5)

    def click_flight(self):
        """选中航班"""
        log.info("选中航班")
        self.is_click(bookflight["选中航班"])
        # sleep()

    def click_book(self):
        """点击预订"""
        log.info("点击预订")
        self.is_click(bookflight["预订按钮"])
        # sleep(3)

    def click_add_passenger(self):
        """点击添加乘机人"""
        log.info("点击添加乘机人")
        self.is_click(bookflight['添加乘机人'])
        # sleep()

    def click_add_staff(self):
        """点击添加员工"""
        log.info("点击添加员工")
        self.is_click(bookflight["新增员工按钮"])
        # sleep()

    def input_staff_name(self):
        """输入员工姓名"""
        log.info("输入员工姓名")
        self.input_text(bookflight["员工姓名"], fake.name())

    def choose_staff_department(self):
        """选择员工部门"""
        log.info("选择员工部门")
        self.is_click(bookflight["部门选择"])
        # sleep()
        self.is_click(bookflight["选中部门"])

    def input_id_number(self):
        """输入身份证号码"""
        log.info("输入身份证号")
        self.input_text(bookflight["证件号"], ID())
        # sleep()

    def click_confirm_staff(self):
        """点击确定添加员工按钮"""
        log.info("点击确定按钮增加员工")
        self.is_click(bookflight["确定--添加员工"])
        # sleep(2)

    def choose_passenger(self):
        """选中乘机人"""
        log.info("选中乘机人")
        self.is_click(bookflight["选中员工"])
        # sleep()

    def cancel_receipt(self):
        """取消报销凭证勾选"""
        log.info("点击报销凭证")
        eles = self.find_elements(bookflight["邮寄地址"])
        if len(eles) == 7: # 只适用于只有一个乘机人
            self.find_elements(bookflight["报销凭证"])[2].click()

    def click_agreement(self):
        """勾选协议"""
        log.info("点击已读协议")
        self.swipe_down()
        # sleep()
        self.is_click(bookflight["阅读并接受"])

    def click_build_order(self):
        """点击生成订单"""
        log.info("点击去付款生成订单")
        self.is_click(bookflight["去付款"])
        # sleep(5)

    def place_order(self):
        """提交订单"""
        self.cancel_receipt()
        self.click_agreement()
        self.click_build_order()

    def click_continue_book(self):
        """点击继续下单"""
        log.info("已有订单则点击继续下单")
        self.is_click(bookflight["继续下单"])
        # sleep(5)

    def click_pay(self):
        """点击支付"""
        log.info("点击支付按钮")
        self.is_click(bookflight["支付"])

    def click_credit_pay(self):
        """点击授信支付"""
        log.info("点击授信支付的支付按钮")
        self.is_click(bookflight["授信支付"])
        sleep(10)

    def get_pay_result(self):
        """获取支付结果"""
        log.info("获取支付结果")
        return self.element_text(bookflight["支付结果"])

    def click_view_order(self):
        """点击查看订单"""
        log.info("点击查看订单进入订单详情")
        self.is_click(bookflight["查看订单"])

    def get_order_id(self):
        """获取订单号"""
        log.info("获取订单号")
        return self.element_text(bookflight["订单号"])[5:]

    def passenger_by_add_staff(self):
        """通过新增添加乘机人"""
        self.click_add_passenger()
        self.click_add_staff()
        self.input_staff_name()
        self.choose_staff_department()
        self.input_id_number()
        self.click_confirm_staff()

    def launch_app(self):
        """重新打开APP"""
        log.info("重新打开APP")
        self.driver.launch_app()
        # sleep(2)



if __name__ == "__maim__":
    pass

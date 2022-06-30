import datetime
from page.apppage import AppPage, sleep
from common.readelement import Element
from common.buildIDnumber import generate_id as ID
from utils.logger import log
from faker import Faker
from common.readconfig import ini

fake = Faker(locale='zh_CN')
booktrain = Element('app', 'app_trainbook')
NAME = ini._get("STAFF", "TRAINPASSENGER")

class AppBookTrain(AppPage):
    """app火车票预订类"""
    def click_train_product(self):
        """点击火车票产品"""
        log.info("点击火车票产品")
        self.is_click(booktrain["火车票产品"])
        
    def click_on_business(self):
        """点击因公"""
        log.info("点击因公")
        self.is_click(booktrain["因公"])

    def click_on_personal(self):
        """点击因私"""
        log.info("点击因私")
        self.is_click(booktrain["因私"])

    def input_departure_city(self, departure_city):
        """输入出发城市"""
        log.info("搜索并选中出发城市")
        self.is_click(booktrain["出发站点"])
        self.input_text(booktrain["出发地搜索"], departure_city)
        # sleep(2)
        self.is_click(booktrain["出发地选择"])
        # sleep()

    def input_arrive_city(self, arrive_city):
        """输入到达城市"""
        log.info("搜索并选中到达城市")
        self.is_click(booktrain["到达站点"])
        self.input_text(booktrain["到达地搜索"], arrive_city)
        # sleep(2)
        self.is_click(booktrain["到达地选择"])
        # sleep()

    def pick_date(self):
        """点击选中日期"""
        log.info("点击选中日期")
        self.is_click(booktrain["日期"])
        locator, index = self.get_date_locator()
        eles = self.find_elements(locator)
        eles[index].click()

    def click_search(self):
        """点击查询"""
        log.info("点击查询按钮")
        self.is_click(booktrain["查询"])
        # sleep(5)

    def click_train(self):
        """选中车次"""
        log.info("选中第一个车次")
        self.is_click(booktrain["选中车次"])
        # sleep()

    def click_book(self):
        """点击预订"""
        log.info("点击第一个预订按钮")
        self.find_elements(booktrain["预订按钮"])[0].click()
        self.is_click(booktrain["预订"])
        # sleep()

    def click_add_passenger(self):
        """点击添加乘车人"""
        log.info("点击天机乘车人按钮")
        self.is_click(booktrain['选择乘客'])
        # sleep()

    def click_add_staff(self):
        """点击添加员工"""
        log.info("点击添加员工")
        self.is_click(booktrain["新增员工按钮"])
        # sleep()

    def input_staff_name(self):
        """输入员工姓名"""
        log.info("输入员工姓名")
        self.input_text(booktrain["员工姓名"], fake.name())

    def choose_staff_department(self):
        """选择员工部门"""
        log.info("选中员工部门")
        self.is_click(booktrain["部门选择"])
        # sleep()
        self.is_click(booktrain["选中部门"])

    def input_id_number(self):
        """输入身份证号码"""
        log.info("输入身份证号啊")
        self.input_text(booktrain["证件号"], ID())
        # sleep()

    def input_phone_number(self, phone):
        """输入手机号"""
        log.info("输入手机号")
        self.input_text(booktrain["手机号"], phone)

    def click_confirm_staff(self):
        """点击确定添加员工按钮"""
        log.info("点击确定按钮添加员工")
        self.is_click(booktrain["确定--添加员工"])
        # sleep(2)

    def choose_passenger(self):
        """选中乘车人"""
        log.info("选中第一个员工")
        self.is_click(booktrain["选中员工"])
        # sleep()

    def click_build_order(self):
        """点击生成订单"""
        log.info("点击去付款生成订单")
        self.is_click(booktrain["去付款"])
        # sleep(5)

    def click_pay(self):
        """点击确认支付"""
        log.info("点击确认支付")
        self.is_click(booktrain["确认支付"])

    def click_credit_pay(self):
        """点击授信支付"""
        log.info("点击授信支付")
        self.is_click(booktrain["授信支付"])
        sleep(3)

    def get_pay_result(self):
        """获取支付结果"""
        log.info("获取支付结果")
        return self.element_text(booktrain["支付结果"])

    def click_view_order(self):
        """点击查看订单"""
        log.info("点击查看订单进入订单详情")
        sleep(2)
        self.is_click(booktrain["查看订单"])
        self.swipe_down()

    def launch_app(self):
        """重新打开APP"""
        log.info("重新打开APP")
        self.driver.launch_app()
        # sleep(2)

    def add_staff_by_ID(self, phone):
        """添加新员工--证件类型ID"""
        log.info("新增员工--证件类型为身份证")
        self.click_add_staff()
        self.input_staff_name()
        self.choose_staff_department()
        self.input_phone_number(phone)
        self.input_id_number()
        self.click_confirm_staff()

    def choose_staff(self, name=NAME):
        """输入员工姓名搜索后选中"""
        log.info("输入员工姓名搜索并选中")
        self.click_add_passenger()
        self.input_text(booktrain["搜索员工"], name)
        # sleep()
        locator = (booktrain["选中搜索员工"][0], booktrain["选中搜索员工"][1].format(name))
        self.is_click(locator)

    def get_date_locator(self):
        """构造日期locator"""
        search_day = 1
        index = 1
        day = datetime.datetime.now().day
        if day < 24:
            search_day = int(day) + 4
            index = 0
        locator = Element('app_trainbook')["日期选择"]
        locator = (locator[0], locator[1].format(search_day))
        return locator, index


if __name__ == "__maim__":
    pass

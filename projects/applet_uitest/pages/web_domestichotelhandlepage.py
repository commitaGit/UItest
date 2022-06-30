import random
from base.web_basepage import WebPage
from minium import logger
from time import sleep

ORDER_HANDLE = ("xpath", "//a[contains(text(), '订单处理')]")
DOMESTIC_HOTEL = ("xpath", "//a[@href='/order/domestic-hotel/tasks']")
ORDER_ID = ("xpath", "//input[@formcontrolname='orderNoLike']")
SEARCH_BUTTON = ("xpath", "//button[@type='submit']")
FIRST_ROW = ("xpath", "//tbody/tr[1]/td[2]") # 判断订单号是否有任务
# 调出任务，调出任务后才可查看任务类型
CHECK_BOX = ("xpath", "//thead/tr[1]/th[1]/label[1]")
CALL_OUT_TASK = ("xpath", "//span[contains(text(),'调出任务')]/..")
CONFIRM_BUTTON = ("xpath", "//span[contains(text(),'确定')]/..")
ACTION_BAR = ("xpath", "//tbody/tr[1]/td[11]/span[2]")
HANDLE = ("xpath", "//tbody/tr[1]/td[11]/span[2]/a")
# 部分退订确认
RETURN_FARE = ("xpath", "//input[@placeholder='退订手续费']")
PAY_SUPPLY_FARE = ("xpath", "//input[@placeholder='付供应商手续费（成本）']")
RETURN_SUCCESS = ("xpath", "//span[text()=' 退订成功 ']/..")
# 订房
SUPPLIER = ("xpath", "//nz-select[@formcontrolname='supplierObject']")
QIANTAO = ("xpath", "//div[contains(text(),'千淘')]/..")
SUPPLIER_PAYMENT = ("xpath", "//nz-select[@formcontrolname='supplierPaymentMode']")
FIRST_PAYMENT = ("xpath", "//cdk-virtual-scroll-viewport[1]/div[1]/nz-option-item[1]")
SUPPLIER_NUMBER = ("xpath", "//input[@formcontrolname='supplierOrderNo']")
PURCHASE_COST = ("xpath", "//input[@placeholder='房费']") # 有几个填几个（或填完第一个后面自动填充）
BOOK_SUCCESS = ("xpath", "//span[contains(text(),'订房成功')]/..")

class DomesticHotelOrderHandlePage(WebPage):
    """国内酒店订单处理类"""

    def domestic_order_handle(self):
        logger.info("进入国内酒店订单处理")
        self.js_click(ORDER_HANDLE)
        self.js_click(DOMESTIC_HOTEL)

    def order_search(self, order_id):
        logger.info("输入查询订单号：{0}".format(order_id))
        self.input_text(ORDER_ID, order_id)
        self.js_click(SEARCH_BUTTON)
        sleep(0.8)

    def task_exist_or_not(self):
        logger.info("判断订单号任务是否存在")
        if not self.element_exist(FIRST_ROW): # 订单号是否有记录
            return False
        return True

    def call_out_task(self):
        logger.info("调出任务")
        self.js_click(CHECK_BOX)
        self.js_click(CALL_OUT_TASK)
        self.js_click(CONFIRM_BUTTON)
        sleep(0.5)

    def enter_task_page(self):
        logger.info("进入任务处理详情页面")
        self.js_click(HANDLE)

    def reservation_confirm_page(self):
        logger.info("在订房确认页面完成订房任务")
        self.roll_to_tagert(BOOK_SUCCESS)
        self.js_click(SUPPLIER)
        self.js_click(QIANTAO)
        self.js_click(SUPPLIER_PAYMENT)
        self.js_click(FIRST_PAYMENT)
        self.input_text(SUPPLIER_NUMBER, random.randint(10000000000, 99999999999))
        eles = self.find_elements(PURCHASE_COST)
        eles[0].send_keys(random.randint(10, 50))
        self.js_click(BOOK_SUCCESS)
        self.js_click(CONFIRM_BUTTON)

    def to_task_detail_page(self, order_id):
        logger.info("进入订单：{0}任务详情页".format(order_id))
        self.domestic_order_handle()
        self.order_search(order_id)
        if not self.task_exist_or_not():
            return False
        if "无权限" in self.element_text(ACTION_BAR):
            self.call_out_task()
        self.enter_task_page()
        return True

    def reservation_confirm(self, order_id):
        logger.info("完成订单：{0}的订房任务全流程".format(order_id))
        if not self.to_task_detail_page(order_id):
            return False
        self.reservation_confirm_page()
        return self.task_submit_result()

    def part_cancel_room_page(self):
        logger.info("在退订任务页面完成退订任务")
        self.roll_to_tagert(RETURN_SUCCESS)
        self.input_text(RETURN_FARE, random.randint(10, 20))
        self.input_text(PAY_SUPPLY_FARE, random.randint(1, 10))
        self.js_click(RETURN_SUCCESS)

    def all_cancel_room_page(self):
        logger.info("在退订任务页面完成退订任务")
        self.roll_to_tagert(RETURN_SUCCESS)
        self.js_click(RETURN_SUCCESS)

    def part_cancel_room(self, order_id):
        logger.info("完成订单：{0}的部分退房任务".format(order_id))
        if not self.to_task_detail_page(order_id):
            return False
        self.part_cancel_room_page()
        return self.task_submit_result()

    def all_cancel_room(self, order_id):
        logger.info("完成订单：{0}的全部退房任务".format(order_id))
        if not self.to_task_detail_page(order_id):
            return False
        self.all_cancel_room_page()
        return self.task_submit_result()

    def task_submit_result(self):
        logger.info("调出任务按钮是否存在--判断任务是否提交成功，返回了国内酒店任务列表")
        if not self.element_exist(CALL_OUT_TASK):
            return False
        return True

if __name__ == "__maim__":
    pass

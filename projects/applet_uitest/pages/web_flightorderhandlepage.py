import random
from base.web_basepage import WebPage
from minium import logger
from time import sleep

ORDER_HANDLE = ("xpath", "//a[contains(text(), '订单处理')]")
DOMESTIC_FLIGHT = ("xpath", "//a[@href='/order/flight/task']")
ORDER_ID = ("name", "orderNoLike")
SEARCH_BUTTON = ("xpath", "//domestic-flight-task[1]/form[1]/nz-row[1]/nz-col[2]/button[1]")
FIRST_ROW = ("xpath", "//tbody/tr[1]/td[2]")# 判断订单号是否有任务
TASK_TYPE = ("xpath", "//tbody/tr[1]/td[12]/span[2]/span[1]")
# 调出任务
CHECK_BOX = ("xpath", "//thead/tr[1]/th[1]/label[1]")
CALL_OUT_TASK = ("xpath", "//span[contains(text(),'调出任务')]/..")
CONFIRM_BUTTON = ("xpath", "//span[contains(text(),'确定')]/..")
HANDLE = ("xpath", "//tbody/tr[1]/td[14]/span[2]/span[1]")
# 改签--改签报价
BUNK_CODE = ("xpath", "//*[@formcontrolname='bunkCode']")
FIRST_BUNK = ("xpath", "//cdk-virtual-scroll-viewport/div[1]/nz-option-item[1]")
REAL_CHANGE_REASON = ("xpath", "//shared-dict-select[@formcontrolname='actualChangeReasonCode']/nz-select[1]")
FIRST_REASON = ("xpath", "//cdk-virtual-scroll-viewport/div[1]/nz-option-item[1]")
CHANGE_FARE = ("xpath", "//input[@formcontrolname='changeTicketFee']")
CREDIT_SUBMIT = ("xpath", "//span[contains(text(),'授信提交')]/..")
# 改签--改签确认
CHANGE_TICKET_NO = ("xpath", "//input[@formcontrolname='ticketNo']")
TICKET_FEE_COST = ("xpath", "//input[@formcontrolname='ticketFeeCost']")
CONFIRM_CHANGE_FARE = ("xpath", "//input[@formcontrolname='changeTicketFeeCost']")
CHANGE_SUPPLIER = ("xpath", "//nz-select[@formcontrolname='supplier']")
CHANGE_BSP = ("xpath", "//div[contains(text(),'BSP')]/..")
CHANGE_PAYMENT = ("xpath", "//nz-select[@formcontrolname='supplierPaymentMode']")
FIRST_PAYMENT = ("xpath", "//cdk-virtual-scroll-viewport/div[1]/nz-option-item[1]")
CHANGE_PAYMENT_NO = ("xpath", "//input[@formcontrolname='supplierPaymentNo']")
CHANGE_SUBMIT = ("xpath", "//span[contains(text(),'提交')]/..")
# 出票
TICKET_NO = ("xpath", "//input[@formcontrolname='ticketNo']")
PAYMENT_NO = ("xpath", "//input[@formcontrolname='supplierPaymentNo']")
SUBMIT_BUTTON = ("xpath", "//span[contains(text(),'提交')]/..")
# 退票
REAL_RETURN_REASON = ("xpath", "//shared-dict-select[@formcontrolname='actualReturnReasonCode']/nz-select[1]")
FIRST_RETURN_REASON = ("xpath", "//cdk-virtual-scroll-viewport/div[1]/nz-option-item[1]")  # 第一个原因
COLLECT_RETURN_FARE = ("xpath", "//input[@formcontrolname='returnTicketFee']")
PAY_RETURN_FARE =  ("xpath", "//input[@formcontrolname='returnTicketFeeCost']")
RETURN_CONFIRM = ("xpath", "//span[contains(text(),'退票确认')]/..")

class FlightOrderHandlePage(WebPage):
    """国内机票订单处理类"""

    def click_order_handle(self):
        logger.info("点击订单处理")
        self.js_click(ORDER_HANDLE)
        self.js_click(DOMESTIC_FLIGHT)

    def order_search(self, order_id):
        logger.info("输入查询订单号：{0}".format(order_id))
        self.input_text(ORDER_ID, order_id)
        self.js_click(SEARCH_BUTTON)
        sleep(0.5)

    def task_exist_or_not(self, task_type):
        logger.info("判断订单号任务是否存在")
        if not self.element_exist(FIRST_ROW): # 订单号是否有记录
            return False
        web_task_type = self.element_text(TASK_TYPE)
        if web_task_type != task_type:
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
        sleep(0.5)
        self.js_click(HANDLE)

    def ticket_confirm_page(self):
        logger.info("在出票确认页面完成出票确认任务")
        eles = self.find_elements(TICKET_NO)
        for ele in eles:
            ticket_number = random.randint(1000000000000, 9999999999999)
            logger.info("输入票号：{0}".format(ticket_number))
            ele.send_keys(ticket_number)
        try: # 交易流水号可能没有
            self.input_text(PAYMENT_NO, random.randint(10000000000, 99999999999))
        except:
            pass
        self.roll_to_tagert(SUBMIT_BUTTON)
        self.js_click(SUBMIT_BUTTON)

    def to_task_detail_page(self, order_id, task_type):
        logger.info("进入订单：{0}-{1}任务详情页".format(order_id, task_type))
        self.click_order_handle()
        self.order_search(order_id)
        if not self.task_exist_or_not(task_type):
            return False
        if "无权限" in self.element_text(HANDLE):
            self.call_out_task()
        self.enter_task_page()
        return True

    def ticket_confirm(self, order_id, task_type="出票"):
        logger.info("完成订单：{0}的出票确认任务全流程".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.ticket_confirm_page()
        return self.task_submit_result()

    def change_confirm_page(self):
        logger.info("在改签确认页面完成改签确认任务")
        eles = self.find_elements(CHANGE_TICKET_NO)
        for ele in eles:
            ticket_number = random.randint(1000000000000, 9999999999999)
            logger.info("输入票号：{0}".format(ticket_number))
            ele.send_keys(ticket_number)
        self.input_text(TICKET_FEE_COST, random.randint(10, 20))
        self.input_text(CONFIRM_CHANGE_FARE, random.randint(1, 10))
        self.roll_to_tagert(CHANGE_SUBMIT)
        self.js_click(CHANGE_SUPPLIER)
        self.js_click(CHANGE_BSP)
        self.js_click(CHANGE_PAYMENT)
        self.js_click(FIRST_PAYMENT)
        try:
            self.input_text(CHANGE_PAYMENT_NO, random.randint(10000000000, 99999999999))
        except:
            pass
        self.js_click(CHANGE_SUBMIT)

    def change_confirm(self, order_id, task_type="改签确认"):
        logger.info("完成订单：{0}的改签确认任务".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.change_confirm_page()
        return True

    def return_confirm_page(self):
        logger.info("在退票任务页面完成退票任务")
        self.roll_to_tagert(REAL_RETURN_REASON)
        self.js_click(REAL_RETURN_REASON)
        self.js_click(FIRST_RETURN_REASON)
        self.roll_to_tagert(COLLECT_RETURN_FARE)
        self.input_text(COLLECT_RETURN_FARE, random.randint(10, 20))
        self.input_text(PAY_RETURN_FARE, random.randint(1, 10))
        self.roll_to_tagert(RETURN_CONFIRM)
        self.js_click(RETURN_CONFIRM)

    def return_confirm(self, order_id, task_type="退票"):
        logger.info("完成订单：{0}的退票任务".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.return_confirm_page()
        return True

    def change_offer_page(self):
        logger.info("在改签报价任务页面完成改签报价任务")
        self.roll_to_tagert(REAL_CHANGE_REASON)
        self.js_click(REAL_CHANGE_REASON)
        self.js_click(FIRST_REASON)
        self.roll_to_tagert(CREDIT_SUBMIT)
        self.js_click(BUNK_CODE)
        self.js_click(FIRST_BUNK)
        self.input_text(CHANGE_FARE, 1)
        self.js_click(CREDIT_SUBMIT)

    def change_offer(self, order_id, task_type="改签报价"):
        logger.info("完成订单：{0}的改签报价任务".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.change_offer_page()
        return True

    def task_submit_result(self):
        logger.info("调出任务按钮是否存在--判断任务是否提交成功，返回了国内机票任务列表")
        if not self.element_exist(CALL_OUT_TASK): # 订单号是否有记录
            return False
        return True

    def round_trip_ticket_confirm(self, order_id, task_type):
        logger.info("完成往返订单：{0}的出票确认任务全流程".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.ticket_confirm_page()
        assert self.task_submit_result(), "没找到调出任务按钮"
        self.js_click(SEARCH_BUTTON)
        if self.task_exist_or_not(task_type):
            self.enter_task_page()
            self.ticket_confirm_page()
            assert self.task_submit_result(), "没找到调出任务按钮"
        return True

    def round_trip_return_confirm(self, order_id, task_type="退票"):
        logger.info("完成订单：{0}的退票任务".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.return_confirm_page()
        assert self.task_submit_result(), "没找到调出任务按钮"
        self.js_click(SEARCH_BUTTON)
        self.enter_task_page()
        self.return_confirm_page()
        return self.task_submit_result()

if __name__== "__maim__":
    pass

import random
from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element

handle = Element('web', 'web_flightorderhandle')

class FlightOrderHandlePage(WebPage):
    """国内机票订单处理类"""

    def click_order_handle(self):
        log.info("点击订单处理")
        self.js_click(handle["订单处理"])
        self.js_click(handle["国内机票"])

    def order_search(self, order_id):
        log.info("输入查询订单号：{0}".format(order_id))
        self.input_text(handle["订单号"], order_id)
        self.js_click(handle["查询"])
        sleep(0.5)

    def task_exist_or_not(self, task_type):
        log.info("判断订单号任务是否存在")
        if not self.element_exist(handle["第一行"]): # 订单号是否有记录
            return False
        web_task_type = self.element_text(handle["任务类型"])
        if web_task_type != task_type:
            return False
        return True

    def call_out_task(self):
        log.info("调出任务")
        self.js_click(handle["勾选框"])
        self.js_click(handle["调出任务"])
        self.js_click(handle["确定"])
        sleep(0.5)

    def enter_task_page(self):
        log.info("进入任务处理详情页面")
        sleep(0.5)
        self.js_click(handle["操作"])

    def ticket_confirm_page(self):
        log.info("在出票确认页面完成出票确认任务")
        eles = self.find_elements(handle["票号"])
        for ele in eles:
            ticket_number = random.randint(1000000000000, 9999999999999)
            log.info("输入票号：{0}".format(ticket_number))
            ele.send_keys(ticket_number)
        try: # 交易流水号可能没有
            self.input_text(handle["交易流水号"], random.randint(10000000000, 99999999999))
        except:
            pass
        self.roll_to_tagert(handle["提交"])
        self.js_click(handle["提交"])

    def to_task_detail_page(self, order_id, task_type):
        log.info("进入订单：{0}-{1}任务详情页".format(order_id, task_type))
        self.click_order_handle()
        self.order_search(order_id)
        if not self.task_exist_or_not(task_type):
            return False
        if "无权限" in self.element_text(handle["操作"]):
            self.call_out_task()
        self.enter_task_page()
        return True

    def ticket_confirm(self, order_id, task_type="出票"):
        log.info("完成订单：{0}的出票确认任务全流程".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.ticket_confirm_page()
        return self.task_submit_result()

    def change_confirm_page(self):
        log.info("在改签确认页面完成改签确认任务")
        eles = self.find_elements(handle["改签票号"])
        for ele in eles:
            ticket_number = random.randint(1000000000000, 9999999999999)
            log.info("输入票号：{0}".format(ticket_number))
            ele.send_keys(ticket_number)
        self.input_text(handle["票补差价"], random.randint(10, 20))
        self.input_text(handle["确认改签手续费"], random.randint(1, 10))
        self.roll_to_tagert(handle["改签提交"])
        self.js_click(handle["改签供应商"])
        self.js_click(handle["改签-BSP"])
        self.js_click(handle["改签支付方式"])
        self.js_click(handle["第一个支付方式"])
        try:
            self.input_text(handle["改签交易流水号"], random.randint(10000000000, 99999999999))
        except:
            pass
        self.js_click(handle["改签提交"])

    def change_confirm(self, order_id, task_type="改签确认"):
        log.info("完成订单：{0}的改签确认任务".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.change_confirm_page()
        return True

    def return_confirm_page(self):
        log.info("在退票任务页面完成退票任务")
        self.roll_to_tagert(handle["实际退票原因"])
        self.js_click(handle["实际退票原因"])
        self.js_click(handle["退票原因"])
        self.roll_to_tagert(handle["收取退票手续费"])
        self.input_text(handle["收取退票手续费"], random.randint(10, 20))
        self.input_text(handle["付供应商退票手续费"], random.randint(1, 10))
        self.roll_to_tagert(handle["退票确认"])
        self.js_click(handle["退票确认"])

    def return_confirm(self, order_id, task_type="退票"):
        log.info("完成订单：{0}的退票任务".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.return_confirm_page()
        return True

    def change_offer_page(self):
        log.info("在改签报价任务页面完成改签报价任务")
        self.roll_to_tagert(handle["实际改签原因"])
        self.js_click(handle["实际改签原因"])
        self.js_click(handle["第一个原因"])
        self.roll_to_tagert(handle["授信提交"])
        self.js_click(handle["舱位代码"])
        self.js_click(handle["第一个舱位"])
        self.input_text(handle["改签手续费"], 1)
        self.js_click(handle["授信提交"])

    def change_offer(self, order_id, task_type="改签报价"):
        log.info("完成订单：{0}的改签报价任务".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.change_offer_page()
        return True

    def change_offer_cancel_page(self):
        log.info("在改签报价页面完成改签取消任务")
        self.roll_to_tagert(handle["取消改签"])
        eles = self.find_elements(handle["取消改签"])
        for ele in eles:
            ele.click()
        self.input_text(handle["操作备注"], "取消测试")
        self.js_click(handle["确认"])
        self.roll_to_tagert(handle["改签取消"])
        self.js_click(handle["改签取消"])

    def change_offer_cancel(self, order_id, task_type="改签报价"):
        log.info("完成订单：{0}的改签报价取消任务".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.change_offer_cancel_page()
        return True

    def change_confirm_cancel_page(self):
        log.info("在改签报价页面完成改签取消任务")
        self.roll_to_tagert(handle["取消改签"])
        eles = self.find_elements(handle["取消改签"])
        for ele in eles:
            ele.click()
        self.input_text(handle["操作备注"], "取消测试")
        self.js_click(handle["确认"])
        self.roll_to_tagert(handle["提交"])
        self.js_click(handle["提交"])

    def change_confirm_cancel(self, order_id, task_type="改签确认"):
        log.info("完成订单：{0}的改签报价取消任务".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.change_confirm_cancel_page()
        return True

    def return_confirm_cancel_page(self):
        log.info("在退票任务页面完成退票取消任务")
        self.roll_to_tagert(handle["退票取消"])
        self.js_click(handle["退票取消"])
        self.js_click(handle["确定"])

    def return_confirm_cancel(self, order_id, task_type="退票"):
        log.info("完成订单：{0}的退票取消任务".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.return_confirm_cancel_page()
        return True

    def task_submit_result(self):
        log.info("调出任务按钮是否存在--判断任务是否提交成功，返回了国内机票任务列表")
        if not self.element_exist(handle["调出任务"]): # 订单号是否有记录
            return False
        return True

    def round_trip_ticket_confirm(self, order_id, task_type):
        log.info("完成往返订单：{0}的出票确认任务全流程".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.ticket_confirm_page()
        assert self.task_submit_result()
        self.js_click(handle["查询"])
        if self.task_exist_or_not(task_type):
            self.enter_task_page()
            self.ticket_confirm_page()
            assert self.task_submit_result()
        return True

    def round_trip_return_confirm(self, order_id, task_type="退票"):
        log.info("完成订单：{0}的退票任务".format(order_id))
        if not self.to_task_detail_page(order_id, task_type):
            return False
        self.return_confirm_page()
        assert self.task_submit_result()
        self.js_click(handle["查询"])
        self.enter_task_page()
        self.return_confirm_page()
        return self.task_submit_result()


if __name__ == "__maim__":
    pass

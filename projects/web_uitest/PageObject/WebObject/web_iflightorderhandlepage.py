import random
from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element

handle = Element('web', 'web_iflightorderhandle')

class IntFlightOrderHandlePage(WebPage):
    """国际机票订单处理类"""

    def click_order_handle(self):
        log.info("点击订单处理")
        self.js_click(handle["订单处理"])

    def click_needs(self):
        log.info("进入国际机票需求任务列表")
        self.click_order_handle()
        self.js_click(handle["国际机票需求"])

    def click_handle(self):
        log.info("进入国际机票处理任务列表")
        self.click_order_handle()
        self.js_click(handle["国际机票处理"])

    def order_search(self, order_id):
        log.info("输入查询订单号：{0}".format(order_id))
        self.input_text(handle["订单号"], order_id)
        self.js_click(handle["查询"])
        sleep(0.5)

    def task_exist_or_not(self, task_type, customer_type="需求类型"): # 有需求和处理两种客服类型
        log.info("判断订单号任务是否存在")
        if not self.element_exist(handle["第一行"]): # 订单号是否有记录
            return False
        web_task_type = self.element_text(handle[customer_type])
        if web_task_type != task_type:
            return False
        return True

    def call_out_task(self):
        log.info("调出任务")
        self.js_click(handle["勾选框"])
        self.js_click(handle["调出任务"])
        self.js_click(handle["调出确定"])
        sleep(0.5)

    def enter_task_page(self, customer_type="需求操作"):
        log.info("进入任务处理详情页面")
        sleep(0.5)
        self.is_click(handle[customer_type])

    def ticket_apply_page(self):
        log.info("在出票申请页面完成出票申请确认")
        self.js_click(handle["提交出票申请"])

    def ticket_confirm_page(self):
        log.info("在出票确认页面完成出票确认任务")
        ticket_number = random.randint(1000000000000, 9999999999999)
        log.info("输入票号：{0}".format(ticket_number))
        self.input_text(handle["票号"], ticket_number)
        self.js_click(handle["供应商"])
        self.js_click(handle["携程"])
        self.js_click(handle["供应商支付方式"])
        self.js_click(handle["出票第一个支付方式"])
        try: # 交易流水号可能没有
            self.input_text(handle["供应商订单号"],  random.randint(10000000, 99999999))
            self.input_text(handle["交易流水号"],  random.randint(10000000, 99999999))
        except:
            pass
        self.roll_to_tagert(handle["确认出票"])
        self.js_click(handle["确认出票"])

    def to_needs_detail_page(self, order_id, task_type):
        """进入国际机票需求任务详情页"""
        log.info("进入订单：{0}-{1}需求任务详情页".format(order_id, task_type))
        self.click_needs()
        self.order_search(order_id)
        if not self.task_exist_or_not(task_type):
            return False
        if "无权限" in self.element_text(handle["需求操作"]):
            self.call_out_task()
        self.enter_task_page()
        return True

    def to_handle_detail_page(self, order_id, task_type):
        log.info("进入订单：{0}-{1}处理任务详情页".format(order_id, task_type))
        self.click_handle()
        self.order_search(order_id)
        if not self.task_exist_or_not(task_type, customer_type="任务类型"):
            return False
        if "无权限" in self.element_text(handle["任务操作"]):
            self.call_out_task()
        self.enter_task_page(customer_type="任务操作")
        return True

    def ticket_apply(self, order_id, task_type="出票申请"):
        log.info("完成订单：{0}的出票确认任务全流程".format(order_id))
        if not self.to_needs_detail_page(order_id, task_type):
            return False
        self.ticket_apply_page()
        return self.task_submit_result()

    def ticket_confirm(self, order_id, task_type="出票"):
        log.info("完成订单：{0}的出票确认任务全流程".format(order_id))
        if not self.to_handle_detail_page(order_id, task_type):
            return False
        self.ticket_confirm_page()
        return self.task_submit_result()

    def change_apply_page(self):
        log.info("在改签申请页面完成改签申请确认")
        self.roll_to_tagert(handle["实际改签原因"])
        self.js_click(handle["实际改签原因"])
        self.js_click(handle["第一个改签原因"])
        self.roll_to_tagert(handle["改签支付"])
        self.input_text(handle["票价补差"], random.randint(1, 100))
        self.input_text(handle["税费补差"], random.randint(1, 20))
        self.input_text(handle["改签手续费"], random.randint(1, 10))
        self.input_text(handle["误机费"], random.randint(1, 10))
        self.input_text(handle["退票政策"], "按照航司规定")
        self.input_text(handle["改签政策"], "按照航司规定")
        self.js_click(handle["改签支付"])
        self.js_click(handle["确定"])

    def change_apply(self, order_id, task_type="改签申请"):
        log.info("完成订单：{0}的改签申请任务".format(order_id))
        if not self.to_needs_detail_page(order_id, task_type):
            return False
        self.change_apply_page()
        return True

    def change_confirm_page(self):
        log.info("在改签确认页面完成改签确认任务")
        self.roll_to_tagert(handle["改签确认"])
        ticket_number = random.randint(1000000000000, 9999999999999)
        log.info("输入票号：{0}".format(ticket_number))
        self.input_text(handle["改签票号"], ticket_number)
        self.input_text(handle["票补差价"], random.randint(1, 40))
        self.input_text(handle["税费差价"], random.randint(1, 10))
        self.input_text(handle["改签费"], random.randint(1, 10))
        self.input_text(handle["改签误机费"], random.randint(1, 10))
        self.js_click(handle["改签供应商"])
        self.js_click(handle["改签-携程"])
        self.js_click(handle["改签支付方式"])
        self.js_click(handle["改签第一个支付方式"])
        try:
            self.input_text(handle["改签供应商订单号"], random.randint(10000000, 99999999))
            self.input_text(handle["改签交易流水号"], random.randint(10000000, 99999999))
        except:
            pass
        self.js_click(handle["改签确认"])

    def change_confirm(self, order_id, task_type="改签"):
        log.info("完成订单：{0}的改签确认任务".format(order_id))
        if not self.to_handle_detail_page(order_id, task_type):
            return False
        self.change_confirm_page()
        return True

    def return_apply_page(self):
        log.info("在退票申请任务页面完成退票申请任务")
        self.roll_to_tagert(handle["确认退票"])
        self.js_click(handle["实际退票原因"])
        self.js_click(handle["第一个退票原因"])
        self.input_text(handle["票面退款"], random.randint(1, 100))
        self.input_text(handle["税费退款"], random.randint(1, 50))
        self.input_text(handle["退票手续费"], random.randint(0, 10))
        self.input_text(handle["客户留款"], random.randint(0, 10))
        self.js_click(handle["确认退票"])
        self.js_click(handle["退票确定"])

    def return_apply(self, order_id, task_type="退票申请"):
        log.info("完成订单：{0}的退票申请任务".format(order_id))
        if not self.to_needs_detail_page(order_id, task_type):
            return False
        self.return_apply_page()
        return True

    def return_confirm_page(self):
        log.info("在退票任务页面完成退票任务")
        self.roll_to_tagert(handle["退票确认"])
        self.input_text(handle["退票费"], random.randint(0, 10))
        self.input_text(handle["退票误机费"], random.randint(0, 10))
        try:
            self.input_text(handle["退票供应商订单号"], random.randint(1000000, 9999999))
            self.input_text(handle["退票交易流水号"], random.randint(1000000, 9999999))
        except:
            pass
        self.js_click(handle["退票确认"])

    def return_confirm(self, order_id, task_type="退票"):
        log.info("完成订单：{0}的退票任务".format(order_id))
        if not self.to_handle_detail_page(order_id, task_type):
            return False
        self.return_confirm_page()
        return True

    def invalid_apply_page(self):
        log.info("在退票任务页面完成废票申请")
        self.roll_to_tagert(handle["确认退票"])
        self.js_click(handle["申请废票"])
        self.input_text(handle["废票费"], random.randint(0, 10))
        self.js_click(handle["确认废票"])

    def invalid_apply(self, order_id, task_type="退票申请"):
        log.info("完成订单：{0}的废票申请任务".format(order_id))
        if not self.to_needs_detail_page(order_id, task_type):
            return False
        self.invalid_apply_page()
        return True

    def invalid_confirm_page(self):
        log.info("在废票任务页面完成废票任务")
        self.roll_to_tagert(handle["废票确认"])
        self.input_text(handle["供应商订单号"], random.randint(1000000, 99999999))
        self.js_click(handle["废票确认"])

    def invalid_confirm(self, order_id, task_type="废票"):
        log.info("完成订单：{0}的{1}任务".format(order_id, task_type))
        if not self.to_handle_detail_page(order_id, task_type):
            return False
        self.invalid_confirm_page()
        return True

    def cancel_order(self, order_id, task_type="取消"):
        log.info("完成订单：{0}的{1}任务".format(order_id, task_type))
        self.to_needs_detail_page(order_id, task_type)
        self.roll_to_tagert(handle["取消确认"])
        self.js_click(handle["取消确认"])

    def change_apply_cancel(self, order_id, task_type="改签申请"):
        log.info("完成订单：{0}的改签申请取消任务".format(order_id, task_type))
        self.to_needs_detail_page(order_id, task_type)
        self.roll_to_tagert(handle["改签取消"])
        self.js_click(handle["改签取消"])
        self.js_click(handle["确定"])

    def return_apply_cancel(self, order_id, task_type="退票申请"):
        log.info("完成订单：{0}的退票申请取消任务".format(order_id, task_type))
        self.to_needs_detail_page(order_id, task_type)
        self.roll_to_tagert(handle["退票取消"])
        self.js_click(handle["退票取消"])
        self.js_click(handle["退票确定"])

    def return_confirm_cancel(self, order_id, task_type="退票"):
        log.info("完成订单：{0}的退票确认取消任务".format(order_id, task_type))
        self.to_handle_detail_page(order_id, task_type)
        self.roll_to_tagert(handle["退票取消"])
        self.js_click(handle["退票取消"])
        self.js_click(handle["退票确定"])

    def task_submit_result(self):
        log.info("调出任务按钮是否存在--判断任务是否提价成功，返回了国际机票任务列表")
        if not self.element_exist(handle["调出任务"]):
            return False
        return True

if __name__ == "__maim__":
    pass

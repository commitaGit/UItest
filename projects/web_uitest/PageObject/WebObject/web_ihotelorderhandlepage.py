import random
from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element

handle = Element('web', 'web_ihotelorderhandle')

class IntHotelOrderHandlePage(WebPage):
    """国际酒店订单处理类"""

    def click_handle(self):
        log.info("进入国际酒店处理任务列表")
        self.js_click(handle["订单处理"])
        self.js_click(handle["国际酒店"])

    def lock_order(self):
        log.info("完成锁单操作")
        eles = self.find_elements(handle["锁单"])
        for ele in range(len(eles)-1, -1, -1):
            log.info("点击：{0}".format(eles[ele]))
            eles[ele].click()

    def order_search(self, order_id):
        log.info("输入查询订单号：{0}".format(order_id))
        self.js_click(handle["全部任务"])
        self.input_text(handle["订单号"], order_id)
        self.js_click(handle["查询"])

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
        self.js_click(handle["调出确定"])
        sleep(0.5)

    def enter_task_page(self):
        log.info("进入任务处理详情页面")
        self.js_click(handle["操作"])

    def to_task_detail_page(self, order_id, task_type):
        log.info("进入订单：{0}任务详情页".format(order_id))
        self.click_handle()
        try:
            self.lock_order()
        except:
            pass
        self.order_search(order_id)
        if not self.task_exist_or_not(task_type):
            return False
        if "无权限" in self.element_text(handle["操作"]):
            self.call_out_task()
        self.enter_task_page()
        return True

    def book_room_page(self):
        log.info("订房页面完成订房任务")
        self.roll_to_tagert(handle["供应商"])
        self.js_click(handle["供应商"])
        self.js_click(handle["第一个供应商"])
        self.js_click(handle["供应商支付方式"])
        self.js_click(handle["第一个支付方式"])
        try: # 交易流水号可能没有
            self.input_text(handle["供应商订单号"],  random.randint(10000000, 99999999))
            self.input_text(handle["供应商交易流水号"],  random.randint(10000000, 99999999))
        except:
            pass
        eles = self.find_elements(handle["房间成本"])
        eles[0].send_keys(random.randint(1, 50))
        self.js_click(handle["订房成功"])

    def book_room(self, order_id):
        log.info("完成订房任务全流程")
        if not self.to_task_detail_page(order_id, task_type="订房"):
            return False
        self.book_room_page()
        return self.element_text(handle["提交结果"])

    def cancel_room_page(self):
        log.info("在退订页面完成退订任务")
        eles = self.find_elements(handle["退订手续费"])
        for ele in eles:
            ele.send_keys(random.randint(0, 10))
        eles = self.find_elements(handle["付供应商手续费（成本）"])
        for ele in eles:
            ele.send_keys(random.randint(0, 10))
        eles = self.find_elements(handle["客户留款"])
        for ele in eles:
            ele.send_keys(random.randint(0, 10))
        self.js_click(handle["确认"])

    def cancel_room(self, order_id):
        log.info("完成退房任务全流程")
        if not self.to_task_detail_page(order_id, task_type="退房"):
            return False
        self.cancel_room_page()
        return self.element_text(handle["退订结果"])

if __name__ == "__maim__":
    pass

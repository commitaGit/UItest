import random
from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element

handle = Element('web', 'web_hotelorderhandle')

class DomesticHotelOrderHandlePage(WebPage):
    """国内酒店订单处理类"""

    def domestic_order_handle(self):
        log.info("进入国内酒店订单处理")
        self.js_click(handle["订单处理"])
        self.js_click(handle["国内酒店"])

    def order_search(self, order_id):
        log.info("输入查询订单号：{0}".format(order_id))
        self.input_text(handle["订单号"], order_id)
        self.js_click(handle["查询"])
        sleep(0.8)

    def task_exist_or_not(self):
        log.info("判断订单号任务是否存在")
        if not self.element_exist(handle["第一行"]): # 订单号是否有记录
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
        self.js_click(handle["操作"])

    def reservation_confirm_page(self):
        log.info("在订房确认页面完成订房任务")
        self.roll_to_tagert(handle["订房成功"])
        self.js_click(handle["供应商"])
        self.js_click(handle["千淘"])
        self.js_click(handle["供应商支付方式"])
        self.js_click(handle["第一个支付方式"])
        self.input_text(handle["供应商订单号"], random.randint(10000000000, 99999999999))
        eles = self.find_elements(handle["房间采购成本"])
        eles[0].send_keys(random.randint(10, 50))
        self.js_click(handle["订房成功"])
        self.js_click(handle["确定"])

    def to_task_detail_page(self, order_id):
        log.info("进入订单：{0}任务详情页".format(order_id))
        self.domestic_order_handle()
        self.order_search(order_id)
        if not self.task_exist_or_not():
            return False
        if "无权限" in self.element_text(handle["操作栏"]):
            self.call_out_task()
        self.enter_task_page()
        return True

    def reservation_confirm(self, order_id):
        log.info("完成订单：{0}的订房任务全流程".format(order_id))
        if not self.to_task_detail_page(order_id):
            return False
        self.reservation_confirm_page()
        return self.task_submit_result()

    def part_cancel_room_page(self):
        log.info("在退订任务页面完成退订任务")
        self.roll_to_tagert(handle["退订成功"])
        self.input_text(handle["退订手续费"], random.randint(10, 20))
        self.input_text(handle["付供应商手续费"], random.randint(1, 10))
        self.js_click(handle["退订成功"])

    def all_cancel_room_page(self):
        log.info("在退订任务页面完成退订任务")
        self.roll_to_tagert(handle["退订成功"])
        self.js_click(handle["退订成功"])

    def part_cancel_room(self, order_id):
        log.info("完成订单：{0}的部分退房任务".format(order_id))
        if not self.to_task_detail_page(order_id):
            return False
        self.part_cancel_room_page()
        return self.task_submit_result()

    def all_cancel_room(self, order_id):
        log.info("完成订单：{0}的全部退房任务".format(order_id))
        if not self.to_task_detail_page(order_id):
            return False
        self.all_cancel_room_page()
        return self.task_submit_result()

    def task_submit_result(self):
        log.info("调出任务按钮是否存在--判断任务是否提交成功，返回了国内酒店任务列表")
        if not self.element_exist(handle["调出任务"]):
            return False
        return True

if __name__ == "__maim__":
    pass

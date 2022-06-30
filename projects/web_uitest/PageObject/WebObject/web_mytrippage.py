from page.webpage import WebPage
from utils.logger import log
from common.readelement import Element

my_trip = Element('web', 'web_mytrip')

class MyTripPage(WebPage):
    """前台我的商旅类"""

    def click_my_trip(self):
        log.info("点击我的商旅")
        self.js_click(my_trip["我的商旅"])

    def click_my_plan(self):
        log.info("点击我的计划")
        self.js_click(my_trip["我的计划"])

    def click_my_apply(self):
        log.info("点击我的申请")
        self.js_click(my_trip["我的申请"])

    def to_my_apply(self):
        log.info("进入我的申请页面")
        self.click_my_trip()
        self.click_my_plan()
        self.click_my_apply()

    def approval_number_search(self, approval_number):
        log.info("输入审批单号查询")
        self.input_text(my_trip["审批单号"], approval_number)
        self.js_click(my_trip["查询"])

    def to_approval_detail(self, approval_number):
        log.info("进入审批单详情")
        self.to_my_apply()
        self.approval_number_search(approval_number)
        self.js_click(my_trip["审批详情"])

    def one_level_status(self):
        log.info("获取一级审批状态")
        return self.element_text(my_trip["一级审批状态"])

    def two_level_status(self):
        log.info("获取二级审批状态")
        return self.element_text(my_trip["二级审批状态"])

if __name__ == "__maim__":
    pass

from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element

travelplan = Element('web', 'web_travelplan')

class SubmitTravelPlanPage(WebPage):
    """前台提交差旅计划类"""

    def click_travel_plan(self):
        """点击差旅计划"""
        log.info("点击 差旅计划")
        self.js_click(travelplan["差旅计划"])

    def input_travel_reason(self, reason):
        """填写出差事由"""
        log.info("填写出差事由")
        self.input_text(travelplan["出差事由"], reason)

    def input_travel_destination(self, destination):
        """填写出差目的地"""
        log.info("填写 出差目的地")
        self.input_text(travelplan["出差目的地"], destination)

    def travel_time(self):
        """选择出差日期"""
        log.info("选择开始日期")
        self.js_click(travelplan["开始日期"])
        self.js_click(travelplan["选中开始日期"])
        self.js_click(travelplan["选择结束日期"])

    def travel_staff(self):
        """选择出差员工"""
        log.info("选择出差员工")
        self.js_click(travelplan["姓名"])
        sleep()
        self.js_click(travelplan["选中员工"])

    def click_submit(self):
        """点击提交差旅计划"""
        log.info("点击提交差旅计划")
        self.js_click(travelplan["提交差旅计划"])

    def get_submit_status(self):
        """获取提交状态"""
        log.info("获取出差计划提交状态")
        return self.element_text(travelplan["提交状态"])

    def get_approval_number(self):
        """获取审批单号"""
        log.info("获取审批单号")
        return self.element_text(travelplan["审批单号"])[5:]

if __name__ == "__maim__":
    pass

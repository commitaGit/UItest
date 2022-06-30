from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element

travelapprove = Element('web', 'web_travelapprovalH5')

class ApprovalPage(WebPage):
    """审批出差申请类"""

    def click_refuse(self):
        """点击拒绝"""
        log.info("点击审批拒绝")
        self.js_click(travelapprove["拒绝"])
        self.js_click(travelapprove["确认"])
        self.refresh()

    def click_agree(self):
        """点击拒绝"""
        log.info("点击审批同意")
        self.js_click(travelapprove["同意"])
        self.js_click(travelapprove["确认"])
        self.refresh()

    def approve_status_one(self):
        """获取一级审批结果"""
        log.info("获取一级审批结果")
        return self.find_elements(travelapprove["审批状态"])[0].text

    def approve_status_two(self):
        """获取二级审批结果"""
        log.info("获取二级审批结果")
        return self.find_elements(travelapprove["审批状态"])[1].text


if __name__ == "__maim__":
    pass

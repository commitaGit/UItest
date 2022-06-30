from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element
from common.readconfig import ini

approvalsetting = Element('web', 'web_approvalsettings')

APPROVER = ini._get("STAFF", "APPROVER")

class ApprovalSettingPage(WebPage):
    """审批出差申请类"""

    def to_approval_setting(self):
        """进入事前审批设置页面"""
        log.info("首页进入事前审批设置页面")
        self.js_click(approvalsetting["商旅管理"])
        self.js_click(approvalsetting["出差设置"])
        self.js_click(approvalsetting["事前审批设置"])
        sleep(0.5)

    def secondary_approver(self):
        """获取二级审批人信息"""
        log.info("获取二级审批人信息")
        return self.element_text(approvalsetting["二级审批人姓名"])

    def secondary_approver_exist(self):
        """判断二级审批人是否设置"""
        log.info("判断二级审批人是否设置")
        if not self.element_text(approvalsetting["二级审批人姓名"]):
            return False
        return True

    def click_basics_change(self):
        """点击基础审批政策修改"""
        log.info("点击基础审批政策修改")
        self.js_click(approvalsetting["修改"])

    def input_secondary_approver(self):
        """搜索并选中二级审批人"""
        log.info("搜索并选中二级审批人")
        self.js_click(approvalsetting["二级审批人输入框"])
        self.input_text(approvalsetting["二级审批人输入"], APPROVER)
        locator = (approvalsetting["选中二级审批人"][0], approvalsetting["选中二级审批人"][1].format(APPROVER))
        self.js_click(locator)

    def clear_secondary_approver(self):
        """删除二级审批人数据"""
        log.info("清空二级审批人数据")
        self.js_click(approvalsetting["二级审批人删除"])

    def click_save(self):
        """点击保存"""
        log.info("点击保存")
        self.js_click(approvalsetting["保存"])
        sleep(0.5)

if __name__ == "__maim__":
    pass

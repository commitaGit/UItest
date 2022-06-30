from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element
from common.readconfig import ini

authorizationsetting = Element('web', 'web_authorizationsettings')

AUTHORIZER = ini._get("STAFF", "AUTHORIZER")

class AuthorizationSettingPage(WebPage):
    """审批出差申请类"""

    def to_authorization_setting(self):
        """进入事中授权设置页面"""
        log.info("首页进入事前授权设置页面")
        self.js_click(authorizationsetting["商旅管理"])
        self.js_click(authorizationsetting["出差设置"])
        self.js_click(authorizationsetting["事中授权设置"])
        sleep()

    def set_authorization_rule(self):
        """点击设置授权规则按钮"""
        log.info("点击设置授权规则按钮")
        self.is_click(authorizationsetting["设置授权规则"])

    def authorization_open_status(self):
        """判断授权管控是否开始"""
        log.info("判断授权管控是否开始")
        attr_class = self.find_element(authorizationsetting["授权管控开关"]).get_attribute('class')
        if attr_class == "ant-switch":
            return False
        return True

    def click_authorization_switch(self):
        """点击授权流程开关"""
        log.info("点击授权流程开关")
        self.js_click(authorizationsetting["授权管控开关"])

    def click_save(self):
        """点击保存"""
        log.info("点击保存")
        self.js_click(authorizationsetting["保存"])
        sleep(0.5)

    def save_result(self):
        """点击保存的结果"""
        log.info("保存结果")
        return self.element_text(authorizationsetting["保存结果"])

    def secondary_authorizer(self):
        """获取二级授权人信息"""
        log.info("获取二级授权人信息")
        return self.element_text(authorizationsetting["二级授权人姓名"])

    def secondary_authorizer_exist(self):
        """判断二级授权人是否设置"""
        log.info("判断二级授权人是否设置")
        sleep(0.5)
        if not self.element_text(authorizationsetting["二级授权人姓名"]):
            return False
        return True

    def click_basics_change(self):
        """点击基础审批政策修改"""
        log.info("点击基础审批政策修改")
        self.js_click(authorizationsetting["修改"])

    def input_secondary_authorizer(self):
        """搜索并选中二级授权人"""
        log.info("搜索并选中二级授权人")
        self.js_click(authorizationsetting["二级授权人输入框"])
        self.input_text(authorizationsetting["二级授权人输入"], AUTHORIZER)
        locator = (authorizationsetting["选中二级授权人"][0], authorizationsetting["选中二级授权人"][1].format(AUTHORIZER))
        self.js_click(locator)
        # self.js_click(authorizationsetting["二级授权人输入框"])

    def clear_secondary_authorizer(self):
        """删除二级授权人数据"""
        log.info("清空二级授权人数据")
        self.js_click(authorizationsetting["二级授权人删除"])

if __name__ == "__maim__":
    pass

from page.webpage import WebPage
from utils.logger import log
from common.readelement import Element

management = Element('web', 'web_management')

class ManagementPage(WebPage):
    """前台商旅管理类"""

    def click_management(self):
        log.info("点击 商旅管理")
        self.js_click(management["商旅管理"])

    def click_travel_settings(self):
        log.info("点击 出差设置")
        self.js_click(management["出差设置"])

    def click_travel_policy(self):
        log.info("点击 差旅政策")
        self.js_click(management["差旅政策"])

    def travel_policy_name(self):
        log.info("校验 差旅政策名称")
        return self.element_exist(management["差旅政策名称"])

    def basic_travel_policy(self):
        log.info("校验 基础差标政策")
        return self.element_exist(management["基础差标政策"])

    def book_setting(self):
        log.info("校验 预订设置")
        return self.element_exist(management["预订设置"])

    def add_travel_policy(self):
        log.info("校验 新增差标政策")
        return self.element_exist(management["新增差旅政策"])

    def click_book_setting(self):
        log.info("点击预订设置")
        self.js_click(management["预订设置"])
        return self.element_exist(management["自定义字段"])

    def domestic_flight_setting(self):
        log.info("校验 国内机票设置")
        self.js_click(management["国内机票设置"])
        return self.element_exist(management["机票行程限制"])

    def insurance(self):
        log.info("校验 员工自愿购买保险")
        return self.element_exist(management["员工自愿购买保险"])

    def refund_reason(self):
        log.info("校验 退票原因配置")
        return self.element_exist(management["退票需要填写原因"])

    def change_reason(self):
        log.info("校验 改签原因配置")
        return self.element_exist(management["改签需要填写原因"])

    def train_setting(self):
        log.info("校验 火车票设置")
        self.js_click(management["火车票设置"])

    def iflight_setting(self):
        log.info("校验 国际·港澳台机票设置")
        self.js_click(management["国际·港澳台机票设置"])

    def click_travel_setting_back(self):
        log.info("点击预订设置的返回")
        self.roll_to_tagert(management["返回"])
        self.js_click(management["返回"])

    def click_add_travel_policy(self):
        log.info("点击 新增差旅政策")
        self.js_click(management["新增差旅政策"])

    def click_open(self):
        log.info("点击 启用")
        eles = self.find_elements(management["启用"])
        for ele in eles:
            ele.click()

    def domestic_flight_policy(self):
        log.info("校验 国内机票设置")
        return self.element_exist(management["国内机票设置"])

    def domestic_hotel_policy(self):
        log.info("校验 国内酒店政策")
        return self.element_exist(management["国内酒店政策"])

    def price_limit(self):
        log.info("校验 需预订最低价")
        return self.element_exist(management["价格限制"])

    def book_time_limit(self):
        log.info("校验 需提前预订")
        return self.element_exist(management["时间限制"])

    def discount_limit(self):
        log.info("校验 机票折扣")
        return self.element_exist(management["折扣限制"])

    def bunk_limit(self):
        log.info("校验 舱等限制")
        return self.element_exist(management["舱等限制"])

    def depart_time_limit(self):
        log.info("校验 起飞时间")
        return self.element_exist(management["起飞时间限制"])

    def additional_remark(self):
        log.info("校验 补充说明")
        return self.element_exist(management["补充说明"])

    def first_tier_cities(self):
        log.info("校验 一线城市")
        return self.element_exist(management["一线城市"])

    def second_tier_cities(self):
        log.info("校验 二线城市")
        return self.element_exist(management["二线城市"])

    def third_tier_cities(self):
        log.info("校验 三线城市")
        return self.element_exist(management["三线城市"])

    def other_cities(self):
        log.info("校验 其他城市")
        return self.element_exist(management["其他城市"])

    def city_setting_button(self):
        log.info("校验 去设置城市等级按钮")
        return self.element_exist(management["去设置城市等级"])

    def click_approval_setting(self):
        log.info("点击 事前审批设置")
        self.js_click(management["事前审批设置"])

    def basic_approval_policy(self):
        log.info("校验 基础审批政策")
        return self.element_exist(management["基础审批政策"])

    def employees_without_approval(self):
        log.info("校验 无需审批的员工")
        return self.element_exist(management["无需审批的员工"])

    def setting_approval_role(self):
        log.info("校验 设置审批规则")
        return self.element_exist(management["设置审批规则"])

    def add_approval_process(self):
        log.info("校验 新增审批流程")
        return self.element_exist(management["新增审批流程"])

    def click_add_approval_process(self):
        log.info("点击 新增审批流程")
        self.js_click(management["新增审批流程"])

    def personal_approval_process(self):
        log.info("校验 个人审批流程")
        return self.element_exist(management["个人审批流程"])

    def departmental_approval_process(self):
        log.info("校验 部门审批流程")
        return self.element_exist(management["部门审批流程"])

    def click_approval_close(self):
        log.info("点击 审批关闭")
        self.find_elements(management["审批关闭"])[-1].click()

    def click_authorization_settings(self):
        log.info("点击 事中授权设置")
        self.js_click(management["事中授权设置"])

    def employees_without_authorization(self):
        log.info("校验 无需授权的员工")
        return self.element_exist(management["无需授权的员工"])

    def basic_authorization_policy(self):
        log.info("校验 基础授权政策")
        return self.element_exist(management["基础授权政策"])

    def click_add_authorization_policy(self):
        log.info("点击 新增授权流程")
        self.js_click(management["新增授权流程"])

    def personal_authorization_process(self):
        log.info("校验 个人授权流程")
        return self.element_exist(management["个人授权流程"])

    def project_authorization_process(self):
        log.info("校验 项目授权流程")
        return self.element_exist(management["项目授权流程"])

    def departmental_authorization_process(self):
        log.info("校验 部门授权流程")
        return self.element_exist(management["部门授权流程"])

    def click_authorization_close(self):
        log.info("点击 授权关闭")
        self.find_elements(management["授权关闭"])[-1].click()

    def click_notification_settings(self):
        log.info("点击 事后知会设置")
        self.js_click(management["事后知会设置"])

    def employees_without_notification(self):
        log.info("校验 无需知会的员工")
        return self.element_exist(management["无需知会的员工"])

    def basic_notification_policy(self):
        log.info("校验 基础知会政策")
        return self.element_exist(management["基础知会政策"])

    def click_add_notification_policy(self):
        log.info("点击 新增知会流程")
        self.js_click(management["新增知会流程"])

    def personal_notification_process(self):
        log.info("校验 个人知会流程")
        return self.element_exist(management["个人知会流程"])

    def project_notification_process(self):
        log.info("校验 项目知会流程")
        return self.element_exist(management["项目知会流程"])

    def departmental_notification_process(self):
        log.info("校验 部门知会流程")
        return self.element_exist(management["部门知会流程"])

    def click_notification_close(self):
        log.info("点击 知会关闭")
        self.find_elements(management["知会关闭"])[-1].click()

    def click_setting_notification_rule(self):
        log.info("点击 设置知会规则")
        self.js_click(management["设置知会规则"])

    def open_notification_process(self):
        log.info("校验 开启知会流程")
        return self.element_exist(management["开启知会流程"])

    def click_notification1_close(self):
        log.info("点击 知会关闭")
        self.find_elements(management["知会关闭1"])[0].click()

    def click_enterprise_project(self):
        log.info("点击 企业项目")
        self.js_click(management["企业项目"])

    def click_add_project(self):
        log.info("点击 新增项目")
        self.js_click(management["新增项目"])

    def project_name(self):
        log.info("校验 项目名称")
        return self.element_exist(management["项目名称"])

    def click_project_close(self):
        log.info("点击 项目返回")
        self.find_elements(management["项目返回"])[0].click()

    def click_project_association_settings(self):
        log.info("点击 项目关联设置")
        self.js_click(management["项目关联设置"])

    def associated_project(self):
        log.info("校验 出差订单关联项目")
        return self.element_exist(management["出差订单关联项目"])

    def click_associated_project_back(self):
        log.info("点击 关联项目返回")
        self.js_click(management["关联项目返回"])

    def click_green_channel(self):
        log.info("点击 绿色通道")
        self.js_click(management["绿色通道"])

    def click_add_green_channel_staff(self):
        log.info("点击 新增人员")
        self.js_click(management["新增人员"])

    def click_cancel(self):
        log.info("点击 取消")
        self.js_click(management["取消"])

    def click_city_level(self):
        log.info("点击 城市等级")
        self.js_click(management["城市等级"])

    def first_tier_city(self):
        log.info("校验 等级一线城市")
        return self.element_exist(management["等级一线城市"])

    def second_tier_city(self):
        log.info("校验 等级二线城市")
        return self.element_exist(management["等级二线城市"])

    def third_tier_city(self):
        log.info("校验 等级三线城市")
        return self.element_exist(management["等级三线城市"])

    def other_city(self):
        log.info("校验 等级其他城市")
        return self.element_exist(management["等级其他城市"])

    def refresh_page(self):
        log.info("刷新页面（避免弹框未关闭导致后续用例失败）")
        self.refresh()
        self.js_click(management["出差设置"])

if __name__ == "__maim__":
    pass

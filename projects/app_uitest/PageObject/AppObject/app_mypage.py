from page.apppage import AppPage, sleep
from common.readelement import Element
from utils.logger import log

mypage = Element('app', 'app_mypage')


class AppMyPage(AppPage):
    """APP我的页面类"""

    def click_my_page(self):
        log.info("点击我的页面")
        self.find_elements(mypage["我的"])[-1].click()
        sleep()

    def click_my_order(self):
        log.info("点击我的订单")
        self.is_click(mypage['我的订单'])

    def check_order_list(self):
        log.info("校验 订单列表")
        return self.element_exist(mypage["订单列表"])

    def click_all(self):
        log.info("点击全部")
        self.is_click(mypage["全部"])

    def click_be_paid(self):
        log.info("点击待支付")
        self.is_click(mypage["待支付"])

    def click_processing(self):
        log.info("点击处理中")
        self.is_click(mypage["处理中"])

    def click_wait_travel(self):
        log.info("点击待出行")
        self.is_click(mypage["待出行"])

    def click_refund_cancel(self):
        log.info("点击退款/取消")
        self.is_click(mypage["退款/取消"])

    def click_return(self):
        log.info("点击左上角返回")
        self.is_click(mypage["左上角返回"])

    def check_contact_customer_service(self):
        log.info("校验联系客服")
        return self.element_exist(mypage["联系客服"])

    def click_common_information(self):
        log.info("点击常用信息")
        self.is_click(mypage["常用信息"])

    def click_passenger(self):
        log.info("点击旅客")
        self.is_click(mypage["旅客"])

    def check_passenger(self):
        log.info("校验旅客")
        return self.element_exist(mypage["旅客"])

    def click_address(self):
        log.info("点击 地址")
        self.is_click(mypage["地址"])

    def check_address(self):
        log.info("校验地址")
        return self.element_exist(mypage["地址"])

    def click_invoice(self):
        log.info("点击 发票")
        self.is_click(mypage["发票"])

    def check_invoice(self):
        log.info("校验发票")
        return self.element_exist(mypage["发票"])

    def click_about_us(self):
        log.info("点击关于我们")
        self.is_click(mypage["关于我们"])

    def click_user_instructions(self):
        log.info("点击用户须知")
        self.is_click(mypage["用户须知"])

    def check_user_instructions(self):
        log.info("校验 关于本服务许可")
        return self.element_exist(mypage["关于本服务许可"])

    def click_service_agreement(self):
        log.info("点击服务协议")
        self.is_click(mypage["服务协议"])

    def check_service_agreement(self):
        log.info("校验 用户服务协议")
        return self.element_exist(mypage["用户服务协议"])

    def click_privacy_policy(self):
        log.info("点击隐私政策")
        self.is_click(mypage["隐私政策"])

    def check_privacy_policy(self):
        log.info("校验 适用范围")
        return self.element_exist(mypage["适用范围"])

    def click_integral(self):
        log.info("点击积分")
        self.is_click(mypage["积分"])

    def click_integral_rule(self):
        log.info("点击积分规则")
        self.is_click(mypage["积分规则"])

    def check_integral_use(self):
        log.info("校验 积分能为我带来什么")
        return self.element_exist(mypage["积分能为我带来什么"])

    def check_get_integral(self):
        log.info("校验 如何获取更多积分")
        return self.element_exist(mypage["如何获取更多积分"])

    def click_setting(self):
        log.info("点击 设置")
        self.is_click(mypage["设置"])

    def check_my_info(self):
        log.info("校验 我的信息")
        return self.element_exist(mypage["我的信息"])

    def check_reset_password(self):
        log.info("校验 重置密码")
        return self.element_exist(mypage["重置密码"])

    def check_bind_phone(self):
        log.info("校验 绑定手机")
        return self.element_exist(mypage["绑定手机"])

    def check_clear_cache(self):
        log.info("校验 清除缓存")
        return self.element_exist(mypage["清除缓存"])

if __name__ == "__maim__":
    pass

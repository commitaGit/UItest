from page.webpage import WebPage
from utils.logger import log
from common.readelement import Element

flight_stub = Element('web', 'web_systemmanage')

class FlightTestStubPage(WebPage):
    """机票测试桩类"""

    def to_flight_stub(self):
        """到国内机票测试桩配置页面"""
        log.info("到国内机票测试桩配置页面")
        self.js_click(flight_stub["系统管理"])
        self.roll_to_tagert(flight_stub["国内机票测试桩"])
        self.js_click(flight_stub["国内机票测试桩"])

    def to_iflight_stub(self):
        """到国际机票测试桩配置页面"""
        log.info("到国际机票测试桩配置页面")
        self.js_click(flight_stub["系统管理"])
        self.roll_to_tagert(flight_stub["国际机票测试桩"])
        self.js_click(flight_stub["国际机票测试桩"])

    def operation_management(self):
        """点击系统管理"""
        log.info("点击 系统管理")
        self.js_click(flight_stub["系统管理"])

    def price_verification(self):
        """验价返回成功结果"""
        log.info("验价返回成功结果")
        self.js_click(flight_stub["验价"])
        self.js_click(flight_stub["返回成功结果"])

    def pnr_apply(self):
        """发起订座申请返回成功结果"""
        log.info("发起订座申请返回成功结果")
        self.js_click(flight_stub["发起订座申请"])
        self.js_click(flight_stub["返回成功结果"])

    def pnr_callback(self):
        """订座结果回调返回成功结果"""
        log.info("订座结果回调返回成功结果")
        self.js_click(flight_stub["订座结果回调"])
        self.js_click(flight_stub["返回成功结果"])

    def pay_verify(self):
        """支付前验证返回成功结果"""
        log.info("支付前验证返回成功结果")
        self.js_click(flight_stub["支付前验证"])
        self.js_click(flight_stub["返回成功结果"])

    def pay_verify_callback(self):
        """支付前验价回调返回成功结果"""
        log.info("支支付前验价回调返回成功结果")
        self.js_click(flight_stub["支付前验价回调"])
        self.js_click(flight_stub["返回成功结果"])

    def ticket_issuing_apply(self):
        """支出票申请返回成功结果"""
        log.info("出票申请返回成功结果")
        self.js_click(flight_stub["出票申请"])
        self.js_click(flight_stub["返回成功结果"])

    def ticket_issuing_callback(self):
        """出票回调成功结果"""
        log.info("出票回调返回成功结果")
        self.js_click(flight_stub["出票回调"])
        self.js_click(flight_stub["返回成功结果"])

    def separate_pnr(self):
        """分离PNR成功结果"""
        log.info("分离PNR返回成功结果")
        self.js_click(flight_stub["分离PNR"])
        self.js_click(flight_stub["返回成功结果"])

    def ticket_number_callback(self):
        """票号信息回调成功结果"""
        log.info("返回")
        self.js_click(flight_stub["票号信息回调"])
        self.js_click(flight_stub["返回成功结果"])

    def submit(self):
        """提交配置"""
        log.info("提交配置")
        self.js_click(flight_stub["提交"])

    def flight_stub_setting(self):
        """将国内机票测试桩全配置为返回成功结果"""
        log.info("将国内机票测试桩全配置为返回成功结果")
        self.to_flight_stub()
        eles = self.find_elements(flight_stub["国内机票配置项"])
        for number in range(len(eles)):
            eles[number].click()
            self.js_click(flight_stub["返回成功结果"])
        self.roll_to_tagert(flight_stub["提交"])
        self.submit()

    def iflight_stub_setting(self):
        """将国际机票测试桩全配置为返回成功结果"""
        log.info("将国内机票测试桩全配置为返回成功结果")
        self.to_iflight_stub()
        eles = self.find_elements(flight_stub["国际机票配置项"])
        for number in range(len(eles)):
            eles[number].click()
            self.js_click(flight_stub["返回成功结果"])
        self.submit()

if __name__ == "__maim__":
    pass

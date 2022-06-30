from page.webpage import WebPage
from utils.logger import log
from common.readelement import Element

authorization = Element('web', 'web_authorizationH5')

class AuthorizationPage(WebPage):
    """授权类"""

    def click_refuse(self):
        """点击拒绝"""
        log.info("点击授权拒绝")
        self.js_click(authorization["拒绝"])
        self.js_click(authorization["确认"])
        self.refresh()

    def click_agree(self):
        """点击同意"""
        log.info("点击授权同意")
        self.js_click(authorization["同意"])
        self.js_click(authorization["确认"])
        self.refresh()

    def authorize_status_one(self):
        """获取一级授权结果"""
        log.info("获取一级授权结果")
        return self.find_elements(authorization["授权状态"])[0].text

    def authorize_status_two(self):
        """获取二级授权结果"""
        log.info("获取二级授权结果")
        return self.find_elements(authorization["授权状态"])[1].text

    def get_order_id(self):
        """获取授权订单的订单号"""
        log.info("获取授权订单的订单号")
        text = self.element_text(authorization["订单号"])
        order_id = text[5:-1]
        return order_id

if __name__ == "__maim__":
    pass

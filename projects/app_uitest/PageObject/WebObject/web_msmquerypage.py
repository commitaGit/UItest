from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element

smsquery = Element('web', 'web_smsquery')

class SmsQueryPage(WebPage):
    """后台短信查询类"""

    def order_processing(self):
        """点击订单处理"""
        log.info("点击 订单处理")
        self.js_click(smsquery["订单处理"])

    def information_service(self):
        """点击信息平台--信息查询"""
        log.info("点击 信息平台--信息查询")
        self.js_click(smsquery["信息查询"])

    def sms_query(self):
        """"点击短信查询"""
        log.info("点击 短信查询")
        self.js_click(smsquery["短信查询"])
        self.js_click(smsquery["查询按钮"])

    def to_sms_query(self):
        """进入短信查询列表"""
        log.info("进入短信查询列表")
        self.order_processing()
        self.information_service()
        sleep(0.5)
        self.sms_query()

    def get_verification_code(self, phone_number): # 若验证码不在第一页，暂时先不处理
        """获取验证码"""
        log.info("获取--{0}--验证码".format(phone_number))
        verification_code = ""
        for number in range(1, 20, 2):
            page_phone = self.get_phone_number(number)
            log.info("网页号码：{0}，查询手机号码：{1}".format(page_phone, phone_number))
            if page_phone == phone_number:
                sms_text = self.get_sms_detail(number)
                if "验证码" in sms_text:
                    verification_code = self.get_code(sms_text)
                    break
        return verification_code

    def get_phone_number(self, row_num):
        """获取手机号"""
        log.info("获取手机号")
        locator = self.num_replace(smsquery["手机号列"], row_num)
        return self.element_text(locator)

    def get_sms_detail(self, row_num):
        """获取信息详情"""
        log.info("获取信息详情")
        self.mouse_over(self.num_replace(smsquery["内容详情列"], row_num))
        return self.element_text(smsquery["短信内容"])

    def get_code(self, sms_text):
        """提取短信中的验证码"""
        log.info("提取短信中的验证码")
        num = sms_text.index("验证码")
        return sms_text[num+4:num+10]

    def num_replace(self, tuple_data, rep_number):
        specific_path = str(tuple_data[1]).replace("[n]", "[{}]".format(rep_number))
        return tuple_data[0], specific_path

    def get_approval_H5_URL(self, approval_number): # 若验证码不在第一页，暂时先不处理
        """获取审批H5链接"""
        log.info("获取审批H5链接")
        H5_url = ""
        for number in range(1, 20, 2): # 循环遍历第一页短信
            send_scenario = self.get_send_scenario(number)
            log.info("发送场景:{0}".format(send_scenario))
            if send_scenario == "出差审批":
                sms_text = self.get_sms_detail(number)
                if approval_number in sms_text:
                    H5_url = self.get_approval_url(sms_text)
                    break
        return H5_url

    def get_approval_url(self, sms_text):
        """提取短信中的审批链接"""
        log.info("提取短信中的H5链接")
        num_start = sms_text.index("请点击链接")
        num_end = sms_text.index("进行审批")
        return sms_text[num_start+6:num_end]

    def get_authorization_H5_URL(self, order_id): # 若验证码不在第一页，暂时先不处理
        """获取授权H5链接"""
        log.info("获取订单-{0}-授权H5链接".format(order_id))
        H5_url = ""
        for row_number in range(1, 20, 2):
            page_order_id = self.get_order_id(row_number)
            send_scenario = self.get_send_scenario(row_number)
            log.info("网页订单号:{0}，发送场景:{1}".format(page_order_id, send_scenario))
            if (order_id == page_order_id) and ("授权邀约" in send_scenario):
                sms_text = self.get_sms_detail(row_number)
                H5_url = self.get_authorization_url(sms_text)
                break
        return H5_url

    def get_order_id(self, row_num):
        """获取短信订单号"""
        log.info("获取短信订单号")
        locator = self.num_replace(smsquery["订单号列"], row_num)
        return self.element_text(locator)

    def get_send_scenario(self, row_num):
        """获取短信订单号"""
        log.info("获取发送场景")
        locator = self.num_replace(smsquery["发送场景列"], row_num)
        return self.element_text(locator)

    def get_authorization_url(self, sms_text):
        """提取短信中的授权链接"""
        log.info("提取短信中的授权链接")
        num_start = sms_text.index("请点击")
        return sms_text[num_start+3:-3]

if __name__ == "__maim__":
    pass

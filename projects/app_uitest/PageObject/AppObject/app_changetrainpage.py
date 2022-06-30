from page.apppage import AppPage, sleep
from common.readelement import Element
from utils.logger import log

changetrain = Element('app', 'app_trainchange')

class AppChangeTrain(AppPage):
    """app改签火车票类"""

    def click_change_button(self):
        """点击改签"""
        log.info("点击改签按钮")
        self.swipe_down()
        self.is_click(changetrain["改签按钮"])

    def confirm_change(self): # 只有一个乘车人，改签的乘车人、时间、到达站就用默认值
        """确认改签"""
        log.info("点击确认改签按钮")
        self.is_click(changetrain["确认改签按钮"])
        # sleep()

    def choose_train(self):
        """选中车次"""
        log.info("选中第一个车次")
        self.is_click(changetrain["选中车次"])
        # sleep(2)

    def change_confirm(self):
        """点击改签按钮"""
        log.info("点击第一个可改签座次")
        self.find_elements(changetrain["改签"])[0].click()
        self.is_click(changetrain["确认改签按钮"])
        self.is_click(changetrain["确定"])
        # sleep(5)

    def pay_change_fare(self):
        """授信支付改签费用"""
        log.info("授信支付改签费用")
        self.is_click(changetrain["确认支付"])
        self.is_click(changetrain["授信支付"])
        # sleep(2)

    def get_change_apply_status(self):
        """获取改签申请状态"""
        log.info("获取改签申请状态")
        return self.element_text(changetrain["改签申请状态"])

    def click_view_order(self):
        """进入订单详情"""
        log.info("点击查看订单进入订单详情")
        self.is_click(changetrain["查看订单"])


if __name__ == "__maim__":
    pass

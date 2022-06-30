from page.apppage import AppPage, sleep
from common.readelement import Element
from utils.logger import log

returntrain = Element('app', 'app_trainreturn')

class AppReturnTrain(AppPage):
    """火车票退票类"""

    def click_return_button(self):
        """点击退票"""
        log.info("点击退票按钮")
        self.swipe_down()
        self.is_click(returntrain["退票"])

    def confirm_return(self): # 只有一个乘车人默认勾选了
        """确认退票"""
        log.info("点击按钮确认退票")
        self.is_click(returntrain["确认退票"])
        # sleep()
        self.is_click(returntrain["确定"])
        # sleep()

    def get_return_apply_status(self):
        """获取退票申请状态"""
        log.info("获取退票申请状态")
        return self.element_text(returntrain["退票申请状态"])

    def click_view_order(self):
        """进入订单详情"""
        log.info("点击查看订单进入订单详情")
        self.is_click(returntrain["查看订单"])

if __name__ == "__maim__":
    pass

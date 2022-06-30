from page.apppage import AppPage, sleep
from common.readelement import Element
from utils.logger import log

returnflight = Element('app', 'app_flightreturn')

class AppReturnFlight(AppPage):
    """app国内机票退票类"""

    def back_to_home_page(self):
        """返回首页"""
        log.info("点击返回按钮返回首页")
        self.is_click(returnflight["返回"])
        self.is_click(returnflight["返回"])
        self.is_click(returnflight["首页"])

    def click_return_button(self):
        """点击退票"""
        log.info("点击退票按钮")
        self.swipe_down()
        self.is_click(returnflight["退票"])

    def choose_passenger(self):
        """选择乘机人"""
        log.info("选中乘机人")
        self.is_click(returnflight["选乘机人"])
        self.is_click(returnflight["下一步"])
        # sleep()

    def choose_route(self):
        """选择行程"""
        log.info("选中行程")
        self.is_click(returnflight["下一步"])
        # sleep(2)

    def get_order_status(self):
        """获取订单状态"""
        log.info("获取订单状态")
        self.is_click(returnflight["查看订单"])
        # sleep(2)
        return self.element_text(returnflight["订单状态"])

    def launch_app(self):
        """重新打开APP"""
        log.info("重新打开APP")
        self.driver.launch_app()
        sleep(2)

if __name__ == "__maim__":
    pass

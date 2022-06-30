from page.webpage import WebPage
from common.readelement import Element
from utils.logger import log

flight_return = Element('web', 'web_flightreturn')

class ReturnFlightPage(WebPage):
    """国内机票退票申请提交类"""

    def click_my_travel(self):
        log.info("点击我的商旅")
        self.js_click(flight_return["我的商旅"])

    def click_first_return(self):
        log.info("点击第一个退票按钮")
        self.js_click(flight_return["退票按钮"])

    def choose_return_reason(self):
        log.info("选择退票原因")
        self.roll_to_tagert(flight_return["下一步"])
        try:
            self.js_click(flight_return["退票原因"])
        except:
            pass
        self.click_next()

    def click_confirm_return(self):
        log.info("点击弹框确认按钮")
        self.js_click(flight_return["弹框确认"])

    def return_apply_status(self):
        log.info("获取退票申请提交状态")
        return self.element_text(flight_return["申请提交状态"])

    def get_order_id(self):
        log.info("获取订单号")
        self.element_text(flight_return["订单号"])
        return self.element_text(flight_return["订单号"])

    def submit_flight_return_apply(self):
        log.info("提交退票申请")
        self.click_my_travel()
        self.click_first_return()
        self.choose_return_reason()
        self.click_confirm_return()
        apply_status = self.return_apply_status()
        order_id = self.get_order_id()
        return apply_status, order_id

    def to_order_detail(self, order_id):
        log.info("进入订单详情")
        locator = flight_return["订单详情"]
        locator = (locator[0], locator[1].format(order_id))
        self.js_click(locator)

    def click_next(self):
        log.info("点击下一步")
        self.js_click(flight_return["下一步"])

    def choose_go_trip(self):
        log.info("点击去程")
        self.find_elements(flight_return["去程"])[0].click()

    def choose_return_trip(self):
        log.info("点击返程")
        self.find_elements(flight_return["去程"])[1].click()

    def choose_passenger(self):
        log.info("选中乘机人")
        self.find_elements(flight_return["乘机人"])[0].click()
        self.click_next()

    def choose_many_passenger(self):
        log.info("选中多个乘机人")
        eles = self.find_elements(flight_return["乘机人"])
        for ele in eles:
            ele.click()
        self.click_next()

    def go_trip_return_apply(self, order_id):
        log.info("提交去程退票申请")
        self.click_my_travel()
        self.to_order_detail(order_id)
        self.click_first_return()
        self.choose_return_reason()
        self.click_confirm_return()
        return self.return_apply_status()

    def click_return_trip(self):
        log.info("点击返程")
        self.js_click(flight_return["详情返程"])

    def return_trip_return_apply(self, order_id):
        log.info("提交返程退票申请")
        self.click_my_travel()
        self.to_order_detail(order_id)
        self.click_return_trip()
        self.click_first_return()
        self.choose_return_reason()
        self.click_confirm_return()
        return self.return_apply_status()

    def round_trip_return_apply(self):
        log.info("提交往返两程退票申请")
        self.click_my_travel()
        self.click_first_return()
        self.choose_go_trip()
        self.choose_return_trip()
        self.click_next()
        self.choose_passenger()
        self.choose_return_reason()
        self.click_confirm_return()
        apply_status = self.return_apply_status()
        order_id = self.get_order_id()
        return apply_status, order_id

    def many_people_return_apply(self):
        log.info("提交多人退票申请")
        self.click_my_travel()
        self.click_first_return()
        self.choose_many_passenger()
        self.choose_return_reason()
        self.click_confirm_return()
        apply_status = self.return_apply_status()
        order_id = self.get_order_id()
        return apply_status, order_id

if __name__ == "__maim__":
    pass

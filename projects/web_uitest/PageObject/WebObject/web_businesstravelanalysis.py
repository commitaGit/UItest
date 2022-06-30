from page.webpage import WebPage
from utils.logger import log
from common.readelement import Element

analysis = Element('web', 'web_travelanalysis')

class TravelAnalysisPage(WebPage):
    """前台商旅分析类"""

    def click_travel_analysis(self):
        log.info("点击 商旅分析")
        self.js_click(analysis["商旅分析"])

    def flight_orders(self):
        self.js_click(analysis["国内机票"])
        return self.element_exist(analysis["第一行"])

    def train_orders(self):
        self.js_click(analysis["国内火车票"])
        return self.element_exist(analysis["第一行"])

    def hotel_orders(self):
        self.js_click(analysis["国内酒店"])
        return self.element_exist(analysis["第一行"])

    def currency_orders(self):
        self.js_click(analysis["通用订单"])
        return self.element_exist(analysis["第一行"])

    def iflight_orders(self):
        self.js_click(analysis["国际•港澳台机票"])
        return self.element_exist(analysis["第一行"])

    def ihotel_orders(self):
        self.js_click(analysis["国际•港澳台酒店"])
        return self.element_exist(analysis["第一行"])

    def travel_apply_orders(self):
        self.js_click(analysis["出差申请"])
        return self.element_exist(analysis["第一行"])

    def click_report_analysis(self):
        self.js_click(analysis["报表分析"])
        self.js_click(analysis["国内机票报表分析"])

    def non_lowest_price(self):
        self.js_click(analysis["未预定最低价"])
        return self.element_exist(analysis["报表第一行"])

    def delay_authorization_loss(self):
        self.js_click(analysis["延迟授权损失"])
        return self.element_exist(analysis["报表第一行"])

    def change_analysis(self):
        self.js_click(analysis["改签分析"])
        return self.element_exist(analysis["报表第一行"])

    def change_authorization_analysis(self):
        self.js_click(analysis["改签授权分析"])
        return self.element_exist(analysis["报表第一行"])

    def return_analysis(self):
        self.js_click(analysis["退票分析"])
        return self.element_exist(analysis["报表第一行"])

    def return_authorization_analysis(self):
        self.js_click(analysis["退票授权分析"])
        return self.element_exist(analysis["报表第一行"])

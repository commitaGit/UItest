import datetime, calendar
from minium import logger
from base.basepage import BasePage
from common.readconfig import ini
from time import sleep

HOTEL_PERSON = ini._get("STAFF", "HOTELPERSON")

class DomesticHotelPage(BasePage):

    def search_hotel(self):
        logger.info("查询酒店")
        # self.mini.page.get_element("view", inner_text="酒店", max_timeout=20).click()
        # self.mini.page.get_element("iconfont[is='components/icon-iconfont/index']", max_timeout=20).click()
        self.mini.page.get_element_by_xpath("/page/view[1]/view[2]/view[1]/view[1]/view[1]", max_timeout=20).click()
        self.choose_dates()
        self.mini.page.get_element("button", inner_text="查 询").click()
        elems = self.mini.page.get_elements(".hotel-item.d-flex", max_timeout=20)
        elems[0].click()

    def choose_dates(self):
        logger.info("选择入住及离店日期")
        self.mini.page.get_element(".flex-1.p-r-8.d-flex").click()
        start_date, end_date, next_month = self.get_dates_index()
        if next_month:
            self.mini.page.get_elements("view[data-index='{0}']".format(start_date))[1].click()
            self.mini.page.get_elements("view[data-index='{0}']".format(end_date))[1].click()
        else:
            self.mini.page.get_element("view[data-index='{0}']".format(start_date)).click()
            self.mini.page.get_element("view[data-index='{0}']".format(end_date)).click()

    def get_dates_index(self):
        logger.info("获取入住及离店日期索引值")
        temp_date = datetime.datetime.now()
        cur_month = int(temp_date.strftime("%Y%m%d")[4:6])
        cur_year = int(temp_date.strftime("%Y%m%d")[:4])
        cur_day = int(temp_date.strftime("%Y%m%d")[6:9])
        cur_month_days = calendar._monthlen(cur_year, cur_month)
        days_value = cur_month_days - cur_day
        if days_value < 3:
            start_date = 0
            end_date = 2
            next_month = True
        else:
            start_date = cur_day + 1
            end_date = cur_day + 3
            next_month = False
        return start_date, end_date, next_month

    def choose_hotel(self):
        logger.info("选择预订酒店")
        self.mini.page.get_element("view", inner_text="代理商A", max_timeout=15).click()
        if self.click_book_button():
            return True
        self.mini.page.get_element("view", inner_text="代理商B", max_timeout=15).click()
        if self.click_book_button():
            return True
        return False

    def click_book_button(self):
        logger.info("预订可退订的房型")
        room_elements = self.mini.page.get_elements("//room-list/view")   # 床型数量
        for number in range(len(room_elements)):
            return_rule = room_elements[number].get_element(".room-more.m-b-4").inner_text # 退订规则
            button_xpath = "//room-list/view[{0}]/view[1]/view[3]/button[1]".format(number+1)
            if ("不可退订" not in return_rule) and (self.mini.page.element_is_exists(button_xpath)): # 可退订并有预订按钮
                self.mini.page.get_element_by_xpath(button_xpath).click()
                return True
        return False

    def choose_occupant(self, check_person=HOTEL_PERSON):
        logger.info("选择入住人")
        self.mini.page.get_element(".iconfont.icon-add-people").click()
        e = self.mini.page.get_element('input[placeholder="搜索"]')
        e.trigger("input", {"value": check_person})
        sleep(1.5)
        self.mini.page.get_element('.iconfont.icon-radio-unselected').click()
        sleep(1)
        self.mini.page.get_element("button", inner_text="确定").click()

    def submit_order(self):
        logger.info("提交并支付订单")
        self.mini.page.get_element("button", inner_text="提交订单").click()
        self.mini.page.get_element("button", inner_text="支付").click()
        self.mini.page.get_element("text", inner_text="查看订单").click()

    def get_order_id(self):
        logger.info("获取订单号")
        return self.mini.page.get_element_by_xpath("/page/page-meta/view/view/view/view[2]/view[1]").inner_text

    def go_order_list(self):
        logger.info("进去订单列表")
        self.mini.page.get_element("view", inner_text="我的").click()
        self.mini.page.get_element("view", inner_text="全部订单").click()

    def book_hotel(self):
        logger.info("预订酒店")
        self.search_hotel()
        assert self.choose_hotel(), "没有可退订房型"
        self.choose_occupant()
        self.submit_order()
        return self.get_order_id()[4:]

    def all_return(self):
        logger.info("提交全部退订申请")
        self.mini.app.go_home()
        self.go_order_list()
        self.mini.page.get_element(".order-item").click()
        sleep(1)
        self.mini.page.get_element("view", inner_text="退订").click()
        self.mini.page.get_element("view[class='submit-btn']", inner_text="确认退订").click()
        return self.mini.page.element_is_exists("view", inner_text="提交成功")

    def partial_return(self):
        logger.info("提交部分退订申请")
        self.mini.app.go_home()
        self.go_order_list()
        self.mini.page.get_element(".order-item").click()
        self.mini.page.get_element("view", inner_text="退订").click()
        self.mini.page.get_element("view", inner_text="部分退订").click()
        self.mini.page.get_element(".date-item").click()
        self.mini.page.get_element("view[class='submit-btn']", inner_text="确认退订").click()
        sleep(1)
        return self.mini.page.element_is_exists("view", inner_text="提交成功")

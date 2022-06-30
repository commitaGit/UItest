import minium
from minium import logger
from time import sleep
from selenium import webdriver
from pages.applet_domestichotelpage import DomesticHotelPage
from pages.web_domestichotelhandlepage import DomesticHotelOrderHandlePage
from pages.web_adminloginpage import AdminLoginPage
from pages.web_multiplesearchpage import MultipleSearchPage
from common.casedependency import CaseDependency

ORDER_ID = ""
DRIVER = webdriver.Chrome()

class DomesticHotelTest(minium.MiniTest):

    def __init__(self, methodName='runTest'):
        super(DomesticHotelTest, self).__init__(methodName)
        self.hotel_page = DomesticHotelPage(self)

    def reservation_confirmation(self, order_id):
        """国内酒店订房确认"""
        if not self.search_order_status(order_id, "已确认"):
            return DomesticHotelOrderHandlePage(DRIVER).reservation_confirm(order_id)
        return True

    def search_order_status(self, order_id, status):
        """查询订单状态"""
        assert AdminLoginPage(DRIVER).admin_logins(), "web后台登录失败"
        search = MultipleSearchPage(DRIVER)
        order_status = search.domestic_hotel_order_status(order_id)
        check = False
        n = 0
        while n < 20:
            if status in order_status:
                check = True
                break
            search.click_search()
            order_status = search.get_domestic_hotel_status()
            n += 1
            sleep(1)
        return check

    def all_cancel_room_confirm(self, order_id):
        """国内酒店全部退房确认"""
        if not self.search_order_status(order_id, "已退订"):
            return DomesticHotelOrderHandlePage(DRIVER).all_cancel_room(order_id)
        return True

    def part_cancel_room_confirm(self, order_id):
        """国内酒店部分退房确认"""
        assert AdminLoginPage(DRIVER).admin_logins(), "web后台登录失败"
        return DomesticHotelOrderHandlePage(DRIVER).part_cancel_room(order_id)

    @CaseDependency(name="test_01_book")
    def test_01_book(self):
        """小程序--国内酒店-预订酒店"""
        global ORDER_ID
        ORDER_ID = self.hotel_page.book_hotel()

    @CaseDependency(name="test_02_book_confirm", depend="test_01_book")
    def test_02_book_confirm(self):
        """小程序-国内酒店--完成订房"""
        global ORDER_ID
        assert self.reservation_confirmation(ORDER_ID), "完成订房任务失败"

    @CaseDependency(name="test_03_return_apply", depend="test_02_book_confirm")
    def test_03_return_apply(self):
        """小程序-国内酒店--提交全部退房申请"""
        logger.info("提交全部退房申请")
        assert self.hotel_page.all_return(), "提交全部退房申请失败"

    @CaseDependency(depend="test_03_return_apply")
    def test_04_return_confirm(self):
        """小程序-国内酒店--完成全部退房任务"""
        logger.info("完成全部退房任务")
        assert self.all_cancel_room_confirm(ORDER_ID), "后台全部退房任务失败"

    @CaseDependency(name="test_05_partial_return_apply", depend="test_01_book")
    def test_05_partial_return_apply(self):
        """小程序-国内酒店--提交部分退房申请"""
        logger.info("提交部分退房申请")
        global ORDER_ID
        ORDER_ID = self.hotel_page.book_hotel()
        assert self.reservation_confirmation(ORDER_ID), "完成订房任务失败"
        assert self.hotel_page.partial_return(), "提交部分退房申请失败"

    @CaseDependency(depend="test_05_partial_return_apply")
    def test_06_partial_return_confirm(self):
        """小程序-国内酒店--完成部分退房任务"""
        logger.info("完成部分退房任务")
        assert self.part_cancel_room_confirm(ORDER_ID), "后台全部退房任务失败"

    def test_07_clear(self):
        """小程序--关闭浏览器"""
        DRIVER.quit()

if __name__ == "__main__":
    import unittest
    loaded_suite = unittest.TestLoader().loadTestsFromTestCase(DomesticHotelTest)
    print(loaded_suite)
    result = unittest.TextTestRunner().run(loaded_suite)
    print(result)





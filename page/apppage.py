"""
selenium基类
本文件存放了selenium基类的封装方法
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.touch_action import TouchAction
from config.conf import cm
from utils.times import sleep
from utils.logger import log


class AppPage(object):
    """selenium基类"""

    def __init__(self, app_driver):
        # self.driver = cm.get_driver()
        self.driver = app_driver
        self.timeout = 20
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.dt = 2000

    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(cm.APP_LOCATE_MODE[name], value)

    def find_element(self, locator):
        """寻找单个元素"""
        log.info("查找元素:{}".format(locator))
        try:
            # 元素可见时，返回查找到的元素；以下入参为元组的元素，需要加*
            return AppPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_element_located(args)), locator)
        except NoSuchElementException:
            log.error('Can not find element: %s' % locator[1])
            raise
        except TimeoutException:
            log.error('Can not find element: %s' % locator[1])
            raise

    def find_elements(self, locator):
        """查找多个相同的元素"""
        log.info("查找元素:{}".format(locator))
        try:
            return AppPage.element_locator(lambda *args: self.wait.until(
                EC.presence_of_all_elements_located(args)), locator)
        except NoSuchElementException:
                log.error('Can not find element: %s' % locator[1])
                raise

    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        log.info("相同元素：{}".format((locator, number)))
        return number

    def input_text(self, locator, txt):
        """输入(输入前先清空)"""
        log.info("输入文本：{}".format(txt))
        ele = self.find_element(locator)
        ele.clear()
        ele.send_keys(txt)

    def is_click(self, locator):
        """点击"""
        log.info("点击元素：{}".format(locator))
        self.find_element(locator).click()
        sleep()

    def element_text(self, locator):
        """获取当前的text"""
        _text = self.find_element(locator).text
        log.info("获取文本：{}".format(_text))
        return _text

    def js_click(self, locator):
        """用js注入方式点击"""
        log.info("js注入方式点击元素：{}".format(locator))
        element = self.find_element(locator)
        self.driver.execute_script('arguments[0].click()', element)
        sleep()

    def swipe_left(self):
        """左滑"""
        log.info("屏幕左滑")
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        self.driver.swipe(x*3/4,y/4,x/4,y/4)

    def swipe_right(self):
        """右滑"""
        log.info("屏幕右滑")
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        self.driver.swipe(x/4,y/4,x*3/4,y/4)

    def swipe_down(self):
        """下滑"""
        log.info("屏幕下滑")
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        self.driver.swipe(x/2,y/4,x/2,y*3/4,self.dt)

    def swipe_up(self):
        """上滑"""
        log.info("屏幕上滑")
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        self.driver.swipe(x/2,y*3/4,x/2,y/4,self.dt)

    def touch_location(self, x1, y1):
        """
        :param
        x1:x坐标的相对值，绝对值/分辨率，eg:绝对位置是200，分辨率是720，则传入200/720
        y1:y坐标的相对值
        """
        log.info("通过坐标点击元素")
        x = self.driver.get_window_size()['width']
        y= self.driver.get_window_size()['height']
        log.info("元素坐标：x={0},y={1}".format(x1*x, y1*y))
        TouchAction(self.driver).press(x=x1*x, y=y1*y).release().perform()

    def element_exist(self, locator):
        """判断元素是否存在"""
        try:
            log.info("查找元素:{}".format(locator))
            self.driver.find_element(by=locator[0], value=locator[1])
        except NoSuchElementException:
            log.info("元素：{0}不存在".format(locator))
            return False
        return True
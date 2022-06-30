"""
selenium基类
本文件存放了selenium基类的封装方法
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from minium import logger
from time import sleep
LOCATE_MODE = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'name': By.NAME,
        'id': By.ID,
        'class': By.CLASS_NAME,
        'tag': By.TAG_NAME
    }

class WebPage(object):
    """selenium基类"""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 20
        self.wait = WebDriverWait(self.driver, self.timeout)

    def get_url(self, url):
        """打开网址并验证"""
        try:   # 页面窗口可能已经最大化了
            self.driver.maximize_window()
        except:
            pass
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            logger.info("打开网页：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(LOCATE_MODE[name], value)

    def find_element(self, locator):
        """寻找单个元素"""
        logger.info("查找元素:{}".format(locator))
        try:
            return WebPage.element_locator(lambda *args: self.wait.until(
                EC.presence_of_element_located(args)), locator)
        except NoSuchElementException:
            logger.error('Can not find element: %s' % locator[1])
            raise

    def find_elements(self, locator):
        """查找多个相同的元素"""
        logger.info("查找元素:{}".format(locator))
        try:
            return WebPage.element_locator(lambda *args: self.wait.until(
                EC.presence_of_all_elements_located(args)), locator)
        except NoSuchElementException:
                logger.error('Can not find elements: %s' % locator[1])
                raise

    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        logger.info("相同元素：{}".format((locator, number)))
        return number

    def input_text(self, locator, txt):
        """输入(输入前先清空)"""
        # sleep(0.5)
        ele = self.find_element(locator)
        ele.clear()
        ele.send_keys(txt)
        logger.info("输入文本：{}".format(txt))

    def is_click(self, locator):
        """点击"""
        self.find_element(locator).click()
        sleep(0.5)
        logger.info("点击元素：{}".format(locator))

    def element_text(self, locator):
        """获取当前的text"""
        _text = self.find_element(locator).text
        logger.info("获取文本：{}".format(_text))
        return _text

    def js_click(self, locator):
        """用js注入方式点击"""
        element = self.find_element(locator)
        self.driver.execute_script('arguments[0].click()', element)
        sleep(0.5)
        logger.info("js注入方式点击元素：{}".format(locator))

    def roll_to_tagert(self, locator):
        """滚动到指定位置"""
        target = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        sleep(0.5)

    def mouse_over(self, locator):
        """鼠标移动到指定位置"""
        move = self.find_element(locator)
        ActionChains(self.driver).move_to_element(move).perform()

    def get_confirm(self):
        """处理确认类弹框"""
        alert = self.driver.switch_to.alert # 切换到弹框
        alert_test = alert.text  # 获取弹框文本
        alert.accept()
        return alert_test

    @property
    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)

    def input_BackSpace(self, locator):
        """键盘输入删除键"""
        ele = self.find_element(locator)
        ele.send_keys(Keys.BACK_SPACE)

    def element_exist(self, locator):
        """判断元素是否存在"""
        try:
            logger.info("查找元素:{}".format(locator))
            self.driver.find_element(by=locator[0], value=locator[1])
        except NoSuchElementException:
            logger.info("元素：{0}不存在".format(locator))
            return False
        return True

    def element_visible(self, locator):
        """判断元素是否可见"""
        ele = self.find_element(locator)
        return ele.is_displayed()

class BasePage:
    def __init__(self, mini):
        self.mini = mini

    def navigate_to_open(self, route):
        """以导航的方式跳转到指定页面,不允许跳转到 tabbar 页面,支持相对路径和绝对路径, 小程序中页面栈最多十层"""
        self.mini.app.navigate_to(route)

    def redirect_to_open(self, route):
        """关闭当前页面，重定向到应用内的某个页面,不允许跳转到 tabbar 页面"""
        self.mini.app.redirect_to(route)

    def switch_tab_open(self, route):
        """跳转到 tabBar 页面,会关闭其他所有非 tabBar 页面"""
        self.mini.app.switch_tab(route)

    @property
    def current_title(self) -> str:
        """获取当前页面 head title, 具体项目具体分析,以下代码仅用于演示"""
        return self.mini.page.get_element("XXXXXX").inner_text

    def current_path(self) -> str:
        """获取当前页面route"""
        return self.mini.page.path

    def check_element(self):
        """页面元素审查
        在子类中实现此方法时，建议使用Minium框架中提供的断言方法，原因如下：
        调用 Minium 框架提供的断言方法，会拦截 assert 调用，记录运行时数据和截图，自动在测试报告
        中生成截图 (需要在配置文件中将 assert_capture 设置为True)
        但是如果直接assert或使用unittest.TestCase提供的断言，当断言失败时，无法自动生成截图
        """
        raise NotImplementedError

    @property
    def current_route(self) -> str:
        """获取当前页面route, 具体项目具体分析, 以下代码仅用于演示"""
        return self.mini.app.get_current_page().path

    def _open(self, route, open_type=None):
        """
        小程序页面跳转可以使用以下三个方法, 一些区别如下：
        1.`navigate_to`: 此方法会保留当前页面，并跳转到应用内的某个页面(不能跳到tabbar页面). 小程序中页面栈最多十层, 如果超过十层时，再使用此方法
        跳转页面, 会抛出以下异常：`minium.framework.exception.MiniAppError: webview count limit exceed`. 因此需要在运行用例后及时清除页面栈;
        2. `redirect_to`: 关闭当前页面，重定向到应用内的某个页面，使用此方法跳转页面时，会替换页面栈，因此页面栈不会超限，但是也导致不支持页面回退;
        3. `relaunch`: 关闭所有页面，清空页面栈，打开到应用内的某个页面;
        """
        open_type = 'redirect' if open_type is None else open_type

        if open_type.lower() == "navigate":
            self.mini.app.navigate_to(route)
        elif open_type.lower() == "redirect":
            self.mini.app.redirect_to(route)
        else:
            self.mini.app.relaunch(route)


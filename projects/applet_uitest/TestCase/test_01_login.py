import minium
from pages.applet_loginpage import LoginPage

class LoginTest(minium.MiniTest):

    def __init__(self, methodName='runTest'):
        super(LoginTest, self).__init__(methodName)
        self.login = LoginPage(self)

    def test_01_login(self):
        """小程序--登录"""
        self.mini.native.start_wechat()
        for number in range(4):
            if number == 3:
                assert False, "登录失败"
            if self.login.login():
                assert True
                return

if __name__ == "__main__":
    import unittest
    loaded_suite = unittest.TestLoader().loadTestsFromTestCase(LoginTest)
    result = unittest.TextTestRunner().run(loaded_suite)
    print(result)



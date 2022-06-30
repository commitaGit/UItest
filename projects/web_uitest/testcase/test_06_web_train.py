import pytest
from projects.web_uitest.PageObject.WebObject.web_trainpage import TrainPage
from common.customerlogin import CustomerLogin

class TestTrain:

    @pytest.mark.dependency(name='book')
    def test_001(self, drivers):
        """WEB-预订火车票"""
        pass
        # CustomerLogin(drivers).customer_login()
        # train = TrainPage(drivers)
        # assert "支付成功" in train.book_train()
        # train.click_view_book_order()
        # assert "已出票" in train.get_order_status()

    @pytest.mark.dependency(name='change', depends=["book"])
    def test_002(self, drivers): # todo 改签无车次的情况
        """WEB-火车票改签"""
        pass
        # train = TrainPage(drivers)
        # assert "改签申请已成功提交" in train.submit_change_apply()
        # train.click_view_change_order()
        # assert "已出票" in train.get_order_status()

    @pytest.mark.dependency(depends=["change"])
    def test_003(self, drivers):
        """WEB-火车票退票"""
        pass
        # train = TrainPage(drivers)
        # assert "退票申请已成功提交" in train.submit_return_apply()
        # train.click_view_return_order()
        # assert "已退票" in train.get_order_status()

if __name__ == '__main__':
    pytest.main(['testcase/test_06_web_train.py'])


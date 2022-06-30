import pytest
from app_uitest.PageObject.AppObject.app_changetrainpage import AppChangeTrain
from app_uitest.PageObject.AppObject.app_returtrainpage import AppReturnTrain
from app_uitest.PageObject.AppObject.app_booktrainpage import AppBookTrain


class TestAppTrain:

    def book_train(self, BOOK, departure_city="深圳", arrive_city="广州"):
        BOOK.click_train_product()
        BOOK.input_departure_city(departure_city)
        BOOK.input_arrive_city(arrive_city)
        BOOK.pick_date()
        BOOK.click_search()
        BOOK.click_train()
        BOOK.click_book()
        BOOK.choose_staff()
        BOOK.click_build_order()
        BOOK.click_pay()
        BOOK.click_credit_pay()

    @pytest.mark.dependency(name="book_train")
    def test_001(self, app_drivers):
        """APP-火车票预订"""
        BOOK = AppBookTrain(app_drivers)
        BOOK.launch_app()
        self.book_train(BOOK)
        assert "支付成功" in BOOK.get_pay_result()

    @pytest.mark.dependency(name="change_train", depends=["book_train"])
    def test_002(self, app_drivers):
        """APP-火车票改签"""
        BOOK = AppBookTrain(app_drivers)
        CHANGE = AppChangeTrain(app_drivers)
        BOOK.click_view_order()
        CHANGE.click_change_button()
        CHANGE.confirm_change()
        CHANGE.choose_train()
        CHANGE.change_confirm()
        CHANGE.pay_change_fare()
        assert "改签申请提交成功" in CHANGE.get_change_apply_status()

    @pytest.mark.dependency(depends=["change_train"])
    def test_003(self, app_drivers):
        """APP-火车票退票"""
        CHANGE = AppChangeTrain(app_drivers)
        CHANGE.click_view_order()
        RETURN = AppReturnTrain(app_drivers)
        RETURN.click_return_button()
        RETURN.confirm_return()
        assert "退票申请提交成功" in RETURN.get_return_apply_status()

if __name__ == '__main__':
    pytest.main(['testcase/test_03_app_train.py'])
    pass


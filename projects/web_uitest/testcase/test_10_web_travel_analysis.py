import pytest
from projects.web_uitest.PageObject.WebObject.web_businesstravelanalysis import TravelAnalysisPage
from common.customerlogin import CustomerLogin


class TestTravelAnalysis:

    def test_01(self, drivers):
        """WEB-商旅分析--综合查询"""
        CustomerLogin(drivers).customer_login()
        analysis = TravelAnalysisPage(drivers)
        analysis.click_travel_analysis()
        pytest.assume(analysis.flight_orders())
        pytest.assume(analysis.train_orders())
        pytest.assume(analysis.hotel_orders())
        pytest.assume(analysis.currency_orders())
        pytest.assume(analysis.iflight_orders())
        pytest.assume(analysis.ihotel_orders())
        pytest.assume(analysis.travel_apply_orders())

    def test_02(self, drivers):
        """WEB-商旅分析--报表分析"""
        analysis = TravelAnalysisPage(drivers)
        analysis.click_report_analysis()
        pytest.assume(analysis.non_lowest_price())
        pytest.assume(analysis.delay_authorization_loss())
        pytest.assume(analysis.change_analysis())
        pytest.assume(analysis.change_authorization_analysis())
        pytest.assume(analysis.return_analysis())
        pytest.assume(analysis.return_authorization_analysis())

if __name__ == '__main__':
    pytest.main(['testcase/test_10_web_travel_analysis.py'])



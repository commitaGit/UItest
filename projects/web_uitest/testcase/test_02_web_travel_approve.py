import pytest
from projects.web_uitest.PageObject.WebObject.web_msmquerypage import SmsQueryPage
from projects.web_uitest.PageObject.WebObject.web_travelplanpage import SubmitTravelPlanPage
from projects.web_uitest.PageObject.WebObject.web_approvalH5page import ApprovalPage
from projects.web_uitest.PageObject.WebObject.web_approvalsettingpage import ApprovalSettingPage
from projects.web_uitest.PageObject.WebObject.web_mytrippage import MyTripPage
from common.adminlogin import AdminLogin
from common.customerlogin import CustomerLogin


APPROVALNO = ""

class TestTravelApprove:

    def submit_travel_plan(self, drivers):
        """提交差旅计划"""
        global APPROVALNO
        if not CustomerLogin(drivers).customer_login():
            return False
        submit = SubmitTravelPlanPage(drivers)
        submit.click_travel_plan()
        submit.input_travel_reason("测试测试")
        submit.input_travel_destination("深圳")
        submit.travel_time()
        submit.travel_staff()
        submit.click_submit()
        if "提交成功" in submit.get_submit_status():
            APPROVALNO = submit.get_approval_number()
            return True
        return False

    def get_approve_H5_url(self, drivers, approval_number):
        """获取审批的H5链接"""
        login_result = AdminLogin(drivers).admin_sign()
        if not login_result:
            return False
        sms = SmsQueryPage(drivers)
        sms.to_sms_query()
        return sms.get_approval_H5_URL(approval_number)

    def approval_agree(self, drivers, approval_number):
        """审批通过"""
        H5_URL = self.get_approve_H5_url(drivers, approval_number)
        approve = ApprovalPage(drivers)
        approve.get_url(H5_URL)
        approve.click_agree()

    def approval_refuse(self, drivers, approval_number):
        """审批拒绝"""
        H5_URL = self.get_approve_H5_url(drivers, approval_number)
        approve = ApprovalPage(drivers)
        approve.get_url(H5_URL)
        approve.click_refuse()

    def get_one_level_status(self, drivers, approval_number):
        """获取前台审批单一级审批状态"""
        CustomerLogin(drivers).customer_login()
        status = MyTripPage(drivers)
        status.to_approval_detail(approval_number)
        return status.one_level_status()

    def get_two_level_status(self, drivers, approval_number):
        """获取前台审批单二级审批状态"""
        CustomerLogin(drivers).customer_login()
        status = MyTripPage(drivers)
        status.to_approval_detail(approval_number)
        return status.two_level_status()

    def test_001(self, drivers):
        """WEB-设置只需一级审批"""
        assert CustomerLogin(drivers).customer_login(), "web前台登录失败"
        setting = ApprovalSettingPage(drivers)
        setting.to_approval_setting()
        if setting.secondary_approver_exist():
            setting.click_basics_change()
            setting.clear_secondary_approver()
            setting.click_save()
        assert not setting.secondary_approver_exist()

    @pytest.mark.dependency(name="travel_plan")
    def test_002(self, drivers):
        """WEB-提交差旅计划"""
        submit = SubmitTravelPlanPage(drivers)
        assert self.submit_travel_plan(drivers)
        assert "提交成功" in submit.get_submit_status()

    @pytest.mark.dependency(depends=["travel_plan"])
    def test_003(self, drivers):
        """WEB-一级审批通过"""
        self.approval_agree(drivers, APPROVALNO)
        approve = ApprovalPage(drivers)
        assert "审批通过" in approve.approve_status_one()
        # assert "审批通过" in self.get_one_level_status(drivers, APPROVALNO)

    @pytest.mark.dependency(depends=["travel_plan"])
    def test_004(self, drivers):
        """WEB-一级审批拒绝"""
        assert self.submit_travel_plan(drivers), "提交出差申请失败"
        self.approval_refuse(drivers, APPROVALNO)
        approve = ApprovalPage(drivers)
        assert "审批拒绝" in approve.approve_status_one()
        # assert "审批拒绝" in self.get_one_level_status(drivers, APPROVALNO)

    @pytest.mark.dependency(name="secondary_approve")
    def test_005(self, drivers):
        """WEB-设置二级审批人"""
        assert CustomerLogin(drivers).customer_login(), "web前台登录失败"
        setting = ApprovalSettingPage(drivers)
        setting.to_approval_setting()
        if not setting.secondary_approver_exist():
            setting.click_basics_change()
            setting.input_secondary_approver()
            setting.click_save()
        assert setting.secondary_approver_exist()

    @pytest.mark.dependency(depends=["secondary_approve", "travel_plan"])
    def test_006(self, drivers):
        """WEB-二级审批通过"""
        assert self.submit_travel_plan(drivers)
        self.approval_agree(drivers, APPROVALNO)
        self.approval_agree(drivers, APPROVALNO)
        approve = ApprovalPage(drivers)
        assert "审批通过" in approve.approve_status_two()
        # assert "审批通过" in self.get_two_level_status(drivers, APPROVALNO)

    @pytest.mark.dependency(depends=["secondary_approve", "travel_plan"])
    def test_007(self, drivers):
        """WEB-二级审批拒绝"""
        assert self.submit_travel_plan(drivers), "提交出差申请失败"
        self.approval_agree(drivers, APPROVALNO)
        self.approval_refuse(drivers, APPROVALNO)
        approve = ApprovalPage(drivers)
        assert "审批拒绝" in approve.approve_status_two()
        # assert "审批拒绝" in self.get_two_level_status(drivers, APPROVALNO)

if __name__ == '__main__':
    pytest.main(['testcase/test_02_web_travel_approve.py'])

import random
from page.webpage import WebPage, sleep
from utils.logger import log
from common.readelement import Element
from utils.excel import OperateExcel
from faker import Faker

register = Element('web', 'web_register')
faker = Faker(locale='zh_CN')
ope_excel = OperateExcel("register.xls", "机构注册")


class RegisterPage(WebPage):
    """后台注册类"""

    def operation_management(self):
        """点击运营管理"""
        log.info("点击 运营管理")
        self.js_click(register["运营管理"])

    def travel_department(self):
        """点击商旅事业部--机构客户"""
        log.info("点击 商旅事业部--机构客户")
        self.js_click(register["商旅事业部"])

    def add_button(self):
        """"点击新增按钮"""
        log.info("点击 新增按钮")
        self.js_click(register["新增按钮"])

    def travel_dep_add(self):
        """商旅事业部新增"""
        self.operation_management()
        self.travel_department()
        self.add_button()

    def customer_type_tmc(self):
        """选中客户类型--tmc"""
        log.info("选中客户类型--tmc")
        self.is_click(register["客户类型"])
        self.is_click(register["TMC"])

    def customer_type_gp(self):
        """选中客户类型--GP机构"""
        log.info("选中客户类型--GP机构")
        self.is_click(register["客户类型"])
        self.is_click(register["GP机构"])

    def full_customer_name(self):
        """输入客户全称"""
        log.info("输入客户全称")
        full_name = faker.company()
        self.input_text(register["客户全称"], txt=full_name)
        ope_excel.write_value(1, 1, full_name)
        return full_name

    def shot_customer_name(self, shot_name):
        """输入客户简称"""
        log.info("输入客户简称")
        self.input_text(register["客户简称"], txt=shot_name)

    def member_id(self):
        """输入会员号"""
        log.info("输入会员号")
        menber_id = "TH{0}".format(random.randint(1000000000, 9999999999))
        self.input_text(register["会员号"], txt=menber_id)
        ope_excel.write_value(1, 3, menber_id)

    def customer_scale(self):
        """选择客户规模"""
        log.info("选择客户规模")
        self.is_click(register["客户规模"])
        self.is_click(self.num_replace(register["具体规模"], 4))

    def business_status(self):
        """选择业务状态"""
        log.info("选择业务状态")
        self.is_click(register["业务状态"])
        self.is_click(self.num_replace(register["具体状态"], 3))

    def industry(self):
        """选择所属行业"""
        log.info("选择所属行业")
        self.is_click(register["所属行业"])
        self.is_click(self.num_replace(register["具体行业"], 13))

    def credit_rating(self):
        """选择信用等级"""
        log.info("选择信用等级")
        self.is_click(register["信用等级"])
        self.is_click(self.num_replace(register["具体等级"], 3))

    def customer_address(self):
        """选择省市区"""
        log.info("选择省-市-区")
        self.is_click(register["客户地址"])
        self.is_click(self.num_replace(register["省"], 31))
        self.is_click(register["市"])
        self.is_click(self.num_replace(register["区"], 3))

    def specific_address(self):
        """输入具体地址"""
        log.info("输入具体地址")
        address = faker.street_address()
        self.input_text(register["详细地址"], txt=address)
        ope_excel.write_value(1, 4, address)

    def customer_info(self):
        """填写客户信息"""
        log.info("填写客户信息")
        self.customer_scale()
        self.business_status()
        self.industry()
        self.credit_rating()
        self.customer_address()

    def sales_manager(self):
        """选择销售经理"""
        log.info("选择销售经理")
        self.is_click(register["销售经理"])
        self.multiple_click(register["可选销售经理"], 15)
        self.js_click(register["销售经理"])

    def customer_manager(self):
        """选择客服经理"""
        log.info("选择客服经理")
        self.is_click(register["客服经理"])
        self.multiple_click(register["可选客服经理"], 15)
        self.js_click(register["客服经理"])

    def settlement_manager(self):
        """选择结算经理"""
        log.info("选择结算经理")
        self.is_click(register["结算经理"])
        self.multiple_click(register["可选结算经理"], 15)
        self.js_click(register["结算经理"])

    def maintain_manager(self):
        """选择维护经理"""
        log.info("选择维护经理")
        self.is_click(register["维护经理"])
        self.multiple_click(register["可选维护经理"], 15)
        self.js_click(register["维护经理"])

    def service_info(self):
        """填写服务信息"""
        log.info("填写服务信息")
        self.sales_manager()
        self.customer_manager()
        self.settlement_manager()
        self.maintain_manager()

    def contact_name(self):
        """输入联系人姓名"""
        log.info("输入联系人姓名")
        contant_name = faker.name()
        self.roll_to_tagert(register["联系人姓名"])
        self.input_text(register["联系人姓名"], txt=contant_name)
        ope_excel.write_value(1, 5, contant_name)

    def contact_phone_and_mail(self):
        """输入联系人手机号"""
        log.info("输入联系人手机号和邮箱")
        contact_phone = "111{0}".format(random.randint(10000000, 99999999))
        contact_mail = "{0}@tehang.com".format(contact_phone)
        self.roll_to_tagert(register["联系人手机"])
        self.input_text(register["联系人手机"], txt=contact_phone)
        self.roll_to_tagert(register["联系人邮箱"])
        self.input_text(register["联系人邮箱"], txt=contact_mail)
        ope_excel.write_value(1, 6, contact_phone)
        ope_excel.write_value(1, 7, contact_mail)
        return contact_phone

    def open_products(self): # 开通所有产品
        """选择开通产品"""
        log.info("开通产品")
        self.roll_to_tagert(register["开通产品"])
        self.is_click(register["开通产品"])
        product_number = len(self.find_elements(register["产品数量"]))
        locator = register["可选产品"]
        for number in range(1, product_number+1):
            pro_locator = (locator[0], str(locator[1]).replace("[n]", "[{}]".format(number)))
            self.is_click(pro_locator)
        self.js_click(register["开通产品"])

    def save_corp(self):
        log.info("提交机构数据")
        self.roll_to_tagert(register["保存"])
        self.is_click(register["保存"])
        sleep(6)

    def back_to_list(self):
        log.info("点击返回列表")
        self.roll_to_tagert(register["返回列表"])
        self.is_click(register["返回列表"])
        sleep()

    def get_corp_name(self):
        log.info("获取机构名称")
        return self.element_text(register["获取机构名"])

    def num_replace(self, tuple_data, maxnumber):
        """将locator中的n替换为数字"""
        number = random.randint(1, maxnumber)
        specific_path = str(tuple_data[1]).replace("[n]", "[{}]".format(number))
        return tuple_data[0], specific_path

    def multiple_click(self, locator, maxnumber):
        for number in range(1, 4):
            self.is_click(self.num_replace(locator, maxnumber))

if __name__ == "__maim__":
    pass

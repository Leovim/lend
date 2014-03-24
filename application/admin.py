#coding=utf8

import json
import tornado.web
from models import *
from config import options

# todo 后台管理功能
# todo 查看用户信息，查看用户贷款，查看用户行为，查看所有贷款，查看所有未完成贷款
# todo 修改用户贷款
# todo 还款状态，完成后需修改loan，behaviour，pay中相关字段的还款状态
# todo 担保关系审核
# todo 添加修改状态功能后，增加loan model中相关检查

class BaseHandler(tornado.web.RequestHandler):
    user_model = UserModel()
    guarantee_model = GuaranteeModel()
    loan_model = LoanModel()
    behaviour_model = BehaviourModel()
    split_model = SplitLoanModel()

    def get_current_user(self):
        user_id = self.get_secure_cookie("user", max_age_days=365)
        if not user_id:
            return None
        return True


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass


class AdminLoginHandler(BaseHandler):
    def get(self):
        self.render("nimda/login.html")


class AdminAuthenticateHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        if username == options.admin and password == options.password:
            self.set_secure_cookie("user", str(username), expires_days=365)
            result_json = json.dumps({'result': 1}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", result_json=result_json)
        else:
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", result_json=result_json)


class AdminUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, user_id):
        user_info = self.user_model.get_user_info(user_id)
        loans = self.loan_model.get_user_all_loans(user_id)
        for i, item in enumerate(loans):
            if item['check_status'] == 0:
                loans[i]['check_status'] = "待审核"
            elif item['check_status'] == 1:
                loans[i]['check_status'] = "正常"
            elif item['check_status'] == 2:
                loans[i]['check_status'] = "已完成"

            loans[i]['guarantor1_name'] = None
            loans[i]['guarantor2_name'] = None
            if item['guarantor1']:
                guarantor1 = self.user_model.get_user_info(item['guarantor1'])
                loans[i]['guarantor1_name'] = guarantor1['real_name']
            if item['guarantor2']:
                guarantor2 = self.user_model.get_user_info(item['guarantor2'])
                loans[i]['guarantor2_name'] = guarantor2['real_name']
        self.render("nimda/user.html", user_info=user_info, loans=loans)


class AdminLoanHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("nimda/loan.html")


class AdminGuaranteeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        guarantee = self.guarantee_model.get_all_guarantee()
        unchecked_guarantee = self.guarantee_model.get_all_unchecked_guarantee()
        for i, item in enumerate(guarantee):
            guarantor_info = self.user_model.\
                get_user_info(guarantee[i]['guarantor_id'])
            guarantee[i]['guarantor_name'] = guarantor_info['real_name']
            warrantee_info = self.user_model.\
                get_user_info(guarantee[i]['warrantee_id'])
            guarantee[i]['warrantee_name'] = warrantee_info['real_name']
        for i, item in enumerate(unchecked_guarantee):
            guarantor_info = self.user_model.\
                get_user_info(unchecked_guarantee[i]['guarantor_id'])
            unchecked_guarantee[i]['guarantor_name'] = \
                guarantor_info['real_name']
            warrantee_info = self.user_model.\
                get_user_info(unchecked_guarantee[i]['warrantee_id'])
            unchecked_guarantee[i]['warrantee_name'] = \
                warrantee_info['real_name']
        self.render("nimda/guarantee.html", guarantee=guarantee,
                    unchecked_guarantee=unchecked_guarantee)


class AdminGuaranteeCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, guarantee_id):
        self.guarantee_model.change_status(guarantee_id)
        self.redirect("nimda/guarantee")


class AdminLoanCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, loan_id):
        loan_id = int(loan_id)
        pass


class AdminPayHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("nimda/pay.html")


class AdminPayCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        loan_id = int(self.get_argument("loan_id", None))
        pass

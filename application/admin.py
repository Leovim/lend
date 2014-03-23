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
        self.render("nimda/user.html")


class AdminLoanHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("nimda/loan.html")


class AdminGuaranteeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("nimda/guarantee.html")


class AdminLoanCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, loan_id):
        loan_id = int(loan_id)
        pass


class AdminPayHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass


class AdminPayCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        loan_id = int(self.get_argument("loan_id", None))
        pass


class AdminGuaranteeCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, guarantee_id):
        pass

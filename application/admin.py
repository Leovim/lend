#coding=utf8

import tornado.web
import tornado.httpclient
import tornado.gen
from models import *
from config import options

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# todo 添加修改状态功能后，增加loan model中相关检查


class BaseHandler(tornado.web.RequestHandler):
    user_model = UserModel()
    guarantee_model = GuaranteeModel()
    loan_model = LoanModel()
    behaviour_model = BehaviourModel()
    split_model = SplitLoanModel()
    pay_model = PayModel()

    def get_current_user(self):
        user_id = self.get_secure_cookie("user", max_age_days=365)
        if user_id == '1':
            return 1
        elif user_id == '2':
            return 2
        return False

    @tornado.gen.coroutine
    def send_sms(self, phone, content):
        http = tornado.httpclient.AsyncHTTPClient()
        url = "http://utf8.sms.webchinese.cn/?Uid=shuguozhu&Key=" \
              + options.sms_secret + "&smsMob=" + phone + "&"
        import urllib
        data = dict()
        data['smsText'] = content
        n_content = urllib.urlencode(data)
        url = url + n_content
        response = yield http.fetch(url)
        self.finish()
        if response.body == '1':
            yield 1
            return
        else:
            yield 0
            return


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("nimda/index.html")


class AdminLoginHandler(BaseHandler):
    def get(self):
        self.render("nimda/login.html")


class AdminLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect("/nimda/login")


class AdminAuthenticateHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        if username == options.admin and password == options.admin_password:
            self.set_secure_cookie("user", str(1), expires_days=365)
            self.redirect("/nimda/loan")
        elif username == options.read and password == options.read_password:
            self.set_secure_cookie("user", str(2), expires_days=365)
            self.redirect("/nimda/loan")
        else:
            self.render("index.html", result_json="用户名或密码错误")


class AdminAllUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        users = self.user_model.get_all_users()
        self.render("nimda/all_user.html", users=users)


class AdminUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, user_id):
        user_id = int(user_id)
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
        unchecked_loans = self.loan_model.get_all_unchecked_loans()
        loans = self.loan_model.get_all_ing_loans()
        complete_loans = self.loan_model.get_all_complete_loans()
        for i, item in enumerate(unchecked_loans):
            user_info = self.user_model.get_user_info(item['user_id'])
            unchecked_loans[i]['real_name'] = user_info['real_name']
            unchecked_loans[i]['guarantor1_name'] = None
            unchecked_loans[i]['guarantor2_name'] = None
            if item['guarantor1']:
                guarantor1 = self.user_model.get_user_info(item['guarantor1'])
                unchecked_loans[i]['guarantor1_name'] = guarantor1['real_name']
            if item['guarantor2']:
                guarantor2 = self.user_model.get_user_info(item['guarantor2'])
                unchecked_loans[i]['guarantor2_name'] = guarantor2['real_name']
        for i, item in enumerate(loans):
            user_info = self.user_model.get_user_info(item['user_id'])
            loans[i]['real_name'] = user_info['real_name']
            loans[i]['guarantor1_name'] = None
            loans[i]['guarantor2_name'] = None
            if item['guarantor1']:
                guarantor1 = self.user_model.get_user_info(item['guarantor1'])
                loans[i]['guarantor1_name'] = guarantor1['real_name']
            if item['guarantor2']:
                guarantor2 = self.user_model.get_user_info(item['guarantor2'])
                loans[i]['guarantor2_name'] = guarantor2['real_name']
            if item['split_status'] == 1:
                split_info = self.split_model.get_split_info(item['loan_id'])
                loans[i]['split_status'] = split_info
        for i, item in enumerate(complete_loans):
            user_info = self.user_model.get_user_info(item['user_id'])
            complete_loans[i]['real_name'] = user_info['real_name']
            complete_loans[i]['guarantor1_name'] = None
            complete_loans[i]['guarantor2_name'] = None
            if item['guarantor1']:
                guarantor1 = self.user_model.get_user_info(item['guarantor1'])
                complete_loans[i]['guarantor1_name'] = guarantor1['real_name']
            if item['guarantor2']:
                guarantor2 = self.user_model.get_user_info(item['guarantor2'])
                complete_loans[i]['guarantor2_name'] = guarantor2['real_name']
        self.render("nimda/loan.html", unchecked_loans=unchecked_loans,
                    loans=loans, complete_loans=complete_loans)


class AdminLoanCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, loan_id):
        user = self.get_current_user()
        if user == 1:
            loan_id = int(loan_id)
            behaviour = self.behaviour_model.get_loan_loan_behaviour(loan_id)
            self.behaviour_model.change_status(behaviour['behaviour_id'], 1)
            self.loan_model.change_check_status(loan_id, 1)
            self.redirect("/nimda/loan")
        elif user == 2:
            self.render("index.html", result_json="没有权限进行修改")
        else:
            self.redirect("/nimda/login")


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
        user = self.get_current_user()
        if user == 1:
            guarantee_id = int(guarantee_id)
            self.guarantee_model.change_status(guarantee_id)
            self.redirect("/nimda/guarantee")
        elif user == 2:
            self.render("index.html", result_json="没有权限进行修改")
        else:
            self.redirect("/nimda/login")


class AdminPayHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        unchecked_pay = self.pay_model.get_all_unchecked_pay()
        complete_pay = self.pay_model.get_all_complete_pay()

        for i, item in enumerate(unchecked_pay):
            loan_info = self.loan_model.get_loan_info(item['loan_id'])
            unchecked_pay[i]['loan_info'] = loan_info
            user_info = self.user_model.get_user_info(loan_info['user_id'])
            unchecked_pay[i]['loan_info']['real_name'] = user_info['real_name']
            unchecked_pay[i]['loan_info']['guarantor1_name'] = None
            unchecked_pay[i]['loan_info']['guarantor2_name'] = None
            if unchecked_pay[i]['loan_info']['guarantor1']:
                guarantor1 = self.user_model.\
                    get_user_info(unchecked_pay[i]['loan_info']['guarantor1'])
                unchecked_pay[i]['loan_info']['guarantor1_name'] = \
                    guarantor1['real_name']
            if unchecked_pay[i]['loan_info']['guarantor2']:
                guarantor2 = self.user_model.\
                    get_user_info(unchecked_pay[i]['loan_info']['guarantor2'])
                unchecked_pay[i]['loan_info']['guarantor2_name'] = \
                    guarantor2['real_name']
            if unchecked_pay[i]['loan_info']['split_status'] == 1:
                split_info = self.split_model.get_split_info(item['loan_id'])
                unchecked_pay[i]['loan_info']['split_status'] = split_info

        for i, item in enumerate(complete_pay):
            loan_info = self.loan_model.get_loan_info(item['loan_id'])
            complete_pay[i]['loan_info'] = loan_info
            complete_pay[i]['loan_info']['guarantor1_name'] = None
            complete_pay[i]['loan_info']['guarantor2_name'] = None
            if complete_pay[i]['loan_info']['guarantor1']:
                guarantor1 = self.user_model.\
                    get_user_info(complete_pay[i]['loan_info']['guarantor1'])
                complete_pay[i]['loan_info']['guarantor1_name'] = \
                    guarantor1['real_name']
            if complete_pay[i]['loan_info']['guarantor2']:
                guarantor2 = self.user_model.\
                    get_user_info(complete_pay[i]['loan_info']['guarantor2'])
                complete_pay[i]['loan_info']['guarantor2_name'] = \
                    guarantor2['real_name']
        self.render("nimda/pay.html", unchecked_pay=unchecked_pay,
                    complete_pay=complete_pay)


class AdminPayCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, pay_id):
        user = self.get_current_user()
        if user == 1:
            pay_id = int(pay_id)
            pay_info = self.pay_model.get_pay_info(pay_id)
            bhv_info = self.behaviour_model.\
                get_loan_pay_behaviour(pay_info['loan_id'])
            self.behaviour_model.change_status(bhv_info['behaviour_id'], 1)
            self.pay_model.update_check_status(pay_id)
            loan_info = self.loan_model.get_loan_info(pay_info['loan_id'])
            if loan_info['remain_amount'] == 0:
                # 已完成
                self.loan_model.change_check_status(loan_info['loan_id'], 2)
            self.redirect("/nimda/pay")
        elif user == 2:
            self.render("index.html", result_json="没有权限进行修改")
        else:
            self.redirect("/nimda/login")


class AdminPushHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, user_id):
        user_info = self.user_model.get_user_info(user_id)
        phone = user_info['phone']
        content = "你的贷款即将到期了，请尽快归还。"
        self.send_sms(phone, content)
        self.redirect('/nimda/loan')

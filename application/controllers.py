#coding=utf8

import json
import hashlib
# import datetime
import tornado.web
from models import *


class BaseHandler(tornado.web.RequestHandler):
    user_model = UserModel()
    guarantee_model = GuaranteeModel()
    loan_model = LoanModel()
    behaviour_model = BehaviourModel()

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        return self.user_model.get_user_info(int(user_id))
    
    @staticmethod
    def interest_round(interest):
        return round(interest * 100) / 100

    def calc_one_interest(self, principal):
        if principal <= 200:
            return 0
        elif principal <= 300:
            return 0
        elif principal <= 400:
            return 0
        elif principal <= 500:
            return 0
        elif principal <= 600:
            return self.interest_round((principal - 500) * 0.02 / 52)
        elif principal <= 700:
            return self.interest_round(0.04 + (principal - 600) * 0.04 / 52)
        elif principal <= 800:
            return self.interest_round(0.12 + (principal - 700) * 0.06 / 52)
        elif principal <= 900:
            return self.interest_round(0.24 + (principal - 800) * 0.08 / 52)
        elif principal <= 1000:
            return self.interest_round(0.40 + (principal - 900) * 0.10 / 52)
        elif principal <= 1100:
            return self.interest_round(0.60 + (principal - 1000) * 0.12 / 52)
        elif principal <= 1200:
            return self.interest_round(0.83 + (principal - 1100) * 0.14 / 52)

    def calc_two_interest(self, principal):
        if principal <= 200:
            return 0
        elif principal <= 300:
            return self.interest_round((principal - 200) * 0.1 / 26)
        elif principal <= 400:
            return self.interest_round(0.38 + (principal - 300) * 0.11 / 26)
        elif principal <= 500:
            return self.interest_round(0.80 + (principal - 400) * 0.12 / 26)
        elif principal <= 600:
            return self.interest_round(1.26 + (principal - 500) * 0.13 / 26)
        elif principal <= 700:
            return self.interest_round(1.76 + (principal - 600) * 0.14 / 26)
        elif principal <= 800:
            return self.interest_round(2.30 + (principal - 700) * 0.15 / 26)
        elif principal <= 900:
            return self.interest_round(2.88 + (principal - 800) * 0.16 / 26)
        elif principal <= 1000:
            return self.interest_round(3.50 + (principal - 900) * 0.17 / 26)
        elif principal <= 1100:
            return self.interest_round(4.15 + (principal - 1000) * 0.18 / 26)
        elif principal <= 1200:
            return self.interest_round(4.84 + (principal - 1100) * 0.19 / 26)

    def calc_four_interest(self, principal):
        if principal <= 200:
            return 0
        elif principal <= 300:
            return self.interest_round((principal - 200) * 0.175 / 13)
        elif principal <= 400:
            return self.interest_round(1.35 + (principal - 300) * 0.180 / 13)
        elif principal <= 500:
            return self.interest_round(2.74 + (principal - 400) * 0.185 / 13)
        elif principal <= 600:
            return self.interest_round(4.16 + (principal - 500) * 0.190 / 13)
        elif principal <= 700:
            return self.interest_round(5.62 + (principal - 600) * 0.195 / 13)
        elif principal <= 800:
            return self.interest_round(7.12 + (principal - 700) * 0.200 / 13)
        elif principal <= 900:
            return self.interest_round(8.66 + (principal - 800) * 0.205 / 13)
        elif principal <= 1000:
            return self.interest_round(10.24 + (principal - 900) * 0.210 / 13)
        elif principal <= 1100:
            return self.interest_round(11.86 + (principal - 1000) * 0.215 / 13)
        elif principal <= 1200:
            return self.interest_round(13.51 + (principal - 1100) * 0.220 / 13)

    def calc_interest(self, principal, time):
        # time: week number
        # rate: 22.2% = 0.222
        if time == 1:
            return self.calc_one_interest(principal)
        elif time == 2:
            return self.calc_two_interest(principal)
        elif time == 4:
            return self.calc_four_interest(principal)


class IndexHandler(BaseHandler):
    def get(self, arg):
        result_json = json.dumps([arg, {'name': "Leo中文", 'age': 20},
                                  {'name': "Smith", 'age': 17}],
                                 separators=(',', ':'), encoding="utf-8",
                                 indent=4, ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class LoanHandler(BaseHandler):
    def get(self):
        # user_id = 1
        user = self.get_current_user()
        if not user:
            #raise tornado.web.HTTPError(404)
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        else:
            result = self.loan_model.get_user_new_three_loans(user['user_id'])
            i = 0
            while i < result.__len__():
                if result[i]['guarantor1']:
                    result[i]['guarantor1'] = self.user_model.\
                        get_user_real_name(result[i]['guarantor1'])
                if result[i]['guarantor2']:
                    result[i]['guarantor2'] = self.user_model. \
                        get_user_real_name(result[i]['guarantor2'])
                i += 1
            result_json = json.dumps({'result': 1, 'loan': result},
                                     separators=(',', ':'), encoding="utf-8",
                                     indent=4, ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)


class HistoryHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            # raise tornado.web.HTTPError(404)
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        else:
            result = self.behaviour_model.\
                get_user_new_ten_behaviours(user['user_id'])
            result_json = json.dumps({'result': 1, 'history': result},
                                     separators=(',', ':'), encoding="utf-8",
                                     indent=4, ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)


class LoginHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)

        user_id = self.user_model.check_username_exist(username)
        if user_id:
            user_info = self.user_model.get_user_info(user_id)
            # password hash
            sha = hashlib.sha1()
            sha.update(password)
            sha_password = sha.hexdigest()
            if user_info['password'] == sha_password:
                histories = self.behaviour_model.\
                    get_user_new_ten_behaviours(user_id)
                loans = self.loan_model.get_user_new_three_loans(user_id)
                # success
                self.set_secure_cookie("user", str(user_id))
                del user_info['password']
                result_json = json.dumps({'result': 1,
                                          'user': user_info,
                                          'loans': loans,
                                          'histories': histories},
                                         separators=(',', ':'), indent=4,
                                         encoding="utf-8", ensure_ascii=False)
                self.render("index.html", title="Lend", result_json=result_json)
            else:
                # wrong password
                result_json = json.dumps({'result': 2}, separators=(',', ':'),
                                         indent=4, encoding="utf-8",
                                         ensure_ascii=False)
                self.render("index.html", title="Lend", result_json=result_json)
        else:
            # username not exist
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     indent=4, encoding="utf-8",
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')


class RegisterHandler(BaseHandler):
    def post(self):
        phone = self.get_argument('phone', None)
        username = self.get_argument('username', None),
        password = self.get_argument('password', None)

        # password hash
        sha = hashlib.sha1()
        sha.update(password)
        sha_password = sha.hexdigest()

        # return 1: success
        # return 2: username exist
        # return 3: phone exist
        # return 4: unknown error

        # check if username exist
        if self.user_model.check_username_exist(username):
            result_json = json.dumps({'result': 2}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        # check if phone exist
        elif self.user_model.check_phone_exist(phone):
            result_json = json.dumps({'result': 3}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        else:
            user = dict(
                username=username,
                password=sha_password,
                phone=phone
            )
            self.user_model.add_user(user)
            result_json = json.dumps({'result': 1}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)


class LoanRequestHandler(BaseHandler):
    def post(self):
        user = self.current_user()
        if not user:
            # not logged in
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        else:
            loan_amount = self.get_argument("loan_amount", None)
            loan_date = self.get_argument("loan_date", None)

            # 检验额度，估计贷款各段利息，计算利息，根据已担保人数进行利息减免，计算手续费，计算到期日期，获取被担保人ID，写入数据库
            if self.loan_model.check_total_loan_money(user['user_id'],
                                                      int(loan_amount)):
                result_json = json.dumps({'result': 2}, separators=(',', ':'),
                                         encoding="utf-8", indent=4,
                                         ensure_ascii=False)
                self.render("index.html", title="Lend", result_json=result_json)
            else:
                pass


class DueRequestHandler(BaseHandler):
    def post(self):
        user = self.get_current_user()
        if user:
            loan_id = self.get_argument("loan_id", None)
            due_time = self.get_argument("due_time", None)


class SplitRequestHandler(BaseHandler):
    def post(self):
        loan_id = self.get_argument("loan_id", None)
        pass


class GuaranteeHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            # raise tornado.web.HTTPError(404)
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        else:
            guarantor = self.guarantee_model.get_user_guarantor(user['user_id'])
            warrantee = self.guarantee_model.get_user_warrantee(user['user_id'])
            result_json = json.dumps({'result': 1, 'guarantor': guarantor,
                                      'warrantee': warrantee},
                                     separators=(',', ':'), encoding="utf-8",
                                     indent=4, ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)

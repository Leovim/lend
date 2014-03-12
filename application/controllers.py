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
    
    def calc_interest(self, principal, rate, time):
        # time: week number
        # rate: 22.2% = 0.222
        return principal * rate * time / 52


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
            result = self.behaviour_model.get_user_new_ten_behaviours(user['user_id'])
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
                histories = self.behaviour_model.get_user_new_ten_behaviours(user_id)
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
        if user:
            guarantor = self.guarantee_model.get_user_guarantor(user['user_id'])
            warrantee = self.guarantee_model.get_user_warrantee(user['user_id'])
            result_json = json.dumps({'result': 1, 'guarantor': guarantor,
                                      'warrantee': warrantee},
                                     separators=(',', ':'), encoding="utf-8",
                                     indent=4, ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)

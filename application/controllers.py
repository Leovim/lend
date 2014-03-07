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
        user_id = self.get_secure_cookie("user_id")
        if not user_id:
            return None
        return self.user_model.get_user_info(user_id)


class IndexHandler(BaseHandler):
    def get(self, arg):
        result_json = json.dumps([arg, {'name': "Leo中文", 'age': 20},
                                  {'name': "Smith", 'age': 17}],
                                 separators=(',', ':'), encoding="utf-8",
                                 indent=4, ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class LoanHandler(BaseHandler):
    def get(self, user_id=None):
        # user_id = 1
        user_id = user_id.__str__()
        if not user_id:
            raise tornado.web.HTTPError(404)
        else:
            result = self.loan_model.get_user_new_three_loans(user_id)
            result_json = json.dumps(result, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)


class HistoryHandler(BaseHandler):
    def get(self, user_id=None):
        user_id = user_id.__str__()
        if not user_id:
            raise tornado.web.HTTPError(404)
        else:
            result = self.behaviour_model.get_user_new_ten_behaviours(user_id)
            result_json = json.dumps(result, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)


class LoginHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        # username = "sdlu"
        # password = "123456"
        result_json = json.dumps([], separators=(',', ':'), indent=4,
                                   encoding="utf-8", ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class LogoutHandler(BaseHandler):
    def get(self):
        pass


class RegisterHandler(BaseHandler):
    def post(self):
        password = self.get_argument('password', None)
        sha = hashlib.sha1()
        sha.update(password)
        sha_password = sha.hexdigest()

        # check if username exist
        # check if phone exist

        user = dict(
            username=self.get_argument('username', None),
            password=sha_password,
            phone=self.get_argument('phone', None)
        )
        self.user_model.add_user(user)
        

class LoanRequestHandler(BaseHandler):
    def post(self):
        pass


class DueRequestHandler(BaseHandler):
    def get(self):
        pass


class SplitRequestHandler(BaseHandler):
    def get(self):
        pass

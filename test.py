#coding=utf8

import os
import json
import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8002, help="run on the given port.", type=int)
define("user_id", default=1, help="test user ID.", type=int)
define("username", default="sdlu", help="test username")
define("password", default="123456", help="test user's password")
define("phone", default="13333333333", help="test users' phone number")
define("real_name", default="路少德", help="test user's real name")
define("bank_number", default="", help="test user's bank number")
define("alipay_number", default="", help="test user's alipay number")
define("credit", default=3, help="test user's credit")
define("avatar", default="/static/favicon.ico", help="test user's avatar")


class Applicaiton(tornado.web.Application):
    def __init__(self):
        # route
        handlers = [
            (r"/loan/([0-9]+)", LoanHandler),
            (r"/history/([0-9]+)", HistoryHandler),
            (r"/login", LoginHandler),
            (r"/", IndexHandler),
        ]
        # settings
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        result_json = json.dumps([arg, {'name': "Leo中文", 'age': 20}, {'name': "Smith", 'age': 17}], separators=(',', ':'), encoding="utf-8", indent=4, ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class LoanHandler(tornado.web.RequestHandler):
    def get(self, user_id=None):
        # user_id = 1
        user_id = user_id.__str__()
        if user_id == '1':
            loan = [
                dict(
                    loan_id=10,
                    user_id=1,
                    loan_amount=300,
                    remain_amount=300,
                    loan_date=datetime.date.today().__str__(),
                    due_date=(datetime.date.today() + datetime.timedelta(days=30)).__str__(),
                    split_status=0,
                    due_status=0
                ),
                dict(
                    loan_id=6,
                    user_id=1,
                    loan_amount=600,
                    remain_amount=600,
                    loan_date=datetime.date.today().__str__(),
                    due_date=(datetime.date.today() + datetime.timedelta(days=30)).__str__(),
                    split_status=1,
                    due_status=2
                ),
                dict(
                    loan_id=3,
                    user_id=1,
                    loan_amount=300,
                    remain_amount=300,
                    loan_date=datetime.date.today().__str__(),
                    due_date=(datetime.date.today() + datetime.timedelta(days=30)).__str__(),
                    split_status=0,
                    due_status=1
                )
            ]
            result_json = json.dumps(loan, separators=(',', ':'), indent=4, encoding="utf-8", ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        elif not user_id:
            raise tornado.web.HTTPError(404)
        else:
            raise tornado.web.HTTPError(404)


class HistoryHandler(tornado.web.RequestHandler):
    def get(self, user_id=None):
        user_id = user_id.__str__()
        if user_id == '1':
            history = [
                dict(
                    behaviour_id=10,
                    user_id=1,
                    type=2,
                    money=300
                ),
                dict(
                    behaviour_id=9,
                    user_id=1,
                    type=3,
                    money=300
                ),
                dict(
                    behaviour_id=8,
                    user_id=1,
                    type=1,
                    money=300
                ),
                dict(
                    behaviour_id=7,
                    user_id=1,
                    type=4,
                    money=300
                ),
                dict(
                    behaviour_id=6,
                    user_id=1,
                    type=2,
                    money=300
                ),
                dict(
                    behaviour_id=5,
                    user_id=1,
                    type=4,
                    money=300
                ),
                dict(
                    behaviour_id=4,
                    user_id=1,
                    type=3,
                    money=300
                ),
                dict(
                    behaviour_id=3,
                    user_id=1,
                    type=1,
                    money=300
                ),
                dict(
                    behaviour_id=2,
                    user_id=1,
                    type=1,
                    money=300
                ),
                dict(
                    behaviour_id=1,
                    user_id=1,
                    type=1,
                    money=300
                )
            ]
            result_json = json.dumps(history, separators=(',', ':'), indent=4, ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        elif not user_id:
            raise tornado.web.HTTPError(404)
        else:
            raise tornado.web.HTTPError(404)


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        # username = "sdlu"
        # password = "123456"
        if username == options.username and password == options.password:
            user_info = dict(
                user_id=options.user_id,
                phone=options.phone,
                real_name=options.real_name,
                bank_number=options.bank_number,
                alipay_number=options.alipay_number,
                credit=options.credit,
                avatar=options.avatar,
                loan=[
                    dict(
                        loan_id=10,
                        user_id=1,
                        loan_amount=300,
                        remain_amount=300,
                        loan_date=datetime.date.today().__str__(),
                        due_date=(datetime.date.today() + datetime.timedelta(days=30)).__str__(),
                        split_status=0,
                        due_status=0
                    ),
                    dict(
                        loan_id=6,
                        user_id=1,
                        loan_amount=600,
                        remain_amount=600,
                        loan_date=datetime.date.today().__str__(),
                        due_date=(datetime.date.today() + datetime.timedelta(days=30)).__str__(),
                        split_status=1,
                        due_status=2
                    ),
                    dict(
                        loan_id=3,
                        user_id=1,
                        loan_amount=300,
                        remain_amount=300,
                        loan_date=datetime.date.today().__str__(),
                        due_date=(datetime.date.today() + datetime.timedelta(days=30)).__str__(),
                        split_status=0,
                        due_status=1
                    )
                ],
                history=[
                    dict(
                        behaviour_id=10,
                        user_id=1,
                        type=2,
                        money=300
                    ),
                    dict(
                        behaviour_id=9,
                        user_id=1,
                        type=3,
                        money=300
                    ),
                    dict(
                        behaviour_id=8,
                        user_id=1,
                        type=1,
                        money=300
                    ),
                    dict(
                        behaviour_id=7,
                        user_id=1,
                        type=4,
                        money=300
                    ),
                    dict(
                        behaviour_id=6,
                        user_id=1,
                        type=2,
                        money=300
                    ),
                    dict(
                        behaviour_id=5,
                        user_id=1,
                        type=4,
                        money=300
                    ),
                    dict(
                        behaviour_id=4,
                        user_id=1,
                        type=3,
                        money=300
                    ),
                    dict(
                        behaviour_id=3,
                        user_id=1,
                        type=1,
                        money=300
                    ),
                    dict(
                        behaviour_id=2,
                        user_id=1,
                        type=1,
                        money=300
                    ),
                    dict(
                        behaviour_id=1,
                        user_id=1,
                        type=1,
                        money=300
                    )
                ]
            )
            result_json = json.dumps(user_info, separators=(',', ':'), indent=4, encoding="utf-8", ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        else:
            self.render("index.html", title="Lend", result_json="error")

def main():
    http_server = tornado.httpserver.HTTPServer(Applicaiton())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

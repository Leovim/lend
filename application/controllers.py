#coding=utf8

import json
# import datetime
import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def get(self, arg):
        result_json = json.dumps([arg, {'name': "Leo中文", 'age': 20},
                                  {'name': "Smith", 'age': 17}],
                                 separators=(',', ':'), encoding="utf-8",
                                 indent=4, ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class LoanHandler(tornado.web.RequestHandler):
    def get(self, user_id=None):
        # user_id = 1
        user_id = user_id.__str__()
        if not user_id:
            raise tornado.web.HTTPError(404)


class HistoryHandler(tornado.web.RequestHandler):
    def get(self, user_id=None):
        user_id = user_id.__str__()
        if not user_id:
            raise tornado.web.HTTPError(404)
        else:
            raise tornado.web.HTTPError(404)


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        # username = "sdlu"
        # password = "123456"
        result_json = json.dumps([], separators=(',', ':'), indent=4,
                                   encoding="utf-8", ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


#coding=utf8

from controllers import IndexHandler, LoanHandler, HistoryHandler, LoginHandler

handlers = [
    (r"/loan/([0-9]+)", LoanHandler),
    (r"/history/([0-9]+)", HistoryHandler),
    (r"/login", LoginHandler),
    (r"/", IndexHandler),
]

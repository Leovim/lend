#coding=utf8

from controllers import \
    IndexHandler, \
    LoanHandler, \
    HistoryHandler, \
    LoginHandler, \
    LogoutHandler, \
    RegisterHandler, \
    LoanRequestHandler, \
    DueRequestHandler, \
    SplitRequestHandler

handlers = [
    (r"/loan/([0-9]+)", LoanHandler),
    (r"/history/([0-9]+)", HistoryHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/register", RegisterHandler),
    (r"/loan_request", LoanRequestHandler),
    (r"/due_request", DueRequestHandler),
    (r"/split_request", SplitRequestHandler),
    (r"/", IndexHandler),
]

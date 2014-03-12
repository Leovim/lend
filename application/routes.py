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
    SplitRequestHandler, \
    GuaranteeHandler

handlers = [
    (r"/loan", LoanHandler),
    (r"/history", HistoryHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/register", RegisterHandler),
    (r"/loan_request", LoanRequestHandler),
    (r"/due_request", DueRequestHandler),
    (r"/split_request", SplitRequestHandler),
    (r"/guarantee", GuaranteeHandler),
    (r"/", IndexHandler),
]

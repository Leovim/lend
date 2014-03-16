#coding=utf8

from controllers import \
    IndexHandler, \
    UserHandler, \
    LoanHandler, \
    HistoryHandler, \
    GuaranteeHandler, \
    LoginHandler, \
    LogoutHandler, \
    RegisterHandler, \
    LoanRequestHandler, \
    DueRequestHandler, \
    SplitRequestHandler, \
    SendSmsHandler

handlers = [
    (r"/user", UserHandler),
    (r"/loan", LoanHandler),
    (r"/history", HistoryHandler),
    (r"/guarantee", GuaranteeHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/register", RegisterHandler),
    (r"/loan_request", LoanRequestHandler),
    (r"/due_request", DueRequestHandler),
    (r"/split_request", SplitRequestHandler),
    (r"/send_sms", SendSmsHandler),
    (r"/", IndexHandler),
]

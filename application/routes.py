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
    UpdateHandler, \
    LoanRequestHandler, \
    DueRequestHandler, \
    SplitRequestHandler, \
    GuaranteeRequestHandler, \
    SendSmsHandler

handlers = [
    (r"/user", UserHandler),
    (r"/loan", LoanHandler),
    (r"/history", HistoryHandler),
    (r"/guarantee", GuaranteeHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/register", RegisterHandler),
    (r"/update", UpdateHandler),
    (r"/loan_request", LoanRequestHandler),
    (r"/due_request", DueRequestHandler),
    (r"/split_request", SplitRequestHandler),
    (r"/guarantee_request", GuaranteeRequestHandler),
    (r"/send_sms", SendSmsHandler),
    (r"/", IndexHandler),
]

#coding=utf8
import tornado.web
from config import settings

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
    PayRequestHandler, \
    GuaranteeRequestHandler, \
    GuaranteeDeleteHandler, \
    SendSmsHandler, \
    UploadHandler

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
    (r"/pay_request", PayRequestHandler),
    (r"/guarantee_request", GuaranteeRequestHandler),
    (r"/guarantee_delete", GuaranteeDeleteHandler),
    (r"/send_sms", SendSmsHandler),
    (r"/upload", UploadHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler,
     dict(path=settings['static_path'])),
    (r"/", IndexHandler),
]

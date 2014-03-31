#coding=utf8
import tornado.web
from config import settings

from controllers import \
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
    PasswordHandler, \
    SendSmsHandler, \
    UploadHandler, \
    InterestHandler

from admin import \
    IndexHandler, \
    AdminLoginHandler, \
    AdminLogoutHandler, \
    AdminAuthenticateHandler, \
    AdminUserHandler, \
    AdminGuaranteeHandler, \
    AdminGuaranteeUncheckedHandler, \
    AdminGuaranteeCheckHandler, \
    AdminLoanHandler, \
    AdminLoanUncheckedHandler, \
    AdminLoanCompleteHandler, \
    AdminLoanCheckHandler, \
    AdminPayHandler, \
    AdminPayCheckHandler, \
    AdminPushHandler, \
    AdminResetPhoneHandler, \
    AdminResetBankNumberHandler, \
    AdminAllUserHandler

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
    (r"/password", PasswordHandler),
    (r"/send_sms", SendSmsHandler),
    (r"/upload", UploadHandler),
    (r"/interest", InterestHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler,
     dict(path=settings['static_path'])),
    (r"/nimda/login", AdminLoginHandler),
    (r"/nimda/logout", AdminLogoutHandler),
    (r"/nimda/authenticate", AdminAuthenticateHandler),
    (r"/nimda/user/([0-9]*)", AdminUserHandler),
    (r"/nimda/guarantee", AdminGuaranteeHandler),
    (r"/nimda/guarantee_unchecked", AdminGuaranteeUncheckedHandler),
    (r"/nimda/guarantee_check/([0-9]*)", AdminGuaranteeCheckHandler),
    (r"/nimda/loan", AdminLoanHandler),
    (r"/nimda/loan_unchecked", AdminLoanUncheckedHandler),
    (r"/nimda/loan_complete", AdminLoanCompleteHandler),
    (r"/nimda/loan_check/([0-9]*)", AdminLoanCheckHandler),
    (r"/nimda/pay", AdminPayHandler),
    (r"/nimda/pay_check/([0-9]*)", AdminPayCheckHandler),
    (r"/nimda/reset_phone", AdminResetPhoneHandler),
    (r"/nimda/reset_bank_number", AdminResetBankNumberHandler),
    (r"/nimda/push/([0-9]*)", AdminPushHandler),
    (r"/nimda/all_user/([0-9]*)", AdminAllUserHandler),
    (r"/nimda/index", IndexHandler),
    (r"/nimda", IndexHandler),
]

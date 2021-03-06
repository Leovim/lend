#coding=utf8

import tornado.web
import tornado.httpclient
import tornado.gen
from models import *
from config import options

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class BaseHandler(tornado.web.RequestHandler):
    item_per_page = 50
    user_model = UserModel()
    guarantee_model = GuaranteeModel()
    loan_model = LoanModel()
    behaviour_model = BehaviourModel()
    split_model = SplitLoanModel()
    pay_model = PayModel()

    def get_current_user(self):
        user_id = self.get_secure_cookie("user", max_age_days=365)
        if user_id == '1':
            return 1
        elif user_id == '2':
            return 2
        return False

    @tornado.gen.coroutine
    def send_sms(self, phone, content):
        http = tornado.httpclient.AsyncHTTPClient()
        url = "http://utf8.sms.webchinese.cn/?Uid=shuguozhu&Key=" \
              + options.sms_secret + "&smsMob=" + phone + "&"
        import urllib
        data = dict()
        data['smsText'] = content
        n_content = urllib.urlencode(data)
        url = url + n_content
        response = yield http.fetch(url)
        print response.body
        self.finish()
        if response.body == '1':
            yield 1
            return
        else:
            yield 0
            return


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("nimda/index.html")


class AdminLoginHandler(BaseHandler):
    def get(self):
        self.render("nimda/login.html")


class AdminLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect("/nimda/login")


class AdminAuthenticateHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        if username == options.admin and password == options.admin_password:
            self.set_secure_cookie("user", str(1), expires_days=365)
            self.redirect("/nimda/index")
        elif username == options.read and password == options.read_password:
            self.set_secure_cookie("user", str(2), expires_days=365)
            self.redirect("/nimda/index")
        else:
            self.render("index.html", result_json="用户名或密码错误")


class AdminAllUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page):
        try:
            page = int(page)
        except ValueError:
            self.send_error(404)

        start = self.item_per_page * (page - 1)
        end = self.item_per_page * page
        users = self.user_model.get_slice_users(start, end)
        if users == []:
            self.send_error(404)

        user_number = self.user_model.get_users_number()
        if user_number % self.item_per_page > 0:
            page_number = user_number / self.item_per_page + 1
        else:
            page_number = user_number / self.item_per_page

        next_users = self.user_model.get_slice_users(end, end + 1)
        if next_users == []:
            next_page = 0
        else:
            next_page = page + 1
        if page == 1:
            previous_page = 0
        else:
            previous_page = page - 1
        self.render("nimda/all_user.html", users=users, page=page,
                    previous_page=previous_page, next_page=next_page,
                    page_number=page_number)


class AdminUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, user_id):
        if user_id == "":
            self.render("index.html", result_json="用户不存在")
            return
        user_id = int(user_id)
        user_info = self.user_model.get_user_info(user_id)
        loans = self.loan_model.get_user_all_loans(user_id)
        for i, item in enumerate(loans):
            if item['check_status'] == 0:
                loans[i]['check_status'] = "待审核"
            elif item['check_status'] == 1:
                loans[i]['check_status'] = "正常"
            elif item['check_status'] == 2:
                loans[i]['check_status'] = "已完成"

            loans[i]['guarantor1_name'] = None
            loans[i]['guarantor2_name'] = None
            if item['guarantor1']:
                guarantor1 = self.user_model.get_user_info(item['guarantor1'])
                loans[i]['guarantor1_name'] = guarantor1['real_name']
            if item['guarantor2']:
                guarantor2 = self.user_model.get_user_info(item['guarantor2'])
                loans[i]['guarantor2_name'] = guarantor2['real_name']
        self.render("nimda/user.html", user_info=user_info, loans=loans)


class AdminUserUncheckedHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        users = self.user_model.get_all_unchecked_users()
        self.render("nimda/user_unchecked.html", users=users)


class AdminUserCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, user_id):
        user = self.get_current_user()
        if user == 1:
            user_id = int(user_id)
            self.user_model.update_user_status(user_id, 1)
            user_info = self.user_model.get_user_info(user_id)
            content = "您的审核已通过，现在可以开始借款了。"
            self.send_sms(user_info['phone'], content)
            self.redirect("/nimda/user_unchecked")
        elif user == 2:
            self.render("index.html", result_json="没有权限进行修改")
        else:
            self.redirect("/nimda/login")


class AdminLoanHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page):
        try:
            page = int(page)
        except ValueError:
            self.send_error(404)

        start = self.item_per_page * (page - 1)
        end = self.item_per_page * page
        loans = self.loan_model.get_slice_ing_loans(start, end)
        if loans == []:
            self.send_error(404)

        loan_number = self.loan_model.get_ing_loan_number()
        if loan_number % self.item_per_page > 0:
            page_number = loan_number / self.item_per_page + 1
        else:
            page_number = loan_number / self.item_per_page

        next_loan = self.loan_model.get_slice_ing_loans(end, end + 1)
        if next_loan == []:
            next_page = 0
        else:
            next_page = page + 1
        if page == 1:
            previous_page = 0
        else:
            previous_page = page - 1
        for i, item in enumerate(loans):
            user_info = self.user_model.get_user_info(item['user_id'])
            loans[i]['real_name'] = user_info['real_name']
            loans[i]['guarantor1_name'] = None
            loans[i]['guarantor2_name'] = None
            if item['guarantor1']:
                guarantor1 = self.user_model.get_user_info(item['guarantor1'])
                loans[i]['guarantor1_name'] = guarantor1['real_name']
            if item['guarantor2']:
                guarantor2 = self.user_model.get_user_info(item['guarantor2'])
                loans[i]['guarantor2_name'] = guarantor2['real_name']
            if item['split_status'] == 1:
                split_info = self.split_model.get_split_info(item['loan_id'])
                loans[i]['split_status'] = split_info
        self.render("nimda/loan.html", loans=loans, page=page,
                    previous_page=previous_page, next_page=next_page,
                    page_number=page_number)


class AdminLoanUncheckedHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        unchecked_loans = self.loan_model.get_all_unchecked_loans()
        for i, item in enumerate(unchecked_loans):
            user_info = self.user_model.get_user_info(item['user_id'])
            unchecked_loans[i]['real_name'] = user_info['real_name']
            unchecked_loans[i]['guarantor1_name'] = None
            unchecked_loans[i]['guarantor2_name'] = None
            if item['guarantor1']:
                guarantor1 = self.user_model.get_user_info(item['guarantor1'])
                unchecked_loans[i]['guarantor1_name'] = guarantor1['real_name']
            if item['guarantor2']:
                guarantor2 = self.user_model.get_user_info(item['guarantor2'])
                unchecked_loans[i]['guarantor2_name'] = guarantor2['real_name']
        self.render("nimda/loan_unchecked.html",
                    unchecked_loans=unchecked_loans)


class AdminLoanCompleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page):
        try:
            page = int(page)
        except ValueError:
            self.send_error(404)

        start = self.item_per_page * (page - 1)
        end = self.item_per_page * page
        complete_loans = self.loan_model.get_slice_complete_loans(start, end)
        if complete_loans == []:
            self.send_error(404)

        loan_number = self.loan_model.get_complete_loan_number()
        if loan_number % self.item_per_page > 0:
            page_number = loan_number / self.item_per_page + 1
        else:
            page_number = loan_number / self.item_per_page

        next_loan = self.loan_model.get_slice_complete_loans(end, end + 1)
        if next_loan == []:
            next_page = 0
        else:
            next_page = page + 1
        if page == 1:
            previous_page = 0
        else:
            previous_page = page - 1
        for i, item in enumerate(complete_loans):
            user_info = self.user_model.get_user_info(item['user_id'])
            complete_loans[i]['real_name'] = user_info['real_name']
            complete_loans[i]['guarantor1_name'] = None
            complete_loans[i]['guarantor2_name'] = None
            if item['guarantor1']:
                guarantor1 = self.user_model.get_user_info(item['guarantor1'])
                complete_loans[i]['guarantor1_name'] = guarantor1['real_name']
            if item['guarantor2']:
                guarantor2 = self.user_model.get_user_info(item['guarantor2'])
                complete_loans[i]['guarantor2_name'] = guarantor2['real_name']
        self.render("nimda/loan_complete.html", complete_loans=complete_loans,
                    page=page, previous_page=previous_page, next_page=next_page,
                    page_number=page_number)

class AdminLoanCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, loan_id):
        user = self.get_current_user()
        if user == 1:
            loan_id = int(loan_id)
            loan_info = self.loan_model.get_loan_info(loan_id)
            behaviour = self.behaviour_model.get_loan_loan_behaviour(loan_id)
            user_info = self.user_model.get_user_info(loan_info['user_id'])
            self.behaviour_model.change_status(behaviour['behaviour_id'], 1)
            self.loan_model.change_check_status(loan_id, 1)
            content = "您的借款已汇出，请注意查收。"
            self.send_sms(user_info['phone'],content)
            self.redirect("/nimda/loan_unchecked")
        elif user == 2:
            self.render("index.html", result_json="没有权限进行修改")
        else:
            self.redirect("/nimda/login")


class AdminGuaranteeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page):
        try:
            page = int(page)
        except ValueError:
            self.send_error(404)

        start = self.item_per_page * (page - 1)
        end = self.item_per_page * page
        guarantee = self.guarantee_model.get_slice_guarantee(start, end)
        if guarantee == []:
            self.send_error(404)

        guarantee_number = self.guarantee_model.get_guarantees_number()
        if guarantee_number % self.item_per_page > 0:
            page_number = guarantee_number / self.item_per_page + 1
        else:
            page_number = guarantee_number / self.item_per_page

        next_guarantee = self.guarantee_model.get_slice_guarantee(end, end + 1)
        if next_guarantee == []:
            next_page = 0
        else:
            next_page = page + 1
        if page == 1:
            previous_page = 0
        else:
            previous_page = page - 1
        for i, item in enumerate(guarantee):
            guarantor_info = self.user_model.\
                get_user_info(guarantee[i]['guarantor_id'])
            guarantee[i]['guarantor_name'] = guarantor_info['real_name']
            warrantee_info = self.user_model.\
                get_user_info(guarantee[i]['warrantee_id'])
            guarantee[i]['warrantee_name'] = warrantee_info['real_name']
        self.render("nimda/guarantee.html", guarantee=guarantee, page=page,
                    previous_page=previous_page, next_page=next_page,
                    page_number=page_number)


class AdminGuaranteeUncheckedHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        unchecked_guarantee = self.guarantee_model.get_all_unchecked_guarantee()
        for i, item in enumerate(unchecked_guarantee):
            guarantor_info = self.user_model. \
                get_user_info(unchecked_guarantee[i]['guarantor_id'])
            unchecked_guarantee[i]['guarantor_name'] = \
                guarantor_info['real_name']
            warrantee_info = self.user_model. \
                get_user_info(unchecked_guarantee[i]['warrantee_id'])
            unchecked_guarantee[i]['warrantee_name'] = \
                warrantee_info['real_name']
        self.render("nimda/guarantee_unchecked.html",
                    unchecked_guarantee=unchecked_guarantee)


class AdminGuaranteeCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, guarantee_id):
        user = self.get_current_user()
        if user == 1:
            guarantee_id = int(guarantee_id)
            self.guarantee_model.change_status(guarantee_id)
            guarantee_info = self.guarantee_model.get_guarantee_info(guarantee_id)
            if not guarantee_info:
                self.render("index.html", result_json="担保关系不存在")
                return
            guarantor_info = self.user_model.get_user_info(guarantee_info['guarantor_id'])
            warrantee_info = self.user_model.get_user_info(guarantee_info['warrantee_id'])
            content = "您和" + warrantee_info['real_name'] + "已经成功建立担保关系。"
            self.send_sms(guarantor_info['phone'], content)
            content = "您和" + guarantor_info['real_name'] + "已经成功建立担保关系。"
            self.send_sms(warrantee_info['phone'], content)
            self.redirect("/nimda/guarantee_unchecked")
        elif user == 2:
            self.render("index.html", result_json="没有权限进行修改")
        else:
            self.redirect("/nimda/login")


class AdminPayHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        unchecked_pay = self.pay_model.get_all_unchecked_pay()
        complete_pay = self.pay_model.get_all_complete_pay()

        for i, item in enumerate(unchecked_pay):
            loan_info = self.loan_model.get_loan_info(item['loan_id'])
            unchecked_pay[i]['loan_info'] = loan_info
            user_info = self.user_model.get_user_info(loan_info['user_id'])
            unchecked_pay[i]['loan_info']['real_name'] = user_info['real_name']
            unchecked_pay[i]['loan_info']['guarantor1_name'] = None
            unchecked_pay[i]['loan_info']['guarantor2_name'] = None
            if unchecked_pay[i]['loan_info']['guarantor1']:
                guarantor1 = self.user_model.\
                    get_user_info(unchecked_pay[i]['loan_info']['guarantor1'])
                unchecked_pay[i]['loan_info']['guarantor1_name'] = \
                    guarantor1['real_name']
            if unchecked_pay[i]['loan_info']['guarantor2']:
                guarantor2 = self.user_model.\
                    get_user_info(unchecked_pay[i]['loan_info']['guarantor2'])
                unchecked_pay[i]['loan_info']['guarantor2_name'] = \
                    guarantor2['real_name']
            if unchecked_pay[i]['loan_info']['split_status'] == 1:
                split_info = self.split_model.get_split_info(item['loan_id'])
                unchecked_pay[i]['loan_info']['split_status'] = split_info

        for i, item in enumerate(complete_pay):
            loan_info = self.loan_model.get_loan_info(item['loan_id'])
            complete_pay[i]['loan_info'] = loan_info
            complete_pay[i]['loan_info']['guarantor1_name'] = None
            complete_pay[i]['loan_info']['guarantor2_name'] = None
            if complete_pay[i]['loan_info']['guarantor1']:
                guarantor1 = self.user_model.\
                    get_user_info(complete_pay[i]['loan_info']['guarantor1'])
                complete_pay[i]['loan_info']['guarantor1_name'] = \
                    guarantor1['real_name']
            if complete_pay[i]['loan_info']['guarantor2']:
                guarantor2 = self.user_model.\
                    get_user_info(complete_pay[i]['loan_info']['guarantor2'])
                complete_pay[i]['loan_info']['guarantor2_name'] = \
                    guarantor2['real_name']
        self.render("nimda/pay.html", unchecked_pay=unchecked_pay,
                    complete_pay=complete_pay)


class AdminPayCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, pay_id):
        user = self.get_current_user()
        if user == 1:
            pay_id = int(pay_id)
            pay_info = self.pay_model.get_pay_info(pay_id)
            bhv_info = self.behaviour_model.\
                get_loan_pay_behaviour(pay_info['loan_id'])
            self.behaviour_model.change_status(bhv_info['behaviour_id'], 1)
            self.pay_model.update_check_status(pay_id)
            loan_info = self.loan_model.get_loan_info(pay_info['loan_id'])
            user_info = self.user_model.get_user_info(loan_info['user_id'])
            content = "您的还款已成功，谢谢您的使用。"
            self.send_sms(user_info['phone'], content)
            if loan_info['remain_amount'] == 0:
                # 已完成
                self.loan_model.change_check_status(loan_info['loan_id'], 2)
            self.redirect("/nimda/pay")
        elif user == 2:
            self.render("index.html", result_json="没有权限进行修改")
        else:
            self.redirect("/nimda/login")


class AdminPushHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, user_id):
        user = self.get_current_user()
        if user == 1:
            user_info = self.user_model.get_user_info(user_id)
            phone = user_info['phone']
            content = "您的借款即将到期，请尽快归还。"
            self.send_sms(phone, content)
            self.redirect('/nimda/loan/1')
        elif user == 2:
            self.render("index.html", result_json="没有权限进行修改")
        else:
            self.redirect("/nimda/login")


class AdminResetPhoneHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        if user == 1:
            user_id = int(self.get_argument("user_id", None))
            phone = self.get_argument("phone", None)
            if self.user_model.reset_phone(user_id, phone):
                self.redirect("/nimda/user/"+str(user_id))
            else:
                self.render("index.html", result_json="用户不存在")
        elif user == 2:
            self.render("index.html", result_json="没有权限进行修改")
        else:
            self.redirect("/nimda/login")


class AdminResetBankNumberHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        if user == 1:
            user_id = int(self.get_argument("user_id", None))
            bank_number = self.get_argument("bank_number", None)
            if self.user_model.reset_bank_number(user_id, bank_number):
                self.redirect("/nimda/user/"+str(user_id))
            else:
                self.render("index.html", result_json="用户不存在")
        elif user == 2:
            self.render("index.html", result_json="没有权限进行修改")
        else:
            self.redirect("/nimda/login")


class AdminResetDormHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        if user == 1:
            user_id = int(self.get_argument("user_id", None))
            dorm = self.get_argument("dorm", None)
            if self.user_model.reset_dorm(user_id, dorm):
                self.redirect("/nimda/user/"+str(user_id))
            else:
                self.render("index.html", result_json="用户不存在")
        elif user == 2:
            self.render("index.html", result_json="没有权限进行修改")
        else:
            self.redirect("/nimda/login")

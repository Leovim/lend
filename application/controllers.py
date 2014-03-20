#coding=utf8

import json
import tornado.web
from models import *
from config import options

# todo 推送


class BaseHandler(tornado.web.RequestHandler):
    user_model = UserModel()
    guarantee_model = GuaranteeModel()
    loan_model = LoanModel()
    behaviour_model = BehaviourModel()
    split_model = SplitLoanModel()

    def get_current_user(self):
        user_id = self.get_secure_cookie("user", max_age_days=365)
        if not user_id:
            return None
        return self.user_model.get_user_info(int(user_id))
    
    @staticmethod
    def interest_round(interest):
        return round(interest * 100) / 100

    def calc_one_interest(self, principal):
        if principal <= 200:
            return 0
        elif principal <= 300:
            return 0
        elif principal <= 400:
            return 0
        elif principal <= 500:
            return 0
        elif principal <= 600:
            return self.interest_round((principal - 500) * 0.02 / 52)
        elif principal <= 700:
            return self.interest_round(0.04 + (principal - 600) * 0.04 / 52)
        elif principal <= 800:
            return self.interest_round(0.12 + (principal - 700) * 0.06 / 52)
        elif principal <= 900:
            return self.interest_round(0.24 + (principal - 800) * 0.08 / 52)
        elif principal <= 1000:
            return self.interest_round(0.40 + (principal - 900) * 0.10 / 52)
        elif principal <= 1100:
            return self.interest_round(0.60 + (principal - 1000) * 0.12 / 52)
        elif principal <= 1200:
            return self.interest_round(0.83 + (principal - 1100) * 0.14 / 52)

    def calc_two_interest(self, principal):
        if principal <= 200:
            return 0
        elif principal <= 300:
            return self.interest_round((principal - 200) * 0.1 / 26)
        elif principal <= 400:
            return self.interest_round(0.38 + (principal - 300) * 0.11 / 26)
        elif principal <= 500:
            return self.interest_round(0.80 + (principal - 400) * 0.12 / 26)
        elif principal <= 600:
            return self.interest_round(1.26 + (principal - 500) * 0.13 / 26)
        elif principal <= 700:
            return self.interest_round(1.76 + (principal - 600) * 0.14 / 26)
        elif principal <= 800:
            return self.interest_round(2.30 + (principal - 700) * 0.15 / 26)
        elif principal <= 900:
            return self.interest_round(2.88 + (principal - 800) * 0.16 / 26)
        elif principal <= 1000:
            return self.interest_round(3.50 + (principal - 900) * 0.17 / 26)
        elif principal <= 1100:
            return self.interest_round(4.15 + (principal - 1000) * 0.18 / 26)
        elif principal <= 1200:
            return self.interest_round(4.84 + (principal - 1100) * 0.19 / 26)

    def calc_four_interest(self, principal):
        if principal <= 200:
            return 0
        elif principal <= 300:
            return self.interest_round((principal - 200) * 0.175 / 13)
        elif principal <= 400:
            return self.interest_round(1.35 + (principal - 300) * 0.180 / 13)
        elif principal <= 500:
            return self.interest_round(2.74 + (principal - 400) * 0.185 / 13)
        elif principal <= 600:
            return self.interest_round(4.16 + (principal - 500) * 0.190 / 13)
        elif principal <= 700:
            return self.interest_round(5.62 + (principal - 600) * 0.195 / 13)
        elif principal <= 800:
            return self.interest_round(7.12 + (principal - 700) * 0.200 / 13)
        elif principal <= 900:
            return self.interest_round(8.66 + (principal - 800) * 0.205 / 13)
        elif principal <= 1000:
            return self.interest_round(10.24 + (principal - 900) * 0.210 / 13)
        elif principal <= 1100:
            return self.interest_round(11.86 + (principal - 1000) * 0.215 / 13)
        elif principal <= 1200:
            return self.interest_round(13.51 + (principal - 1100) * 0.220 / 13)

    def calc_extra_interest(self, principal, term):
        return self.interest_round(principal * 0.22 * term / 52)

    def calc_interest(self, principal, term):
        # time: week number
        # rate: 22.2% = 0.222
        principal_ = int(principal)
        term_ = int(term)
        if term_ == 1:
            return self.calc_one_interest(principal_)
        elif term_ == 2:
            return self.calc_two_interest(principal_)
        elif term_ == 4:
            return self.calc_four_interest(principal_)

    @staticmethod
    def send_sms(phone, verification_code):
        url = "http://utf8.sms.webchinese.cn/?Uid=shuguozhu&Key=" \
              + options.sms_secret + "&smsMob=" + phone + "&smsText=" \
              "%E6%82%A8%E7%9A%84%E9%AA%8C%E8%AF%81%E7%A0%81%E6%98%AF" + \
              verification_code
        import urllib2
        a = urllib2.urlopen(url)
        return a.read()


class IndexHandler(BaseHandler):
    def get(self, arg):
        result_json = json.dumps([arg, {'name': "Leo中文", 'age': 20},
                                  {'name': "Smith", 'age': 17}],
                                 separators=(',', ':'), encoding="utf-8",
                                 indent=4, ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class UserHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        del user['password']
        user['loan_limit'] = self.loan_model.get_loan_limit(user['user_id'])
        result_json = json.dumps({'result': 1, 'user': user},
                                 separators=(',', ':'), encoding="utf-8",
                                 indent=4, ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class LoanHandler(BaseHandler):
    def get(self):
        # user_id = 1
        user = self.get_current_user()
        if not user:
            #raise tornado.web.HTTPError(404)
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return
        if user['status'] == 0:
            # 未完善资料
            result_json = json.dumps({'result': 2}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        result = self.loan_model.get_user_new_three_loans(user['user_id'])
        i = 0
        while i < result.__len__():
            if result[i]['guarantor1']:
                result[i]['guarantor1'] = self.user_model.\
                    get_user_real_name(result[i]['guarantor1'])
            if result[i]['guarantor2']:
                result[i]['guarantor2'] = self.user_model. \
                    get_user_real_name(result[i]['guarantor2'])
            if result[i]['split_status'] == 1:
                result[i]['split_status'] = self.split_model.get_split_info(result[i]['loan_id'])
                print result[i]['split_status']
            i += 1
        result_json = json.dumps({'result': 1, 'loans': result},
                                 separators=(',', ':'), encoding="utf-8",
                                 indent=4, ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class HistoryHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            # raise tornado.web.HTTPError(404)
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        result = self.behaviour_model.\
            get_user_new_ten_behaviours(user['user_id'])
        result_json = json.dumps({'result': 1, 'histories': result},
                                 separators=(',', ':'), encoding="utf-8",
                                 indent=4, ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class GuaranteeHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            # raise tornado.web.HTTPError(404)
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        guarantor = self.guarantee_model.get_user_guarantor(user['user_id'])
        warrantee = self.guarantee_model.get_user_warrantee(user['user_id'])
        result_json = json.dumps({'result': 1, 'guarantors': guarantor,
                                  'warrantees': warrantee},
                                 separators=(',', ':'), encoding="utf-8",
                                 indent=4, ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class LoginHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)

        user_id = self.user_model.check_username_exist(username)
        if not user_id:
            # username not exist
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     indent=4, encoding="utf-8",
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        user_info = self.user_model.get_user_info(user_id)
        # password hash
        import hashlib
        sha = hashlib.sha1()
        sha.update(password)
        sha_password = sha.hexdigest()
        if user_info['password'] == sha_password:
            histories = self.behaviour_model.\
                get_user_new_ten_behaviours(user_id)
            loans = self.loan_model.get_user_new_three_loans(user_id)
            i = 0
            while i < loans.__len__():
                if loans[i]['guarantor1']:
                    loans[i]['guarantor1'] = self.user_model. \
                        get_user_real_name(loans[i]['guarantor1'])
                if loans[i]['guarantor2']:
                    loans[i]['guarantor2'] = self.user_model. \
                        get_user_real_name(loans[i]['guarantor2'])
                if loans[i]['split_status'] == 1:
                    loans[i]['split_status'] = self.split_model.get_split_info(loans[i]['loan_id'])
                i += 1
            # success
            self.set_secure_cookie("user", str(user_id), expires_days=365)
            del user_info['password']
            user_info['loan_limit'] = \
                self.loan_model.get_loan_limit(user_info['user_id'])
            guarantor = self.guarantee_model.get_user_guarantor(user_id)
            warrantee = self.guarantee_model.get_user_warrantee(user_id)
            result_json = json.dumps({'result': 1,
                                      'user': user_info,
                                      'loans': loans,
                                      'histories': histories,
                                      'guarantors': guarantor,
                                      'warrantees': warrantee},
                                     separators=(',', ':'), indent=4,
                                     encoding="utf-8", ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        else:
            # wrong password
            result_json = json.dumps({'result': 2}, separators=(',', ':'),
                                     indent=4, encoding="utf-8",
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')


class RegisterHandler(BaseHandler):
    def post(self):
        phone = self.get_argument('phone', None)
        username = self.get_argument('username', None),
        password = self.get_argument('password', None)

        # password hash
        import hashlib
        sha = hashlib.sha1()
        sha.update(password)
        sha_password = sha.hexdigest()

        # return 1: success
        # return 2: username exist
        # return 3: phone exist
        # return 4: unknown error

        # check if username exist
        if self.user_model.check_username_exist(username):
            result_json = json.dumps({'result': 2}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        # check if phone exist
        elif self.user_model.check_phone_exist(phone):
            result_json = json.dumps({'result': 3}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        else:
            user = dict(
                username=username,
                password=sha_password,
                phone=phone
            )
            self.user_model.add_user(user)
            result_json = json.dumps({'result': 1}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)


class UpdateHandler(BaseHandler):
    def post(self):
        user = self.get_current_user()
        if not user:
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        # 获得用户真实姓名，银行卡号，支付宝账号，身份证号，学校，院系，专业，宿舍，专业，头像（图片），三张认证照片（图片）

        real_name = self.get_argument("real_name", None)
        bank_number = self.get_argument("bank_number", None)
        alipay_number = self.get_argument("alipay_number", None)
        identify_number = self.get_argument("identify_number", None)
        school = self.get_argument("school", None)
        department = self.get_argument("department", None)
        major = self.get_argument("major", None)
        dorm = self.get_argument("dorm", None)
        student_id = self.get_argument("student_id", None)

        import base64
        import time
        import os
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                  "static/images/")

        avatar_name = str(int(time.time() * 100)) + '.jpg'
        avatar = self.get_argument("avatar", None)
        avatar = base64.decodestring(avatar)
        tmp_file = open(image_path + avatar_name, "wb")
        tmp_file.write(avatar)
        tmp_file.close()

        pic1_name = str(int(time.time() * 100)) + '.jpg'
        pic1 = self.get_argument("pic1", None)
        pic1 = base64.decodestring(pic1)
        tmp_file = open(image_path + pic1_name, "wb")
        tmp_file.write(pic1)
        tmp_file.close()

        pic2_name = str(int(time.time() * 100)) + '.jpg'
        pic2 = self.get_argument("pic2", None)
        pic2 = base64.decodestring(pic2)
        tmp_file = open(image_path + pic2_name, "wb")
        tmp_file.write(pic2)
        tmp_file.close()

        pic3_name = str(int(time.time() * 100)) + '.jpg'
        pic3 = self.get_argument("pic3", None)
        pic3 = base64.decodestring(pic3)
        tmp_file = open(image_path + pic3_name, "wb")
        tmp_file.write(pic3)
        tmp_file.close()

        pic4_name = str(int(time.time() * 100)) + '.jpg'
        pic4 = self.get_argument("pic4", None)
        pic4 = base64.decodestring(pic4)
        tmp_file = open(image_path + pic4_name, "wb")
        tmp_file.write(pic4)
        tmp_file.close()

        up_user = dict(
            user_id=user['user_id'],
            real_name=real_name,
            bank_number=bank_number,
            alipay_number=alipay_number,
            identify_number=identify_number,
            school=school,
            department=department,
            major=major,
            dorm=dorm,
            student_id=student_id,
            avatar=avatar_name,
            pic1=pic1_name,
            pic2=pic2_name,
            pic3=pic3_name,
            pic4=pic4_name
        )
        self.user_model.update_user(up_user)
        result_json = json.dumps({'result': 1}, separators=(',', ':'),
                                 encoding="utf-8", indent=4,
                                 ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class LoanRequestHandler(BaseHandler):
    def post(self):
        user = self.get_current_user()
        if not user:
            # not logged in
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        loan_amount = int(self.get_argument("loan_amount", None))
        term = int(self.get_argument("term", None))

        # 检验额度，估计贷款各段利息，计算利息，根据已担保人数进行利息减免，计算手续费，计算到期日期，获取被担保人ID，写入数据库
        if self.loan_model.check_total_loan_money(user['user_id'],
                                                  loan_amount):
            result_json = json.dumps({'result': 2}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        interest = self.calc_interest(loan_amount, term)
        warrantee_reduce = self.loan_model.get_warrantee_reduce(user['user_id'])
        interest = self.interest_round(interest * warrantee_reduce)
        fee = 5
        remain_amount = loan_amount + interest + fee

        # datetime
        import datetime
        today = datetime.date.today()
        loan_date = today.__str__()
        week = datetime.timedelta(days=7)
        due_date = (today + week * term).__str__()

        guarantor = self.guarantee_model.get_user_guarantor(user['user_id'])
        guarantor1 = None
        guarantor2 = None
        if guarantor.__len__() == 1:
            # change to user_id
            guarantor1 = int(guarantor[0]['user_id'])
        elif guarantor.__len__() == 2:
            # change to user_id
            guarantor1 = int(guarantor[0]['user_id'])
            guarantor2 = int(guarantor[1]['user_id'])
        loan = dict(
            user_id=user['user_id'],
            # need to check
            guarantor1=guarantor1,
            guarantor2=guarantor2,
            loan_amount=loan_amount,
            remain_amount=remain_amount,
            loan_date=loan_date,
            due_date=due_date
        )
        self.loan_model.add_loan(loan)

        this_loan = self.loan_model.get_user_new_three_loans(user['user_id'])
        loan_id = int(this_loan[0]['loan_id'])
        behaviour = dict(
            user_id=user['user_id'],
            loan_id=loan_id,
            bhv_type=1,
            money=loan_amount,
            time=loan_date,
            check_status=0
        )
        self.behaviour_model.add_behaviour(behaviour)

        result_json = json.dumps({'result': 1}, separators=(',', ':'),
                                 encoding="utf-8", indent=4,
                                 ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class DueRequestHandler(BaseHandler):
    def post(self):
        user = self.get_current_user()
        if not user:
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        loan_id = int(self.get_argument("loan_id", None))
        term = int(self.get_argument("term", None))
        loan_info = self.loan_model.get_loan_info(loan_id)
        # 只能逾期两次
        if loan_info['due_status'] == 2:
            result_json = json.dumps({'result': 2}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        import datetime
        due_date_list = loan_info['due_date'].split('-')
        due_date = datetime.date(year=int(due_date_list[0]),
                                 month=int(due_date_list[1]),
                                 day=int(due_date_list[2]))
        week = datetime.timedelta(days=7)
        due_date = (due_date + week * term).__str__()

        interest = self.calc_extra_interest(loan_info['loan_amount'], term)
        warrantee_num = self.guarantee_model. \
            get_user_warrantee(user['user_id']).__len__()
        if warrantee_num == 1:
            interest = self.interest_round(interest * 0.9)
        elif warrantee_num == 2:
            interest = self.interest_round(interest * 0.8)
        fee = 5
        remain_amount = loan_info['remain_amount'] + interest + fee

        # update data
        self.loan_model.change_due_status(loan_info['loan_id'],
                                          loan_info['due_status']+1,
                                          due_date,
                                          remain_amount)
        # create behaviour
        behaviour = dict(
            user_id=loan_info['user_id'],
            loan_id=loan_info['loan_id'],
            bhv_type=loan_info['due_status']+4,
            money=remain_amount,
            time=datetime.date.today().__str__(),
            check_status=1
        )
        self.behaviour_model.add_behaviour(behaviour)
        result_json = json.dumps({'result': 1}, separators=(',', ':'),
                                 encoding="utf-8", indent=4, ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class SplitRequestHandler(BaseHandler):
    def post(self):
        user = self.get_current_user()
        if not user:
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        loan_id = int(self.get_argument("loan_id", None))
        total_time = int(self.get_argument("total_time", None))
        interval_due = int(self.get_argument("interval_due", None))

        # 获得该loan info
        loan_info = self.loan_model.get_loan_info(loan_id)

        if loan_info['due_status'] > 0:
            # 不能同时分期和逾期
            result_json = json.dumps({'result': 3}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        if loan_info['split_status'] == 1:
            # 只能分期一次
            result_json = json.dumps({'result': 4}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        # 计算新的还款日期
        import datetime
        due_date_list = loan_info['due_date'].split('-')
        due_date = datetime.date(year=int(due_date_list[0]),
                                 month=int(due_date_list[1]),
                                 day=int(due_date_list[2]))
        week = datetime.timedelta(days=7)
        term = total_time * interval_due
        due_date = (due_date + week * term).__str__()

        # 计算新的还款额
        interest = self.calc_extra_interest(loan_info['loan_amount'], term)
        warrantee_num = self.guarantee_model. \
            get_user_warrantee(user['user_id']).__len__()
        if warrantee_num == 1:
            interest = self.interest_round(interest * 0.9)
        elif warrantee_num == 2:
            interest = self.interest_round(interest * 0.8)
        fee = 5
        remain_amount = loan_info['remain_amount'] + interest + fee

        loan = dict(
            loan_id=loan_info['loan_id'],
            remain_amount=remain_amount,
            due_date=due_date,
        )

        # 计算每次还款额
        amount_per = self.interest_round(remain_amount/total_time)

        # 计算下次还款日期
        now_date = datetime.date(year=int(due_date_list[0]),
                                 month=int(due_date_list[1]),
                                 day=int(due_date_list[2]))
        week = datetime.timedelta(days=7)
        next_date = (now_date + week * interval_due).__str__()

        split = dict(
            loan_id=loan['loan_id'],
            total_time=total_time,
            interval_due=interval_due,
            amount_per=amount_per,
            next_date=next_date
        )

        # create behaviour
        behaviour = dict(
            user_id=loan_info['user_id'],
            loan_id=loan_info['loan_id'],
            bhv_type=3,
            money=remain_amount,
            time=datetime.date.today().__str__(),
            check_status=1
        )

        # update data
        if self.loan_model.update_loan(loan):
            self.split_model.add_split(split)
            self.behaviour_model.add_behaviour(behaviour)

            result_json = json.dumps({'result': 1}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
        else:
            # error
            result_json = json.dumps({'result': 2}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)


class GuaranteeRequestHandler(BaseHandler):
    def post(self):
        user = self.get_current_user()
        if not user:
            result_json = json.dumps({'result': 0}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        guarantor_name = self.get_argument("guarantor_name", None)
        phone = self.get_argument("phone", None)
        guarantor_id = self.user_model.check_username_exist(guarantor_name)
        if not guarantor_id:
            # 担保人不存在
            result_json = json.dumps({'result': 2},
                                     separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        guarantor = self.user_model.get_user_info(guarantor_id)
        if guarantor['status'] == 1:
            if guarantor['phone'] == phone:
                if self.guarantee_model.get_user_guarantor(user['user_id']).__len__() > 1:
                    # 用户已有2个担保人
                    result_json = json.dumps({'result': 5},
                                             separators=(',', ':'),
                                             encoding="utf-8", indent=4,
                                             ensure_ascii=False)
                    self.render("index.html", title="Lend",
                                result_json=result_json)
                    return
                if self.guarantee_model.get_user_warrantee(guarantor_id).__len__() > 1:
                    # 对方不能担保2名以上用户
                    result_json = json.dumps({'result': 6},
                                             separators=(',', ':'),
                                             encoding="utf-8", indent=4,
                                             ensure_ascii=False)
                    self.render("index.html", title="Lend",
                                result_json=result_json)
                    return

                guarantee = dict(
                    guarantor_id=guarantor_id,
                    warrantee_id=user['user_id']
                )
                self.guarantee_model.add_guarantee(guarantee)
                result_json = json.dumps({'result': 1},
                                         separators=(',', ':'),
                                         encoding="utf-8", indent=4,
                                         ensure_ascii=False)
                self.render("index.html", title="Lend",
                            result_json=result_json)
            else:
                # 用户电话号码不匹配
                result_json = json.dumps({'result': 3},
                                         separators=(',', ':'),
                                         encoding="utf-8", indent=4,
                                         ensure_ascii=False)
                self.render("index.html", title="Lend",
                            result_json=result_json)
        else:
            # 该用户没有完善资料
            result_json = json.dumps({'result': 4},
                                     separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend",
                        result_json=result_json)


class SendSmsHandler(BaseHandler):
    def post(self):
        phone = self.get_argument("phone", None)
        verify = self.get_argument("verify", None)
        result = self.send_sms(phone, verify)

        result_json = json.dumps({'result': result}, separators=(',', ':'),
                                 encoding="utf-8", indent=4,
                                 ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)


class UploadHandler(BaseHandler):
    def post(self):
        import time
        import os
        import base64
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                  "static/images/")
        pic_name = image_path + str(int(time.time() * 100)) + '.' + self.get_argument("format", None)
        pic = self.get_argument("pic", None)
        pic = base64.decodestring(pic)

        tmp_file = open(pic_name, "wb")
        tmp_file.write(pic)
        tmp_file.close()

        result_json = json.dumps({'result': pic_name}, separators=(',', ':'),
                                 encoding="utf-8", indent=4,
                                 ensure_ascii=False)
        self.render("index.html", title="Lend", result_json=result_json)

#coding=utf8

import json
import tornado.web
from models import *
from config import options

# todo 分期请求处理
# todo 推送


class BaseHandler(tornado.web.RequestHandler):
    user_model = UserModel()
    guarantee_model = GuaranteeModel()
    loan_model = LoanModel()
    behaviour_model = BehaviourModel()

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
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
    # todo 用户完善资料后才能借款
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

        result = self.loan_model.get_user_new_three_loans(user['user_id'])
        i = 0
        while i < result.__len__():
            if result[i]['guarantor1']:
                result[i]['guarantor1'] = self.user_model.\
                    get_user_real_name(result[i]['guarantor1'])
            if result[i]['guarantor2']:
                result[i]['guarantor2'] = self.user_model. \
                    get_user_real_name(result[i]['guarantor2'])
            i += 1
        result_json = json.dumps({'result': 1, 'loan': result},
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
        result_json = json.dumps({'result': 1, 'history': result},
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
        result_json = json.dumps({'result': 1, 'guarantor': guarantor,
                                  'warrantee': warrantee},
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
            # success
            self.set_secure_cookie("user", str(user_id))
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

        # todo 获得用户真实姓名，银行卡号，支付宝账号，身份证号，学校，院系，专业，宿舍，专业，头像（图片），三张认证照片（图片）
        if self.request.files == {}:
            # 没有文件上传
            result_json = json.dumps({'result': 2}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        real_name = self.get_argument("real_name", None)
        bank_number = self.get_argument("bank_number", None)
        alipay_number = self.get_argument("alipay_number", None)
        identify_number = self.get_argument("identify_number", None)
        school = self.get_argument("school", None)
        department = self.get_argument("department", None)
        major = self.get_argument("major", None)
        dorm = self.get_argument("dorm", None)
        student_id = self.get_argument("student_id", None)

        import tempfile
        from PIL import Image
        import time
        import os
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                  "static/images/")

        avatar = self.request.files['avatar'][0]
        pic1 = self.request.files['pic1'][0]
        pic2 = self.request.files['pic2'][0]

        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(avatar['body'])
        tmp_file.seek(0)
        img = Image.open(tmp_file.name)
        image_format = avatar['filename'].split('.').pop().lower()
        avatar_name = str(int(time.time() * 100)) + '.' + image_format
        img.save(image_path + avatar_name)
        tmp_file.close()

        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(pic1['body'])
        tmp_file.seek(0)
        img = Image.open(tmp_file.name)
        image_format = pic1['filename'].split('.').pop().lower()
        pic1_name = str(int(time.time() * 100)) + '.' + image_format
        img.save(image_path + pic1_name)
        tmp_file.close()

        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(pic2['body'])
        tmp_file.seek(0)
        img = Image.open(tmp_file.name)
        image_format = pic2['filename'].split('.').pop().lower()
        pic2_name = str(int(time.time() * 100)) + '.' + image_format
        img.save(image_path + pic2_name)
        tmp_file.close()

        pic3 = self.request.files['pic3'][0]
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(pic3['body'])
        tmp_file.seek(0)
        img = Image.open(tmp_file.name)
        image_format = pic3['filename'].split('.').pop().lower()
        pic3_name = str(int(time.time() * 100)) + '.' + image_format
        img.save(image_path + pic3_name)
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
            pic3=pic3_name
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
        warrantee_num = self.guarantee_model.\
            get_user_warrantee(user['user_id']).__len__()
        if warrantee_num == 1:
            interest = self.interest_round(interest * 0.9)
        elif warrantee_num == 2:
            interest = self.interest_round(interest * 0.8)
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
            guarantor1 = int(guarantor[0]['guarantor_id'])
        elif guarantor.__len__() == 2:
            guarantor1 = int(guarantor[0]['guarantor_id'])
            guarantor2 = int(guarantor[1]['guarantor_id'])
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
        loan = self.loan_model.get_loan_info(loan_id)
        # 只能逾期两次
        if loan['due_status'] == 2:
            result_json = json.dumps({'result': 2}, separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        import datetime
        due_date_list = loan['due_date'].split('-')
        due_date = datetime.date(year=int(due_date_list[0]),
                                 month=int(due_date_list[1]),
                                 day=int(due_date_list[2]))
        week = datetime.timedelta(days=7)
        due_date = (due_date + week * term).__str__()

        interest = self.calc_extra_interest(loan['loan_amount'], term)
        warrantee_num = self.guarantee_model. \
            get_user_warrantee(user['user_id']).__len__()
        if warrantee_num == 1:
            interest = self.interest_round(interest * 0.9)
        elif warrantee_num == 2:
            interest = self.interest_round(interest * 0.8)
        fee = 5
        remain_amount = loan['remain_amount'] + interest + fee

        # update data
        self.loan_model.change_due_status(loan['loan_id'],
                                          loan['due_status']+1,
                                          due_date,
                                          remain_amount)
        # create behaviour
        behaviour = dict(
            user_id=loan['user_id'],
            loan_id=loan['loan_id'],
            bhv_type=loan['due_status']+4,
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
        loan_id = self.get_argument("loan_id", None)
        result_json = json.dumps({'result': loan_id}, separators=(',', ':'),
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
        verify = self.get_argument("verify", None)
        guarantor_id = self.user_model.check_username_exist(guarantor_name)
        if not guarantor_id:
            result_json = json.dumps({'result': 2},
                                     separators=(',', ':'),
                                     encoding="utf-8", indent=4,
                                     ensure_ascii=False)
            self.render("index.html", title="Lend", result_json=result_json)
            return

        guarantor = self.user_model.get_user_info(guarantor_id)
        if guarantor['status'] == 1:
            if guarantor['phone'] == phone:
                result = self.send_sms(phone, verify)
                result_json = json.dumps({'result': result},
                                         separators=(',', ':'),
                                         encoding="utf-8", indent=4,
                                         ensure_ascii=False)
                self.render("index.html", title="Lend",
                            result_json=result_json)
            else:
                # 用户电话号码不匹配
                result_json = json.dumps({'result': 2},
                                         separators=(',', ':'),
                                         encoding="utf-8", indent=4,
                                         ensure_ascii=False)
                self.render("index.html", title="Lend",
                            result_json=result_json)
        else:
            # 该用户没有完善资料
            result_json = json.dumps({'result': 2},
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

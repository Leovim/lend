#coding=utf8

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import *
from db import *

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()


class BaseModel():
    def __init__(self):
        pass

    @staticmethod
    def change_list(result_list):
        i = 0
        while i < result_list.__len__():
            result_list[i] = result_list[i].as_dict()
            i += 1
        return result_list


class UserModel(BaseModel):
    @staticmethod
    def add_user(user):
        new_user = User(username=user['username'],
                        password=user['password'],
                        phone=user['phone'])
        session.add(new_user)
        # session.commit()

    @staticmethod
    def delete_user(user_id):
        user = session.query(User).filter(User.user_id == user_id)
        session.delete(user)
        # session.commit()

    @staticmethod
    def update_user(user):
        # user = dict(
        #     real_name
        #     bank_number
        #     alipay_number
        #     identify_number
        #     school
        #     department
        #     major
        #     dorm
        #     student_id
        #     avatar
        #     pic1
        #     pic2
        #     pic3
        #     pic4
        # )
        up_user = session.query(User).filter(User.user_id == user['user_id'])\
            .one()
        up_user.real_name = user['real_name']
        up_user.bank_number = user['bank_number']
        up_user.alipay_number = user['alipay_number']
        up_user.identify_number = user['identify_number']
        up_user.school = user['school']
        up_user.department = user['department']
        up_user.major = user['major']
        up_user.student_id = user['student_id']
        up_user.dorm = user['dorm']
        up_user.avatar = user['avatar']
        up_user.pic1 = user['pic1']
        up_user.pic2 = user['pic2']
        up_user.pic3 = user['pic3']
        up_user.pic4 = user['pic4']
        up_user.status = 1
        # session.commit()

    @staticmethod
    def update_user_info(user):
        # user = dict(
        #     real_name
        #     bank_number
        #     alipay_number
        #     identify_number
        #     school
        #     department
        #     major
        #     dorm
        #     student_id
        # )
        up_user = session.query(User).filter(User.user_id == user['user_id']) \
            .one()
        up_user.real_name = user['real_name']
        up_user.bank_number = user['bank_number']
        up_user.alipay_number = user['alipay_number']
        up_user.identify_number = user['identify_number']
        up_user.school = user['school']
        up_user.department = user['department']
        up_user.major = user['major']
        up_user.student_id = user['student_id']
        up_user.dorm = user['dorm']
        # session.commit()

    @staticmethod
    def update_user_password(user_id, password):
        # user = dict(
        #     user_id=user_id,
        #     password=password
        # )
        up_user = session.query(User).filter(User.user_id == user_id).one()
        up_user.password = password
        # session.commit()

    @staticmethod
    def update_user_avatar(user):
        # user = dict(
        #     user_id=user_id,
        #     avatar=avatar
        # )
        up_user = session.query(User).filter(User.user_id == user['user_id']) \
            .one()
        up_user.avatar = user['avatar']
        # session.commit()

    @staticmethod
    def update_user_status(user_id):
        # change user status to 1 完善资料之后
        up_user = session.query(User).filter(User.user_id == user_id).one()
        up_user.status = 1
        # session.commit()

    @staticmethod
    def update_user_credit(user_id, credit):
        user = session.query(User).filter(User.user_id == user_id).one()
        user.credit = int(credit)
        # session.commit()

    def get_all_users(self):
        try:
            users = session.query(User).all()
        except NoResultFound:
            return []
        return self.change_list(users)

    @staticmethod
    def get_user_info(user_id):
        try:
            user = session.query(User).filter(User.user_id == user_id).one()
        except NoResultFound:
            return False
        return user.as_dict()

    @staticmethod
    def get_user_id(username):
        try:
            user = session.query(User).filter(User.username == username).one()
        except NoResultFound:
            return False
        return int(user.user_id)

    @staticmethod
    def get_user_real_name(user_id):
        try:
            user = session.query(User).filter(User.user_id == user_id).one()
        except NoResultFound:
            return False
        return user.real_name

    @staticmethod
    def check_username_exist(username):
        try:
            user = session.query(User).filter(User.username == username).one()
        except NoResultFound:
            return False
        return user.user_id

    @staticmethod
    def check_phone_exist(phone):
        try:
            user = session.query(User).filter(User.phone == phone).one()
        except NoResultFound:
            return False
        except MultipleResultsFound:
            return True
        return user.user_id


class GuaranteeModel(BaseModel):
    @staticmethod
    def add_guarantee(guarantee):
        new_guarantee = Guarantee(guarantor_id=guarantee['guarantor_id'],
                                  warrantee_id=guarantee['warrantee_id'],
                                  status=0)
        session.add(new_guarantee)
        # session.commit()

    @staticmethod
    def delete_guarantee(guarantor_id, warrantee_id):
        guarantee = session.query(Guarantee).\
            filter(Guarantee.guarantor_id == guarantor_id).\
            filter(Guarantee.warrantee_id == warrantee_id).one()
        session.delete(guarantee)
        # session.commit()

    @staticmethod
    def change_status(guarantee_id):
        # 审核完成
        guarantee = session.query(Guarantee). \
            filter(Guarantee.guarantee_id == guarantee_id).one()
        guarantee.status = 1
        # session.commit()

    def check_guarantee_exist(self, guarantor_id, warrantee_id):
        try:
            g = session.query(Guarantee).\
                filter(Guarantee.guarantor_id == guarantor_id).\
                filter(Guarantee.warrantee_id == warrantee_id).one()
        except NoResultFound:
            return False
        return g.guarantee_id

    @staticmethod
    def get_user_guarantor(user_id):
        # 担保人
        try:
            g = session.query(Guarantee).\
                filter(Guarantee.warrantee_id == int(user_id)).all()
        except NoResultFound:
            return []

        if g.__len__() == 1:
            try:
                ga = session.query(User).\
                    filter(User.user_id == g[0].guarantor_id).one()
            except NoResultFound:
                return []
            a = []
            b = dict(
                user_id=ga.user_id,
                real_name=ga.real_name
            )
            a.append(b)
        else:
            a = []
            for item in g:
                try:
                    ga = session.query(User).\
                        filter(User.user_id == item.guarantor_id).one()
                except NoResultFound:
                    continue
                b = dict(
                    user_id=ga.user_id,
                    real_name=ga.real_name
                )
                a.append(b)
        return a

    @staticmethod
    def get_user_warrantee(user_id):
        # 被担保人
        try:
            w = session.query(Guarantee). \
                filter(Guarantee.guarantor_id == int(user_id)).all()
        except NoResultFound:
            return []

        if w.__len__() == 1:
            try:
                wa = session.query(User). \
                    filter(User.user_id == w[0].warrantee_id).one()
            except NoResultFound:
                return []
            a = []
            b = dict(
                user_id=wa.user_id,
                real_name=wa.real_name
            )
            a.append(b)
        else:
            a = []
            for item in w:
                try:
                    wa = session.query(User). \
                        filter(User.user_id == item.warrantee_id).one()
                except NoResultFound:
                    continue
                b = dict(
                    user_id=wa.user_id,
                    real_name=wa.real_name
                )
                a.append(b)
        return a

    def get_all_guarantee(self):
        try:
            guarantee = session.query(Guarantee).filter(Guarantee.status == 1)\
                .all()
        except NoResultFound:
            return []
        return self.change_list(guarantee)

    def get_all_unchecked_guarantee(self):
        try:
            guarantee = session.query(Guarantee).filter(Guarantee.status == 0)\
                .all()
        except NoResultFound:
            return []
        return self.change_list(guarantee)


class LoanModel(BaseModel):
    @staticmethod
    def add_loan(loan):
        new_loan = Loan(user_id=loan['user_id'],
                        guarantor1=loan['guarantor1'],
                        guarantor2=loan['guarantor2'],
                        loan_amount=loan['loan_amount'],
                        remain_amount=loan['remain_amount'],
                        loan_date=loan['loan_date'],
                        due_date=loan['due_date'],
                        split_status=0,
                        due_status=0,
                        check_status=0)
        session.add(new_loan)
        # session.commit()

    @staticmethod
    def delete_loan(loan_id):
        loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
        session.delete(loan)
        # session.commit()

    @staticmethod
    def update_loan(loan):
        try:
            up_loan = session.query(Loan).filter(Loan.loan_id ==
                                                 loan['loan_id']).one()
        except NoResultFound:
            return False
        up_loan.remain_amount = loan['remain_amount']
        up_loan.due_date = loan['due_date']
        up_loan.split_status = 1
        # session.commit()
        return True

    @staticmethod
    def update_remain_amount(loan_id, remain_amount):
        loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
        loan.remain_amount = remain_amount
        # session.commit()

    # @staticmethod
    # def update_due_date(loan_id, due_date):
    #     loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
    #     loan.due_date = due_date
    #     session.commit()

    @staticmethod
    def change_due_status(loan_id, status, due_date, remain_amount):
        loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
        loan.due_status = int(status)
        loan.due_date = due_date
        loan.remain_amount = remain_amount
        # session.commit()

    @staticmethod
    def change_split_status(loan_id, status):
        # status: 0 未分期
        #         1 分期
        loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
        loan.split_status = int(status)
        # session.commit()

    @staticmethod
    def change_check_status(loan_id, status):
        # status: 0 wait to check
        #         1 ing
        #         2 complete
        loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
        loan.check_status = int(status)
        # session.commit()

    @staticmethod
    def get_loan_info(loan_id):
        try:
            loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
        except NoResultFound:
            return False
        return loan.as_dict()

    def get_user_all_loans(self, user_id):
        try:
            loans = session.query(Loan).filter(Loan.user_id == user_id).\
                order_by(Loan.loan_id.desc()).all()
        except NoResultFound:
            return []

        return self.change_list(loans)

    def get_user_new_three_loans(self, user_id):
        # order_by 默认升序 可使用order_by(Loan.loan_id.desc())显示降序结果
        # 可能不够3个，需要做处理
        try:
            loans = session.query(Loan).filter(Loan.user_id == user_id). \
                filter(Loan.check_status != 2).order_by(Loan.loan_id.desc()).\
                all()
        except NoResultFound:
            return []

        if loans.__len__() == 1 or loans.__len__() == 2:
            return self.change_list(loans)
        else:
            return self.change_list(loans[0:3])

    def get_all_unchecked_loans(self):
        try:
            loans = session.query(Loan).filter(Loan.check_status == 0)\
                .order_by(Loan.loan_id.desc()).all()
        except NoResultFound:
            return []
        return self.change_list(loans)

    def get_all_ing_loans(self):
        try:
            loans = session.query(Loan).filter(Loan.check_status == 1)\
                .order_by(Loan.loan_id.desc()).all()
        except NoResultFound:
            return []
        return self.change_list(loans)

    def get_all_complete_loans(self):
        try:
            loans = session.query(Loan).filter(Loan.check_status == 2)\
                .order_by(Loan.loan_id.desc()).all()
        except NoResultFound:
            return []
        return self.change_list(loans)

    @staticmethod
    def get_warrantee_reduce(user_id):
        try:
            count = session.query(Guarantee). \
                filter(Guarantee.guarantor_id == user_id). \
                filter(Guarantee.status == 1).count()
        except NoResultFound:
            return 1
        if count == 0:
            return 1
        elif count == 1:
            return 0.9
        elif count == 2:
            return 0.8

    @staticmethod
    def get_loan_limit(user_id):
        try:
            count = session.query(Guarantee).\
                filter(Guarantee.warrantee_id == user_id).\
                filter(Guarantee.status == 1).count()
        except NoResultFound:
            return 300
        if count == 0:
            return 300
        elif count == 1:
            return 700
        elif count == 2:
            return 1200

    def check_total_loan_money(self, user_id, loan_amount):
        # return true 已超额
        # return false 未超额
        try:
            loans = session.query(Loan).filter(Loan.user_id == user_id).\
                filter(Loan.check_status.in_([0, 1])).all()
        except NoResultFound:
            return False

        total_loan_money = 0
        for item in loans:
            total_loan_money += item.loan_amount

        total_loan_money += loan_amount
        loan_limit = self.get_loan_limit(user_id)
        print "total_loan_money = %d" % total_loan_money
        print "loan_limit = %d" % loan_limit
        if total_loan_money <= loan_limit:
            return False
        else:
            return True


class BehaviourModel(BaseModel):
    @staticmethod
    def add_behaviour(behaviour):
        # 1. 借款
        # 2. 还款
        # 3. 分期
        # 4. 逾期
        new_behaviour = Behaviour(user_id=behaviour['user_id'],
                                  loan_id=behaviour['loan_id'],
                                  bhv_type=behaviour['bhv_type'],
                                  money=behaviour['money'],
                                  time=behaviour['time'],
                                  check_status=behaviour['check_status'])
        session.add(new_behaviour)
        # session.commit()

    @staticmethod
    def delete_behaviour(behaviour_id):
        behaviour = session.query(Behaviour).\
            filter(Behaviour.behaviour_id == behaviour_id).one()
        session.delete(behaviour)
        # session.commit()

    @staticmethod
    def change_status(behaviour_id, status):
        behaviour = session.query(Behaviour). \
            filter(Behaviour.behaviour_id == behaviour_id).one()
        behaviour.check_status = int(status)
        # session.commit()
        
    def get_user_all_behaviours(self, user_id):
        try:
            behaviours = session.query(Behaviour).\
                filter(Behaviour.user_id == user_id).\
                order_by(Behaviour.behaviour_id.desc()).all()
        except NoResultFound:
            return []

        return self.change_list(behaviours)

    def get_user_new_ten_behaviours(self, user_id):
        try:
            behaviours = session.query(Behaviour).\
                filter(Behaviour.user_id == user_id).\
                order_by(Behaviour.behaviour_id.desc()).all()
        except NoResultFound:
            return []

        if behaviours.__len__() < 10:
            return self.change_list(behaviours)
        else:
            return self.change_list(behaviours[0:10])

    def get_all_unchecked_behaviours(self):
        try:
            behaviours = session.query(Behaviour).\
                filter(Behaviour.check_status == 0).all()
        except NoResultFound:
            return []

        return self.change_list(behaviours)

    def get_loan_behaviour(self, loan_id):
        try:
            behaviours = session.query(Behaviour). \
                filter(Behaviour.loan_id == loan_id).all()
        except NoResultFound:
            return []

        return self.change_list(behaviours)

    def get_loan_pay_behaviour(self, loan_id):
        try:
            behaviour = session.query(Behaviour). \
                filter(Behaviour.loan_id == loan_id). \
                filter(Behaviour.bhv_type == 2).\
                filter(Behaviour.check_status == 0).one()
        except NoResultFound:
            return False

        return behaviour.as_dict()


class SplitLoanModel(BaseModel):
    @staticmethod
    def add_split(split):
        new_split = SplitLoan(loan_id=split['loan_id'],
                              total_time=split['total_time'],
                              interval_due=split['interval_due'],
                              amount_per=split['amount_per'],
                              next_date=split['next_date'])
        session.add(new_split)
        # session.commit()

    @staticmethod
    def get_split_info(loan_id):
        try:
            split = session.query(SplitLoan).filter(SplitLoan.loan_id
                                                    == loan_id).one()
        except NoResultFound:
            return False

        return split.as_dict()

    @staticmethod
    def change_next_time(split_id, next_date):
        try:
            split = session.query(SplitLoan).filter(SplitLoan.split_id
                                                    == split_id).one()
        except NoResultFound:
            return False

        split.next_date = next_date
        # session.commit()


class PayModel(BaseModel):
    @staticmethod
    def add_pay(pay):
        new_pay = Pay(loan_id=pay['loan_id'],
                      type=pay['type'],
                      amount=pay['amount'],
                      check_status=pay['check_status'],
                      date=pay['date'])
        session.add(new_pay)
        # session.commit()

    def update_check_status(self, pay_id):
        try:
            pay = session.query(Pay).filter(Pay.pay_id == pay_id).one()
        except NoResultFound:
            return False
        pay.check_status = 1
        # session.commit()
        return True

    @staticmethod
    def get_pay_info(pay_id):
        try:
            pay = session.query(Pay).filter(Pay.pay_id == pay_id).one()
        except NoResultFound:
            return False
        return pay.as_dict()

    def get_all_unchecked_pay(self):
        try:
            pay = session.query(Pay).filter(Pay.check_status == 0).all()
        except NoResultFound:
            return []
        return self.change_list(pay)

    def get_all_complete_pay(self):
        try:
            pay = session.query(Pay).filter(Pay.check_status == 1).all()
        except NoResultFound:
            return []
        return self.change_list(pay)

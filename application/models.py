#coding=utf8

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import *
from db import *

Session = sessionmaker(bind=engine)
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
        session.commit()

    @staticmethod
    def delete_user(user_id):
        user = session.query(User).filter(User.user_id == user_id)
        session.delete(user)
        session.commit()

    @staticmethod
    def update_user(user):
        # user = dict(
        #     phone = phone,
        #     real_name = real_name,
        #     bank_number = bank_number,
        #     alipay_number = alipay_number
        # )
        up_user = session.query(User).filter(User.user_id == user['user_id'])\
            .one()
        up_user.phone = user['phone']
        up_user.real_name = user['real_name']
        up_user.bank_number = user['bank_number']
        up_user.alipay_number = user['alipay_number']
        session.commit()

    @staticmethod
    def update_user_password(user):
        # user = dict(
        #     user_id=user_id,
        #     password=password
        # )
        up_user = session.query(User).filter(User.user_id == user['user_id'])\
            .one()
        up_user.password = user['password']
        session.commit()

    @staticmethod
    def update_user_avatar(user):
        # user = dict(
        #     user_id=user_id,
        #     avatar=avatar
        # )
        up_user = session.query(User).filter(User.user_id == user['user_id']) \
            .one()
        up_user.avatar = user['avatar']
        session.commit()

    @staticmethod
    def update_user_credit(user_id, credit):
        user = session.query(User).filter(User.user_id == user_id).one()
        user.credit = int(credit)
        session.commit()

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
            session.query(User).filter(User.phone == phone).one()
        except NoResultFound:
            return False
        except MultipleResultsFound:
            return True
        return True


class GuaranteeModel(BaseModel):
    @staticmethod
    def add_guarantee(guarantee):
        new_guarantee = Guarantee(guarantor_id=guarantee['guarantor_id'],
                                  warrantee_id=guarantee['warrantee_id'],
                                  status=0)
        session.add(new_guarantee)
        session.commit()

    @staticmethod
    def delete_guarantee(guarantee_id):
        guarantee = session.query(Guarantee).\
            filter(Guarantee.guarantee_id == guarantee_id).one()
        session.delete(guarantee)
        session.commit()

    @staticmethod
    def change_status(guarantee_id):
        # 审核完成
        guarantee = session.query(Guarantee). \
            filter(Guarantee.guarantee_id == guarantee_id).one()
        guarantee.status = 1
        session.commit()

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
        session.commit()

    @staticmethod
    def delete_loan(loan_id):
        loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
        session.delete(loan)
        session.commit()

    @staticmethod
    def update_remain_amount(loan_id, remain_amount):
        loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
        loan.remain_amount = int(remain_amount)
        session.commit()

    @staticmethod
    def change_due_status(loan_id, status):
        loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
        loan.due_status = int(status)
        session.commit()

    @staticmethod
    def change_split_status(loan_id, status):
        # status: 0 未分期
        #         1 分期一次
        #         2 两次
        #         3 三次
        loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
        loan.split_status = int(status)
        session.commit()

    @staticmethod
    def change_check_status(loan_id, status):
        # status: 0 wait to check
        #         1 ing
        #         2 complete
        loan = session.query(Loan).filter(Loan.loan_id == loan_id).one()
        loan.check_status = int(status)
        session.commit()

    def get_user_all_loans(self, user_id):
        try:
            loans = session.query(Loan).filter(Loan.user_id == user_id).all()
        except NoResultFound:
            return False

        return self.change_list(loans)

    def get_user_new_three_loans(self, user_id):
        # order_by 默认升序 可使用order_by(Loan.loan_id.desc())显示降序结果
        # 可能不够3个，需要做处理
        try:
            loans = session.query(Loan).filter(Loan.user_id == user_id). \
                order_by(Loan.user_id.desc()).all()
        except NoResultFound:
            return False

        if loans.__len__() == 1 or loans.__len__() == 2:
            return self.change_list(loans)
        else:
            return self.change_list(loans[0:3])

    def get_all_unchecked_loans(self):
        try:
            loans = session.query(Loan).filter(Loan.check_status == 0).all()
        except NoResultFound:
            return False
        return self.change_list(loans)

    @staticmethod
    def get_loan_limit(user_id):
        try:
            count = session.query(Guarantee).\
                filter(Guarantee.warrantee_id == user_id).count()
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
                                  type=behaviour['type'],
                                  money=behaviour['money'],
                                  time=behaviour['time'],
                                  check_status=behaviour['check_status'])
        session.add(new_behaviour)
        session.commit()

    @staticmethod
    def delete_behaviour(behaviour_id):
        behaviour = session.query(Behaviour).\
            filter(Behaviour.behaviour_id == behaviour_id).one()
        session.delete(behaviour)
        session.commit()

    @staticmethod
    def change_status(behaviour_id, status):
        behaviour = session.query(Behaviour). \
            filter(Behaviour.behaviour_id == behaviour_id).one()
        behaviour.check_status = int(status)
        session.commit()
        
    def get_user_all_behaviours(self, user_id):
        try:
            behaviours = session.query(Behaviour).\
                filter(Behaviour.user_id == user_id).\
                order_by(Behaviour.behaviour_id.desc()).all()
        except NoResultFound:
            return False

        return self.change_list(behaviours)

    def get_user_new_ten_behaviours(self, user_id):
        try:
            behaviours = session.query(Behaviour).\
                filter(Behaviour.user_id == user_id).\
                order_by(Behaviour.behaviour_id.desc()).all()
        except NoResultFound:
            return False

        if behaviours.__len__() < 10:
            return self.change_list(behaviours)
        else:
            return self.change_list(behaviours[0:10])
        pass
    
    def get_all_unchecked_behaviours(self):
        try:
            behaviours = session.query(Behaviour).\
                filter(Behaviour.check_status == 0).all()
        except NoResultFound:
            return False

        return self.change_list(behaviours)

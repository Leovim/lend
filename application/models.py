#coding=utf8

from sqlalchemy.orm import sessionmaker
from db import *

Session = sessionmaker(bind=engine)
session = Session()


class UserModel():
    def add_user(self, user):
        new_user = User(username=user['username'],
                        password=user['password'],
                        phone=user['phone'])
        session.add(new_user)
        session.commit()
        
    def delete_user(self, user_id):
        user = session.query(User).filter(User.user_id == user_id)
        session.delete(user)
        session.commit()

    def update_user(self, user):
        '''
        user = dict(
            phone = phone,
            real_name = real_name,
            bank_number = bank_number,
            alipay_number = alipay_number
        )
        '''
        up_user = session.query(User).filter(User.user_id==user['user_id'])\
            .one()
        up_user.phone = user['phone']
        up_user.real_name = user['real_name']
        up_user.bank_number = user['bank_number']
        up_user.alipay_number = user['alipay_number']
        session.commit()
        
    def update_user_password(self, user):
        '''
        user = dict(
            user_id=user_id,
            password=password
        )
        '''
        up_user = session.query(User).filter(User.user_id==user['user_id'])\
            .one()
        up_user.password = user['password']
        session.commit()

    def update_user_avatar(self, user):
        '''
        user = dict(
            user_id=user_id,
            avatar=avatar
        )
        '''
        up_user = session.query(User).filter(User.user_id==user['user_id']) \
            .one()
        up_user.avatar = user['avatar']
        session.commit()


class GuaranteeModel():
    def add_guarantee(self, guarantee):
        new_guarantee = Guarantee(guarantor_id=guarantee['guarantor_id'],
                                  warrantee_id=guarantee['warrantee_id'],
                                  status=0)
        session.add(new_guarantee)
        session.commit()

    def delete_guarantee(self, guarantee_id):
        guarantee = session.query(Guarantee).\
            filter(Guarantee.guarantee_id==guarantee_id).one()
        session.delete(guarantee)
        session.commit()

    def change_status(self, guarantee_id):
        guarantee = session.query(Guarantee). \
            filter(Guarantee.guarantee_id==guarantee_id).one()
        if guarantee.status == 0:
            guarantee.status = 1
        session.commit()


class LoanModel():
    def add_loan(self, loan):
        new_loan = Loan(user_id=loan['user_id'],
                        loan_amount=loan['loan_amount'],
                        remain_amount=loan['remain_amount'],
                        loan_date=loan['loan_date'],
                        due_date=loan['due_date'],
                        split_status=loan['split_status'],
                        due_status=loan['due_status'],
                        check_status=0)
        session.add(new_loan)
        session.commit()

    def delete_loan(self, loan_id):
        loan = session.query(Loan).filter(Loan.loan_id==loan_id).one()
        session.delete(loan)
        session.commit()

    def change_due_status(self, loan_id, status):
        loan = session.query(Loan).filter(Loan.loan_id==loan_id).one()
        loan.due_status = status
        session.commit()

    def change_split_status(self, loan_id, status):
        loan = session.query(Loan).filter(Loan.loan_id==loan_id).one()
        loan.split_status = status
        session.commit()

    def change_check_status(self, loan_id, status):
        loan = session.query(Loan).filter(Loan.loan_id==loan_id).one()
        loan.check_status = status
        session.commit()


class BehaviourModel():
    def add_behaviour(self, behaviour):
        pass
    
    def delete_behaviour(self, behaviour_id):
        pass
    
    def change_status(self, behaviour_id, status):
        pass

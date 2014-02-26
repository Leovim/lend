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
        pass
    
    def delete_guarantee(self, guarantee_id):
        pass
    
    def change_check(self, guarantee_id):
        pass


class LoanModel():
    def add_loan(self, loan):
        pass
    
    def delete_loan(self, loan_id):
        pass
    
    def change_due_status(self, loan_id, status):
        pass

    def change_split_status(self, loan_id, status):
        pass
    
    def change_check_status(self, loan_id, status):
        pass


class BehaviourModel():
    def add_behaviour(self, behaviour):
        pass
    
    def delete_behaviour(self, behaviour_id):
        pass
    
    def change_status(self, behaviour_id, status):
        pass

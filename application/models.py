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


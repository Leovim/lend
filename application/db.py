#coding=utf8

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import options

Base = declarative_base()
engine = create_engine(options.sqlalchemy)
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(20))
    password = Column(String(40))
    phone = Column(String(11))
    real_name = Column(String(5))
    bank_number = Column(String(20))
    alipay_number = Column(String(40))
    credit = Column(Integer)
    avatar = Column(String(50))

    def __init__(self, user_info):
        self.username = user_info['username']
        self.password = user_info['password']
        self.phone = user_info['phone']
        self.real_name = user_info['real_name']
        self.bank_number = user_info['bank_number']
        self.alipay_number = user_info['alipay_number']
        self.credit = int(user_info['credit'])
        self.avatar = user_info['avatar']

    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', )>" % \
               (self.user_id, self.username, self.password,
                self.phone, self.real_name, self.bank_number,
                self.alipay_number, self.credit, self.avatar)


class Guarantee(Base):
    __tablename__ = 'guarantee'

    guarantor_id = Column(Integer, ForeignKey('user.user_id'))
    warrantee_id = Column(Integer, ForeignKey('user.user_id'))
    status = Column(Integer)

    def __init__(self, guarantee):
        self.guarantor_id = int(guarantee['guarantor_id'])
        self.warrantee_id = int(guarantee['warrantee_id'])
        self.status = int(guarantee['status'])

    def __repr__(self):
        return  "<Guarantee('%s', '%s', '%s')>" % (self.guarantor_id,
                                                   self.warrantee_id,
                                                   self.status)


class Loan(Base):
    __tablename__ = 'loan'

    loan_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    loan_amount = Column(Integer)
    remain_amount = Column(Integer)
    loan_date = Column(String(20))
    due_date = Column(String(20))
    split_status = Column(Integer)
    due_status = Column(Integer)
    check_status = Column(Integer)

    def __init__(self, loan):
        self.user_id = int(loan['user_id'])
        self.loan_amount = int(loan['loan_amount'])
        self.remain_amount = int(loan['remain_amount'])
        self.loan_date = loan['loan_date']
        self.due_date = loan['due_date']
        self.split_status = int(loan['split_status'])
        self.due_status = int(loan['due_status'])
        self.check_status = int(loan['check_status'])

    def __repr__(self):
        return "<Loan('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" %\
               (self.loan_id, self.user_id, self.loan_amount,
                self.remain_amount, self.loan_date, self.due_date,
                self.split_status, self.due_status, self.check_status)


class Behaviour(Base):
    __tablename__ = 'behaviour'

    behaviour_id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loan.loan_id'))
    type = Column(Integer)
    money = Column(Integer)
    time = Column(String(20))
    check_status = Column(Integer)

    def __init__(self, behaviour):
        self.loan_id = int(behaviour['loan_id'])
        self.type = int(behaviour['type'])
        self.money = int(behaviour['money'])
        self.time = behaviour['time']
        self.check_status = int(behaviour['check_status'])

    def __repr__(self):
        return "<Behaviour('%s', '%s', '%s', '%s', '%s', '%s')>" % \
               (self.behaviour_id, self.loan_id, self.type, self.money,
                self.time, self.check_status)

#coding=utf8

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from config import options

Base = declarative_base()
engine = create_engine(options.sqlalchemy, encoding="utf-8", pool_recycle=3600)


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

    def __init__(self, username, password, phone, real_name=None,
                 bank_number=None, alipay_number=None, credit=1,
                 avatar=None):
        self.username = username
        self.password = password
        self.phone = phone
        self.real_name = real_name
        self.bank_number = bank_number
        self.alipay_number = alipay_number
        self.credit = int(credit)
        self.avatar = avatar

    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % \
               (self.user_id, self.username, self.password,
                self.phone, self.real_name, self.bank_number,
                self.alipay_number, self.credit, self.avatar)

    def as_dict(self):
        c = dict()
        for item in self.__table__.columns:
            c[item.name] = getattr(self, item.name)
        return c


class Guarantee(Base):
    __tablename__ = 'guarantee'

    guarantee_id = Column(Integer, primary_key=True)
    guarantor_id = Column(Integer, ForeignKey('user.user_id'))
    warrantee_id = Column(Integer, ForeignKey('user.user_id'))
    status = Column(Integer)

    def __init__(self, guarantor_id, warrantee_id, status):
        self.guarantor_id = int(guarantor_id)
        self.warrantee_id = int(warrantee_id)
        self.status = int(status)

    def __repr__(self):
        return  "<Guarantee('%s', '%s', '%s')>" % (self.guarantor_id,
                                                   self.warrantee_id,
                                                   self.status)

    def as_dict(self):
        c = dict()
        for item in self.__table__.columns:
            c[item.name] = getattr(self, item.name)
        return c


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

    def __init__(self, user_id, loan_amount, remain_amount, loan_date, due_date,
                 split_status, due_status, check_status):
        self.user_id = int(user_id)
        self.loan_amount = int(loan_amount)
        self.remain_amount = int(remain_amount)
        self.loan_date = loan_date
        self.due_date = due_date
        self.split_status = int(split_status)
        self.due_status = int(due_status)
        self.check_status = int(check_status)

    def __repr__(self):
        return "<Loan('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" %\
               (self.loan_id, self.user_id, self.loan_amount,
                self.remain_amount, self.loan_date, self.due_date,
                self.split_status, self.due_status, self.check_status)

    def as_dict(self):
        c = dict()
        for item in self.__table__.columns:
            c[item.name] = getattr(self, item.name)
        return c


class Behaviour(Base):
    __tablename__ = 'behaviour'

    behaviour_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('loan.user_id'))
    loan_id = Column(Integer, ForeignKey('loan.loan_id'))
    type = Column(Integer)
    money = Column(Integer)
    time = Column(String(20))
    check_status = Column(Integer)

    def __init__(self, user_id, loan_id, type, money, time, check_status):
        self.user_id = int(user_id)
        self.loan_id = int(loan_id)
        self.type = int(type)
        self.money = int(money)
        self.time = time
        self.check_status = int(check_status)

    def __repr__(self):
        return "<Behaviour('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % \
               (self.behaviour_id, self.user_id, self.loan_id, self.type, self.money,
                self.time, self.check_status)

    def as_dict(self):
        c = dict()
        for item in self.__table__.columns:
            c[item.name] = getattr(self, item.name)
        return c

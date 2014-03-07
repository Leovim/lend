#coding=utf8

from sqlalchemy.orm import sessionmaker
from db import *

Session = sessionmaker(bind=engine)
session = Session()

class BaseModel():
    def change_list(self, result_list):
        i = 0
        while i < result_list.__len__():
            result_list[i] = result_list[i].as_dict()
            i += 1
        return result_list


class UserModel(BaseModel):
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

    def update_user_credit(self, user_id, credit):
        user = session.query(User).filter(User.user_id==user_id).one()
        user.credit = int(credit)
        session.commit()

    def get_user_info(self, user_id):
        user = session.query(User).filter(User.user_id==user_id).one()
        return user.as_dict()

    def get_user_id(self, username):
        user = session.query(User).filter(User.username==username).one()
        return int(user.user_id)


class GuaranteeModel(BaseModel):
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

    def get_user_guarantor(self, user_id):
        guarantor = session.query(Guarantee).\
            filter(Guarantee.warrantee_id==int(user_id)).all()
        if guarantor.__len__() == 1:
            return guarantor[0].as_dict()
        else:
            return self.change_list(guarantor)

    def get_user_warrantee(self, user_id):
        warrantee = session.query(Guarantee). \
            filter(Guarantee.guarantor_id==int(user_id)).all()
        if warrantee.__len__() == 1:
            return warrantee[0].as_dict()
        else:
            return self.change_list(warrantee)


class LoanModel(BaseModel):
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

    def update_remain_amount(self, loan_id, remain_amount):
        loan = session.query(Loan).filter(Loan.loan_id==loan_id).one()
        loan.remain_amount = int(remain_amount)
        session.commit()

    def change_due_status(self, loan_id, status):
        loan = session.query(Loan).filter(Loan.loan_id==loan_id).one()
        loan.due_status = int(status)
        session.commit()

    def change_split_status(self, loan_id, status):
        loan = session.query(Loan).filter(Loan.loan_id==loan_id).one()
        loan.split_status = int(status)
        session.commit()

    def change_check_status(self, loan_id, status):
        loan = session.query(Loan).filter(Loan.loan_id==loan_id).one()
        loan.check_status = int(status)
        session.commit()

    def get_user_all_loans(self, user_id):
        loans = session.query(Loan).filter(Loan.user_id==user_id).all()
        if loans.__len__() == 1:
            return loans[0].as_dict()
        else:
            return self.change_list(loans)

    def get_user_new_three_loans(self, user_id):
        # order_by 默认升序 可使用order_by(Loan.loan_id.desc())显示降序结果
        # 可能不够3个，需要做处理
        loans = session.query(Loan).filter(Loan.user_id==user_id).\
            order_by(Loan.user_id.desc()).all()
        if loans.__len__() == 1:
            return loans[0].as_dict()
        elif loans.__len__() == 2:
            return self.change_list(loans)
        else:
            return self.change_list(loans[0:3])

    def get_all_unchecked_loans(self):
        loans = session.query(Loan).filter(Loan.check_status==0).all()
        if loans.__len__() == 1:
            return loans[0].as_dict()
        else:
            return self.change_list(loans)


class BehaviourModel(BaseModel):
    def add_behaviour(self, behaviour):
        new_behaviour = Behaviour(user_id=behaviour['user_id'],
                                  loan_id=behaviour['loan_id'],
                                  type=behaviour['type'],
                                  money=behaviour['money'],
                                  time=behaviour['time'],
                                  check_status=behaviour['check_status'])
        session.add(new_behaviour)
        session.commit()

    def delete_behaviour(self, behaviour_id):
        behaviour = session.query(Behaviour).\
            filter(Behaviour.behaviour_id==behaviour_id).one()
        session.delete(behaviour)
        session.commit()

    def change_status(self, behaviour_id, status):
        behaviour = session.query(Behaviour). \
            filter(Behaviour.behaviour_id==behaviour_id).one()
        behaviour.check_status = int(status)
        session.commit()
        
    def get_user_all_behaviours(self, user_id):
        pass
    
    def get_user_new_ten_behaviours(self, user_id):
        pass
    
    def get_all_unchecked_behaviours(self):
        pass

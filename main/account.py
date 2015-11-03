from main.models import Trans
from main.models import Accounts
from main.models import Currency
from main.models import TransError
from django.contrib.auth.models import User

class Account(object):
    def __init__(self, *args, **kwards):
        user = data.get('user', None)
        currency = data.get('currency', None)
        user_id=data.get('user_id', None)
        id = data.get('id', None)

        if isinstance(user, User):
            user_id = user.id

        if isinstance(user, int):
            user_id = user

        currency_id = data.get('currency_id', None)
        if isinstance(currency, Currency):
            currency_id = currency.id

        if isinstance(currency, int):
            currency_id = currency


        self.__account = Accounts.objects.get(user_id = user_id, currency_id=currency_id)
        self.__currency_id = currency_id
        self.__user_id = user_id
        self.__trans = Trans.objects.get(id=self.account.last_trans_id)
        if self.__account.id == self.__trans.user2_id:
           self.__balance =  self.__trans.res_balance2
        else:
           self.__balance =  self.__trans.res_balance1

        self.__inconsist = False

    def currency(self):
        return self.__currency_id

    def acc(self):
        return self.__account

    def get_user(self):
        return self.__user_id

    def reload(self):
        self.__account = Accounts.objects.get(user_id = self.__user_id, currency_id=self.__currency_id)
        self.__trans = Trans.objects.get(id=self.__account.last_trans_id)


        if self.__account.id == self.__trans.user2_id:
           self.__balance =  self.__trans.res_balance2
        else:
           self.__balance =  self.__trans.res_balance1
        self.__inconsist = False

    def get_balance(self):
        if  self.__inconsist :
            raise TransError("it seems a race condition, reload object")
        return self.__balance

    def plus(self, amnt):
        self.__balance += amnt
        return  self.__balance

    def mines(self, amnt):
        self.__balance -= amnt
        return  self.__balance

    def save(self, trans):
        if  self.__inconsist:
            raise TransError("it seems a race condition, reload object")

        try:
            acc = Accounts.objects.get(id=self.__account.id, last_trans_id=self.__trans.id).update(
                last_trans_id = trans.id,
                balance = self.__balance)

            self.__account = acc
            self.__trans = trans
        except Accounts.DoesNotExist:
            raise TransError("it seems a race condition")
            self.__inconsist = True

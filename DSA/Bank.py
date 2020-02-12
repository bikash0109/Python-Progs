import random
from abc import *


class Account:
    def __init__(self, account_holder):
        self.holder = account_holder
        self.balance = 0
        self.__accountid = random.randint(100, 999)
        self.loantaken = 0
        self.loanamt = 0
        self.Credit = 0

    def deposit(self, amount):

        self.balance = self.balance + amount

        return self.balance

    def withdraw(self, amount):

        if amount > self.balance:
            return 'Not enough funds'

        self.balance = self.balance - amount

        return 'Your new balance is ${}'.format(self.balance)

    @property
    def Accountnumber(self):

        return self.__accountid

    def loan(self, amount):

        if amount >= 100:

            self.loanamt += amount

            self.loantaken += 1

            return self.loanamt

        else:

            return 'Please enter valid amount'

    def cc(self, limit=1000):

        if self.Credit == 0:

            self.Credit += 1

            return "Congratulations you have successfully applied for a credit card"

        else:

            return "You already have a credit card issued."


class CheckingAccount(Account):
    withdraw_fee = 1

    def __init__(self, name):

        super().__init__(name)

    def withdraw(self, amount):

        if amount <= (self.balance + self.withdraw_fee):

            return Account.withdraw(self, amount + self.withdraw_fee)

        else:

            return "Invalid"


class Bank(ABC):
    def __init__(self):
        self.Account = []

    def openAccount(self, name, amount, account_type=Account):
        if type(name) is str and type(amount) is int or float:
            customer = account_type(name)
            customer.deposit(amount)
            self.Account.append(customer)
            return ("Your account was created successfully with Accountnumber {} and balance ${}".format(
                customer.Accountnumber, customer.balance))
        else:
            return "Sorry your account was not created."

    def deposit(self, accountnumber, amount):
        for customer in self.Account:
            if accountnumber == customer.Accountnumber and amount >= 0:
                customer.deposit(amount)
                return "Your new balance is ${}".format(customer.balance)
            elif accountnumber != customer.Accountnumber:
                return "Your Account was not detected"
            else:
                return "Invalid entry"

    def withdraw(self, accountnumber, amount):
        for customer in self.Account:
            if accountnumber == customer.Accountnumber and amount >= 0:
                return customer.withdraw(amount)
            elif accountnumber != customer.Accountnumber:
                return "Your Account was not detected"

    def balance(self, accountnumber):
        for customer in self.Account:
            if accountnumber == customer.Accountnumber:
                return customer.balance
            else:
                return "Account not found"


class Customer(Bank):

    def __init__(self, name):

        self.customer_name = name

        super().__init__()

    def loan(self, accountnumber, amount):

        for customer in self.Account:

            if accountnumber == customer.Accountnumber:

                if customer.loantaken == 0:

                    customer.loan(amount)

                    return "You have successfully applied for loan of ${}".format(customer.loanamt)

                else:

                    return "You already have a loan "

            elif accountnumber != customer.Accountnumber:

                return "Your Account was not detected"

            else:

                return "Unable to process loan"

    def monthly_payment(self, accountnumber, amount):

        for customer in self.Account:

            if accountnumber == customer.Accountnumber:

                return customer.withdraw(amount)

            else:

                return "Your account was not detected"

    def deposit_check(self, accountnumber, amount):

        for customer in self.Account:

            if accountnumber == customer.Accountnumber:

                return "Available balance: ${}. Your check was successfully deposited".format(customer.deposit(amount))

            else:

                return "Your account was not detected"

    @property
    def creditcard(self):

        for customer in self.Account:

            if self.customer_name == customer.holder:

                return customer.cc()

            elif self.customer_name not in customer.holder:

                return "Account was not detected"

            else:

                return


class manager(Bank):
    def __init__(self):
        super(manager, self).__init__()

    def getParentAccount(self):
        print(self.Account)

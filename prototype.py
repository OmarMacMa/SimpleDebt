import datetime
import pandas as pd
from typing import List


class User:

    def __init__(self, name: str, balance: float = 0.0):
        self.name: str = name
        self.total_contribution: float = 0.0
        self.total_debt: float = 0.0
        self.balance: float = balance

    def calculate_balance(self):
        self.balance = self.total_contribution - self.total_debt
        self.balance = round(self.balance, 2)
        self.total_contribution = round(self.total_contribution, 2)
        self.total_debt = round(self.total_debt, 2)
        return self.balance

    def __str__(self):
        return self.name


class Payment:

    def __init__(self, user_paying: User, users_receiving: List[User], amount: float, description: str, date: datetime, category: str):
        self.user_paying: User = user_paying
        self.users_receiving: List[User] = users_receiving
        self.amount: float = amount
        self.description: str = description
        self.date: datetime = date
        self.category: str = category
        self.amount_per_user: float = amount / (len(users_receiving) + 1)

    def calculate_total_contribution(self):
        self.user_paying.total_contribution += self.amount
        for receiving in self.users_receiving:
            receiving.total_debt += self.amount_per_user
        self.user_paying.total_debt += self.amount_per_user


class Group:

    def __init__(self, name: str):
        self.name: str = name
        self.users: List[User] = []
        self.payments: List[Payment] = []

    def add_user(self, name: str):
        for user in self.users:
            if user.name == name:
                return user
        self.users.append(User(name))
        return self.users[-1]

    def add_payment(self, user_paying: str, users_receiving: List[str], amount: float, description: str, date: datetime, category: str):
        user_paying_obj = self.add_user(user_paying)
        users_receiving_obj = [self.add_user(user) for user in users_receiving]
        payment = Payment(user_paying_obj, users_receiving_obj, amount, description, date, category)
        self.payments.append(payment)

    def calculate_amount_per_user(self):
        for payment in self.payments:
            payment.calculate_total_contribution()
    
    def calculate_balance(self):
        for user in self.users:
            user.calculate_balance()

    """Corrections needed
    def calculate_minimum_transactions(self):
        debtors = []
        creditors = []
        for user in self.users:
            if user.balance > 0:
                creditors.append(User(user.name, user.balance))
            elif user.balance < 0:
                debtors.append(User(user.name, user.balance))
        creditors.sort(key=lambda x: x.balance, reverse=True)
        debtors.sort(key=lambda x: x.balance)
        transactions = []
        for debtor in debtors:
            for creditor in creditors:
                if debtor.balance < 0.2 and debtor.balance > -0.2:
                    break
                if creditor.balance < 0.2 and creditor.balance > -0.2:
                    continue
                if debtor.balance < creditor.balance:
                    transactions.append(f"{debtor.name} pays {creditor.name} ${-1*debtor.balance}")
                    creditor.balance += debtor.balance
                    debtor.balance = 0
                else:
                    transactions.append(f"{debtor.name} pays {creditor.name} ${-1*creditor.balance}")
                    debtor.balance += creditor.balance
                    creditor.balance = 0
        for transaction in transactions:
            print(transaction)"""

    def display_results(self):
        print(f"Group: {self.name}")
        print(f"| User \t| Contribution | Debt | Balance |")
        for user in self.users:
            print(f"| {user.name} | {user.total_contribution} | {user.total_debt} | {user.balance} |")


def main():
    group = Group("HEMT")
    records = pd.read_csv("records.csv")
    for index, record in records.iterrows():
        amount = float(record["Amount"])
        date = datetime.datetime.strptime(record["Date"], "%Y-%m-%d")
        receiving = []
        for user in record["UsersReceiving"].split(";"):
            receiving.append(user)
        group.add_payment(record["UserPaying"], receiving, amount, record["Description"], date, record["Category"])
    group.calculate_amount_per_user()
    group.calculate_balance()
    group.display_results()


if __name__ == "__main__":
    main()
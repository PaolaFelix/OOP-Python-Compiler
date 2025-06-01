class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance

# Usage
account = BankAccount(100)
account.deposit(50)
print(account.get_balance())

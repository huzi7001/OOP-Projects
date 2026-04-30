#creat account class with two attributes , balance and account no.
#creat method for debit, credit and printing the balance

# def def__init__(balance, account_num):
#     raise NotImplementedError

class Account:
    def __init__(self, balance, account_num):
        self.bal = balance 
        self.acc = account_num


    def debit(self, amount):
        if amount > self.bal:
            return "Insufficient balance"
        self.bal -= amount
        return f"Debited {amount}. New balance is {self.bal}"

    def credit(self, amount):
        self.bal += amount
        return f"Credited {amount}. New balance is {self.bal}" 

    def get_balance(self):
        return f"Account Number: {self.acc}, Balance: {self.bal}"
    
# Example usage:
account = Account(10000, "0123456789")
print(account.credit(500))

acc =Account(11500, "0123456789")
print(acc.debit(1500))

acc_1 = Account(135, "0123456789")
print(acc_1.get_balance())
print(acc_1.credit(200))
print(acc_1.debit(500))







#creat account class with two attributes , balance and account no.
#creat method for debit, credit and printing the balance


class Account:
    def __init__(self, balance, acc_num):
        self.balance = bal
        self.acc_num = acc_num  

    def debit(self, amount):
        if amount>self.balance:
            return "Insufficient balance"
     
        self.balance-=amount
        return f"debited amount : {amount} New balance is : {self.balance}"
    
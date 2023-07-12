import math
from itertools import zip_longest


class Category:
    def __init__(self, name) -> None:
        self.name = name
        self.ledger = []
        self.balance = 0
        self.withdraw_count = 0

    def deposit(self, amount, description=""):
        self.balance += amount
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount):
            return False
        self.balance -= amount
        self.withdraw_count += amount
        self.ledger.append({"amount": -amount, "description": description})
        return True

    def get_balance(self):
        return self.balance

    def transfer(self, amount, another_category):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f"Transfer to {another_category.name}")
        another_category.deposit(amount, f"Transfer from {self.name}")
        return True

    def check_funds(self, amount):
        return amount <= self.balance

    def __str__(self) -> str:
        line = "*" * 13 + "Food" + "*" * 13 + "\n"
        for item in self.ledger:
            item_name = item["description"][:23]
            item_amount = item["amount"]
            item_amount = f"{item_amount:.2f}"
            line += f"{item_name}" + " " * (23 - len(item_name))
            line += " " * (7 - len(item_amount[:7])) + item_amount[:7] + "\n"
        line += f"Total: {self.balance:.2f}"
        return line


def create_spend_chart(categories):
    answer = "Percentage spent by category\n"
    all_budget = sum(i.withdraw_count for i in categories)
    percentage = []
    for category in categories:
        percentage.append(math.floor((category.withdraw_count / all_budget) * 100))
    for i in range(100, -10, -10):
        tmp = " "
        for per in percentage:
            if per >= i:
                tmp += "o  "
            else:
                tmp += "   "
        answer += " " * (3 - len(str(i))) + f"{i}|" + tmp + "\n"
    answer += "    -" + "---" * len(categories) + "\n"
    for category in zip_longest(*[i.name for i in categories], fillvalue=" "):
        tmp = "     "
        for letter in category:
            tmp += letter + "  "
        answer += tmp + "\n"
        print(category)
    return answer


# food = Category("food")
# entertainment = Category("entertainment")
# food.deposit(900, "deposit")
# food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
# food.transfer(20, entertainment)
# print(food)
food = Category("Food")
business = Category("Business")
entertainment = Category("Entertainment")
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
expected = "Percentage spent by category\n100|          \n 90|          \n 80|          \n 70|    o     \n 60|    o     \n 50|    o     \n 40|    o     \n 30|    o     \n 20|    o  o  \n 10|    o  o  \n  0| o  o  o  \n    ----------\n     B  F  E  \n     u  o  n  \n     s  o  t  \n     i  d  e  \n     n     r  \n     e     t  \n     s     a  \n     s     i  \n           n  \n           m  \n           e  \n           n  \n           t  "
print(expected)
actual = create_spend_chart([business, food, entertainment])
print(actual)

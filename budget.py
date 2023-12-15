class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, budget_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {budget_category.category}")
            budget_category.deposit(amount, f"Transfer from {self.category}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.category:*^30}\n"
        items = "".join(
            f"{item['description'][:23]:23}{item['amount']:7.2f}\n"
            for item in self.ledger
        )
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    chart = "Percentage spent by category\n"
    spent_percentages = [
        sum(item["amount"] for item in category.ledger if item["amount"] < 0)
        / category.get_balance()
        * 100
        if category.get_balance() != 0
        else 0
        for category in categories
    ]

    for i in range(100, -1, -10):
        chart += f"{i:3}|"
        for percentage in spent_percentages:
            chart += " o " if percentage >= i else "   "
        chart += "\n"

    chart += "    ----------\n"

    # Find the longest category name
    max_length = max(len(category.category) for category in categories)

    for i in range(max_length):
        chart += "     "
        for category in categories:
            chart += f"{category.category[i] if i < len(category.category) else ' ':2}  "
        chart += "\n"

    return chart.strip()


if __name__ == '__main__':
    food = Category("Food")
    food.deposit(1000, "initial deposit")
    food.withdraw(10.15, "groceries")
    food.withdraw(15.89, "restaurant and more food for dessert")
    print(food.get_balance())
    clothing = Category("Clothing")
    food.transfer(50, clothing)
    clothing.withdraw(25.55)
    clothing.withdraw(100)
    auto = Category("Auto")
    auto.deposit(1000, "initial deposit")
    auto.withdraw(15)

    print(food)
    print(clothing)

    print(create_spend_chart([food, clothing, auto]))

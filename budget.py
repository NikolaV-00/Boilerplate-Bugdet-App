class Category:

    def __init__(self, cat):
        self.cat = cat
        self.ledger = list()

    def __str__(self):
        # title line will be 30 chars long with name of
        # the category in the centre surrounded by *
        title = f"{self.cat:*^30}\n"
        lines = ""
        total = 0
        for line in self.ledger:
            # first 23 chars of the lines will be from description
            # while the last 7 will be from amount, rounded to 2 decimals
            lines += f"{line['description'][0:23]:23}" + f"{line['amount']:>7.2f}" + '\n'

            total += line['amount']

        output = title + lines + "Total: " + str(total)
        return output

    def get_balance(self):
        balance = 0
        # returns a balance with every change
        for money in self.ledger:
            balance += money['amount']
        return balance

    def check_funds(self, amount):
        # checks if the given amount is smaller than the balance
        if self.get_balance() >= amount:
            return True
        else:
            return False

    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=''):
        # checks if the balance is higher than the requested amount
        # if it is preform the withdrawal
        if self.check_funds(amount):
            self.ledger.append({"amount": -1 * amount, "description": description})
            return True
        else:
            return False

    def transfer(self, amount, category):
        # similar to withdraw function, except here
        # the funds are transferred from one category to another
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + category.cat)
            category.deposit(amount, "Transfer from " + self.cat)
            return True
        return False


def create_spend_chart(categories):
    # in case no category is in created
    items = len(categories)
    if items == 0:
        return 'No categories provided'

    chart = 'Percentage spent by category\n'
    data = list()
    lines = 0
    total = 0.00

    for ctgr in categories:
        # takes the longest cat name to set number of lines
        if lines < len(ctgr.cat):
            lines = len(ctgr.cat)

        spent = 0.00
        # if there have been some withdraws,
        # calculate the absolute sum of those
        for money in ctgr.ledger:
            if money['amount'] < 0:
                spent += money['amount']
        total += spent
        data.append([ctgr.cat, abs(spent)])

    total = abs(total)

    # calculate the percentage for each category
    for d in data:
        percent = d[1] / total * 100
        d[1] = percent

    # forms 0| to 100| in increments of 10
    for x in reversed(range(11)):
        x = x * 10
        num = str(x)
        line = str()
        if num == '0':
            line += ' '
        if num != '100':
            line += ' '
        line += num + '|'
        # forms the percentage part of the chart
        for d in data:
            if x < d[1]:
                line += ' o '
            else:
                line += '   '

        chart += line + ' \n'
    # forms the lines between percentage and category names
    chart += '    -'
    for n in range(items):
        chart += '---'
    # forms vertical category names
    for n in range(lines):
        chart += '\n    '
        for d in data:
            try:
                chart += ' ' + d[0][n] + ' '
            except:
                chart += '   '
        chart += ' '

    return chart
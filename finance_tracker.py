import json
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np

class FinanceTracker:
    ############################ SETUP ############################
    def __init__(self, filename):
        self.filename = filename
        self.load_data()
        self.auto_reset()

    def print_last_login(self):
        print(f'Last login: {self.data["params"]["last_login"]}')

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.data = data

                self.catagory_map = {}
            for i, catagory in enumerate(self.data['catagories']):
                self.catagory_map[i + 1] = catagory

            self.loan_map = {}
            for i, loan in enumerate(self.data['loans']):
                self.loan_map[i + 1] = loan

            self.account_map = {}
            for i, account in enumerate(self.data['accounts']):
                self.account_map[i + 1] = account

        except FileNotFoundError:
            data = {}
        return data

    def save_data(self):
        self.data['params']['last_login'] = datetime.today().strftime('%Y-%m-%d')
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)
        backup_file = self.filename.split('.')[0] + '_backup.json'
        with open("../" + backup_file, 'w') as file:
            json.dump(self.data, file)

    ############################ MOVE MONEY ############################
    def add_transaction(self, amount, catagory, description):
        self.data['accounts']['checking'] -= amount
        self.data['transactions'].append({'date': datetime.today().strftime('%Y-%m-%d'), 'amount': amount, 'catagory': self.catagory_map[int(catagory)], 'description': description})
        self.data['catagories'][self.catagory_map[int(catagory)]]['count'] += 1
        self.data['catagories'][self.catagory_map[int(catagory)]]['amount'] += amount
        self.list_last_n_transactions(1)
        self.save_data()
        self.data = self.load_data()

    def add_income(self, amount, description):
        self.data['accounts']['checking'] += amount * self.data['params']['checking_rate']
        self.data['accounts']['savings'] += amount * self.data['params']['savings_rate']
        self.data['income'].append({'date': datetime.today().strftime('%Y-%m-%d'), 'amount': amount, 'description': description})
        self.list_last_n_transactions(1)
        self.save_data()
        self.data = self.load_data()

    def transfer_between_accounts(self, amount, from_account, to_account):
        self.data['accounts'][self.account_map[int(from_account)]] -= amount
        self.data['accounts'][self.account_map[int(to_account)]] += amount
        self.save_data()
        self.data = self.load_data()

    def pay_loan(self, amount, loan):
        self.data['accounts']['savings'] -= amount
        self.data['loans'][self.loan_map[int(loan)]] -= amount
        self.data['loan_payments'].append({'date': datetime.today().strftime('%Y-%m-%d'), 'amount': amount, 'loan': self.loan_map[int(loan)]})
        self.list_last_n_transactions(1)
        self.save_data()
        self.data = self.load_data()

    ############################ VIEW DATA ############################
    
    def print_loans(self):
        i = 1
        for loan, amount in self.data['loans'].items():
            print(f'{i}. {self.pretty_names(loan)}: {round(amount, 2)}')
            i += 1

    def list_last_n_transactions(self, n):
        for transaction in self.data["transactions"][-n:]:
            print(f"{transaction['date']}: ${transaction['amount']} --> {transaction['description']}")

    def get_balance(self):
        print('====================================')
        print('Accounts:')
        self.print_accounts()
        account_total = 0
        for account in self.data['accounts'].values():
            account_total += account
        print(f'Account total: {round(account_total, 2)}')
        print('====================================')
        print('Loans:')
        self.print_loans()
        loan_total = 0
        for loan in self.data['loans'].values():
            loan_total += loan
        print(f'Loan total: {round(loan_total, 2)}')
        print('====================================')
        print('Catagories:')
        self.print_catagories()
        catagory_total = 0
        for catagory in self.data['catagories'].values():
            catagory_total += catagory['amount']
        print(f'Total spent since {self.data["params"]["last_reset"]}: {catagory_total}')
    
    def print_catagories(self):
        i = 1
        for catagory_name, catagory in self.data['catagories'].items():
            print(f'{i}. {self.pretty_names(catagory_name)} --> count: {catagory["count"]}, amount: {catagory["amount"]}')
            i += 1

    def print_by_catagory(self, catagory):
        total = 0
        for transaction in self.data['transactions']:
            if transaction['catagory'] == self.catagory_map[int(catagory)]:
                print(f"{transaction['date']}: ${transaction['amount']} --> {transaction['description']}")
                total += transaction['amount']
        print(f'Total: {round(total, 2)}')
    
    def print_by_month(self, month):
        total = 0
        print(f'Month: {month}')
        for transaction in self.data['transactions']:
            if transaction['date'].split('-')[1] == month:
                print(f"{transaction['date']}: ${transaction['amount']} --> {transaction['description']}")
                total += transaction['amount']
        print(f'Total: {round(total, 2)}')

    def print_accounts(self):
        i = 1
        for account, amount in self.data['accounts'].items():
            print(f'{i}. {self.pretty_names(account)}: {round(amount, 2)}')
            i += 1
    
    def print_last_reset(self):
        print(f'Last reset: {self.data["params"]["last_reset"]}')

    ############################ ADD DATA ############################

    def add_catagory(self, catagory):
        self.data['catagories'][catagory] = {'count': 0, 'amount': 0, 'percent': 0}
        self.save_data()
        self.data = self.load_data()

    def add_loan(self, loan, amount):
        self.data['loans'][loan] = amount
        self.save_data()
        self.data = self.load_data()
    
    def add_account(self, account, amount):
        self.data['accounts'][account] = amount
        self.save_data()
        self.data = self.load_data()

    ############################ RESET DATA ############################
    def auto_reset(self): # Automatically reset catagories on the first login of the month
        last_login = datetime.strptime(self.data['params']['last_login'], '%Y-%m-%d')

        if datetime.today().strftime('%Y-%m-%d').split('-')[2] == '01' or last_login.month != datetime.today().month:
            print('Monthly auto reset in progress')
            print('====================================')
            print('Last Month Spending:')
            self.print_catagories()
            print('====================================')
            self.reset_catagories()

        print('Auto reset complete')

    def reset(self):
        self.data['params']['last_reset'] = datetime.today().strftime('%Y-%m-%d')
        self.reset_catagories()
        self.reset_loans_payments()
        self.reset_income()
        self.reset_transactions()
    
    def reset_catagories(self):
        self.data['params']['last_reset'] = datetime.today().strftime('%Y-%m-%d')
        for catagory in self.data['catagories']:
            self.data['catagories'][catagory]['count'] = 0
            self.data['catagories'][catagory]['amount'] = 0
        self.save_data()
        self.data = self.load_data()

    def reset_loans_payments(self):
        self.data['loan_payments'] = []
        self.save_data()
        self.data = self.load_data()

    def reset_income(self):
        self.data['income'] = []
        self.save_data()
        self.data = self.load_data()

    def reset_transactions(self):
        self.data['transactions'] = []
        self.save_data()
        self.data = self.load_data()

    ############################ GRAPHING ############################

    def display_income_graph(self): # Display a line chart of income over time, built backwards from the current date
        incomes = self.data['income']
        first_date = datetime.strptime(incomes[0]['date'], '%Y-%m-%d')
        dates = []
        pay_period_sum = 0
        pay_period_sum_list = []
        checking_rate = self.data['params']['checking_rate']
        savings_rate = self.data['params']['savings_rate']
        pay_period_checking = 0
        pay_period_savings = 0
        pay_period_checking_list = []
        pay_period_savings_list = []
        for income in incomes:
            if (datetime.strptime(income['date'], '%Y-%m-%d') - first_date).days > 12:
                pay_period_sum_list.append(pay_period_sum)
                dates.append(first_date.strftime('%Y-%m-%d'))
                pay_period_checking_list.append(pay_period_checking)
                pay_period_savings_list.append(pay_period_savings)

                pay_period_sum = 0
                first_date = datetime.strptime(income['date'], '%Y-%m-%d')
                pay_period_checking = 0
                pay_period_savings = 0
            
            pay_period_sum += income['amount']
            pay_period_checking += income['amount'] * checking_rate
            pay_period_savings += income['amount'] * savings_rate

        pay_period_sum_list.append(pay_period_sum)
        dates.append(first_date.strftime('%Y-%m-%d'))
        pay_period_checking_list.append(pay_period_checking)
        pay_period_savings_list.append(pay_period_savings)

        fig = plt.figure(figsize=(10, 7))
        plt.xlabel('Date')
        plt.ylabel('Income')
        plt.title('Income Over Time')
        plt.ylim(0, max(pay_period_sum_list) + 100)
        plt.plot(dates, pay_period_sum_list, label='Total Income')
        plt.plot(dates, pay_period_checking_list, label='Checking Income')
        plt.plot(dates, pay_period_savings_list, label='Savings Income')
        plt.legend()
        plt.show()

    def display_catagory_graph(self): # Display a pie chart of catagory spending
        categories = self.data['catagories']
        names = []
        amounts = []
        for category in categories:
            if categories[category]['amount'] == 0:
                continue
            names.append(self.pretty_names(category))
            amounts.append(categories[category]['amount'])
        
        if len(names) == 0:
            print('No catagory spending')
            return

        fig = plt.figure(figsize=(10, 7))
        plt.title('Catagory Spending')
        plt.pie(amounts, labels=names, autopct=lambda pct: self.func(pct, amounts))

        plt.show()

    def display_account_graph(self): # Display a pie chart of account balances
        accounts = self.data['accounts']
        names = []
        amounts = []
        for account in accounts:
            names.append(self.pretty_names(account))
            amounts.append(accounts[account])

        if len(names) == 0:
            print('No accounts')
            return

        fig = plt.figure(figsize=(10, 7))
        plt.title('Account Balances')
        plt.pie(amounts, labels=names, autopct=lambda pct: self.func(pct, amounts))

        plt.show()

    def display_loan_graph(self): # Display a pie chart of loan payments
        loans = self.data['loans']
        names = []
        amounts = []
        for loan in loans:
            names.append(self.pretty_names(loan))
            amounts.append(loans[loan])

        if len(names) == 0:
            print('No loans')
            return

        fig = plt.figure(figsize=(10, 7))
        plt.title('Loan Amounts')
        plt.pie(amounts, labels=names, autopct=lambda pct: self.func(pct, amounts))

        plt.show()
    
    def func(self, pct, allvalues): # Helper function for the graphing functions
        absolute = float(pct / 100.*np.sum(allvalues))
        return "{:.2f}%\n(${:.2f})".format(pct, absolute)
    
    def pretty_names(self, name):
        return name.replace('_', ' ').title()
    
    ############################ BUDGETING ############################

    def set_budgeting_goals(self): # Set budgeting goals for each catagory
        catagory_goals = {}
        for catagory in self.data['catagories']:
            catagory_goals[catagory] = float(input(f'Enter budgeting goal for {self.pretty_names(catagory)}: '))
        self.data['catagory_goals'] = catagory_goals
        self.save_data()
        self.data = self.load_data()

    def print_budgeting_goals(self): # Print budgeting goals for each catagory
        for catagory, goal in self.data['catagory_goals'].items():
            print(f'{self.pretty_names(catagory)}: {goal}')
            print(f'Amount spent: {self.data["catagories"][catagory]["amount"]}')

    def reset_budgeting_goals(self): # Reset budgeting goals for each catagory
        self.data['catagory_goals'] = {}
        self.save_data()
        self.data = self.load_data()
        

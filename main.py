import sys
from finance_tracker import FinanceTracker

def move_money():
    while True:
        print('====================================')
        print('Move Money')
        print('1. Add transaction')
        print('2. Add income')
        print('3. Pay loan')
        print('4. Transfer between accounts')
        print('B. Back')
        print('Q. Quit')
        print('====================================')
        choice = input('Enter choice: ')
        print('====================================')

        if choice == '1': # Add transaction
            print('====================================')
            try:
                amount = float(input('Enter amount: '))
                print('Catagories: ')
                tracker.print_catagories()
                catagory = input('Enter catagory: ')
                description = input('Enter description: ')
                tracker.add_transaction(amount, catagory, description)
            except ValueError:
                print('====================================')
                print('Invalid inputs')
            except KeyError:
                print('====================================')
                print('Invalid catagory')
        elif choice == '2': # Add income
            print('====================================')
            try:
                amount = float(input('Enter amount: '))
                description = input('Enter description: ')
                tracker.add_income(amount, description)
                input('Would you like to reset your category info? (Y/N): ')
                if input == 'Y' or input == 'y':
                    tracker.reset_catagories()
            except ValueError:
                print('====================================')
                print('Invalid inputs')
            except KeyError:
                print('====================================')
                print('Invalid catagory')
        elif choice == '3': # Pay loan
            print('====================================')
            try:
                amount = float(input('Enter amount: '))
                print('Loans: ')
                tracker.print_loans()
                loan = input('Enter loan: ')
                tracker.pay_loan(amount, loan)
            except ValueError:
                print('====================================')
                print('Invalid inputs')
            except KeyError:
                print('====================================')
                print('Invalid loan')
        elif choice == '4': # Transfer between accounts
            print('====================================')
            try:
                amount = float(input('Enter amount: '))
                print('Accounts: ')
                tracker.print_accounts()
                from_account = input('Enter from account: ')
                to_account = input('Enter to account: ')
                tracker.transfer_between_accounts(amount, from_account, to_account)
            except ValueError:
                print('====================================')
                print('Invalid inputs')
            except KeyError:
                print('====================================')
                print('Invalid account')
        elif choice == 'B' or choice == 'b': # Back
            choose_purpose()
        elif choice == 'Q' or choice == 'q': # Quit
            quit()
        else:
            print('Invalid choice')

def view_data():
    while True:
        print('====================================')
        print('View Data')
        print('1. List account and loan balances')
        print('2. List last n transactions')
        print('3. List transactions by catagory')
        print('4. List transactions by month')
        print('5. List catagories')
        print('6. List last reset')
        print('B. Back')
        print('Q. Quit')
        print('====================================')
        choice = input('Enter choice: ')
        print('====================================')

        if choice == '1': # List account and loan balances
            tracker.get_balance()
            input('Press enter to continue')
        elif choice == '2': # List last n transactions
            try:
                n = int(input('Enter n: '))
                tracker.list_last_n_transactions(n)
                input('Press enter to continue')
            except ValueError:
                print('====================================')
                print('Invalid n')
        elif choice == '3': # List transactions by catagory
            try:
                print('Catagories: ')
                tracker.print_catagories()
                catagory = input('Enter catagory: ')
                tracker.print_by_catagory(catagory)
                input('Press enter to continue')
            except ValueError:
                print('====================================')
                print('Invalid catagory')
            except KeyError:
                print('====================================')
                print('Invalid catagory')
        elif choice == '4': # List transactions by month
            try:
                month = input('Enter month (mm): ')
                tracker.print_by_month(month)
                input('Press enter to continue')
            except ValueError:
                print('====================================')
                print('Invalid month')
            except KeyError:
                print('====================================')
                print('Invalid month')
        elif choice == '5': # List catagories
            tracker.print_catagories()
            input('Press enter to continue')
        elif choice == '6': # List last reset
            tracker.print_last_reset()
            input('Press enter to continue')
        elif choice == 'B' or choice == 'b': # Back
            choose_purpose()
        elif choice == 'Q' or choice == 'q': # Quit
            quit()
        else:
            print('Invalid choice')


def add_data():
    while True:
        print('====================================')
        print('Add Data')
        print('1. Add catagory')
        print('2. Add loan')
        print('3. Add account')
        print('B. Back')
        print('Q. Quit')
        print('====================================')
        choice = input('Enter choice: ')
        print('====================================')

        if choice == '1': # Add catagory
            try:
                catagory = input('Enter catagory: ')
                tracker.add_catagory(catagory)
            except ValueError:
                print('====================================')
                print('Invalid inputs')
            except KeyError:
                print('====================================')
                print('Invalid catagory')
        elif choice == '2': # Add loan
            try:
                loan = input('Enter loan: ')
                amount = float(input('Enter amount: '))
                tracker.add_loan(loan, amount)
            except ValueError:
                print('====================================')
                print('Invalid inputs')
            except KeyError:
                print('====================================')
                print('Invalid loan')
        elif choice == '3': # Add account
            try:
                account = input('Enter account: ')
                amount = float(input('Enter amount: '))
                tracker.add_account(account, amount)
            except ValueError:
                print('====================================')
                print('Invalid inputs')
            except KeyError:
                print('====================================')
                print('Invalid account')
        elif choice == 'B' or choice == 'b': # Back
            choose_purpose()
        elif choice == 'Q' or choice == 'q': # Quit
            quit()
        else:
            print('Invalid choice')

def reset_data():
    while True:
        print('====================================')
        print('Reset Data')
        tracker.print_last_reset()
        print('1. Reset catagories')
        print('2. Reset loans payments')
        print('3. Reset income')
        print('4. Reset transactions')
        print('5. Reset all data')
        print('B. Back')
        print('Q. Quit')
        print('====================================')
        choice = input('Enter choice: ')
        print('====================================')

        if choice == '1': # Reset catagories
            tracker.reset_catagories()
        elif choice == '2': # Reset loans payments
            tracker.reset_loans_payments()
        elif choice == '3': # Reset income
            tracker.reset_income()
        elif choice == '4': # Reset transactions
            tracker.reset_transactions()
        elif choice == '5': # Reset all data
            print('Are you sure you want to reset transactions, catagories, income, and loan payments?')
            confirm = input('Enter Y to confirm: ')
            if confirm == 'Y' or confirm == 'y':
                tracker.reset()
            else:
                print('Reset cancelled')
                continue
        elif choice == 'B' or choice == 'b': # Back
            choose_purpose()
        elif choice == 'Q' or choice == 'q': # Quit
            quit()
        else:
            print('Invalid choice')

def display_data():
    print('====================================')
    while True:
        print('Display Data')
        print('1. Display account graph')
        print('2. Display catagory graph')
        print('3. Display loan graph')
        print('4. Display income graph')
        print('B. Back')
        print('Q. Quit')
        print('====================================')
        choice = input('Enter choice: ')
        print('====================================')

        if choice == '1':
            tracker.display_account_graph()
        elif choice == '2':
            tracker.display_catagory_graph()
        elif choice == '3':
            tracker.display_loan_graph()
        elif choice == '4':
            tracker.display_income_graph()
        elif choice == 'B' or choice == 'b':
            choose_purpose()
        elif choice == 'Q' or choice == 'q':
            quit()
        else:
            print('Invalid choice')

def quit():
    tracker.save_data()
    print('Goodbye!')
    sys.exit()

def choose_purpose():
    print('Welcome to your finance tracker!')
    tracker.print_last_login()

    while True:
        print('====================================')
        print('What would you like to do?')
        print('1. Move your money')
        print('2. View data')
        print('3. Add data')
        print('4. Reset data')
        print('5. Display data')
        print('Q. Quit')
        print('====================================')
        choice = input('Enter choice: ')
        print('====================================')

        if choice == '1':
            move_money()
        elif choice == '2':
            view_data()
        elif choice == '3':
            add_data()
        elif choice == '4':
            reset_data()
        elif choice == '5':
            display_data()
        elif choice == 'Q' or choice == 'q':
            quit()
        else:
            print('Invalid choice')   

if __name__ == '__main__':
    tracker = FinanceTracker('finances.json')
    choose_purpose()

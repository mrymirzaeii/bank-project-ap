import csv
import datetime
from user import User
from account import Account

def load_users():
    users = []
    try:
        with open("data/users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(User(row["username"], row["password"], row["role"], row["status"]))
    except FileNotFoundError:
        print("users.csv not found!")
    return users

def load_accounts():
    accounts = []
    try:
        with open("data/accounts.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                accounts.append(Account(row["account_id"], row["username"], row["account_type"], float(row["balance"]), row["is_blocked"]))
    except FileNotFoundError:
        print("accounts.csv not found!")
    return accounts

def save_accounts(accounts):
    with open("data/accounts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["account_id", "username", "account_type", "balance", "is_blocked"])
        for acc in accounts:
            writer.writerow([acc.account_id, acc.username, acc.account_type, acc.balance, acc.is_blocked])

def save_users(users):
    with open("data/users.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password", "role", "status"])
        for u in users:
            writer.writerow([u.username, u.password, u.role, u.status])

def save_transaction(account_id, username, trans_type, amount, balance_after):
    with open("data/transactions.csv", "a", newline="") as file:
        writer = csv.writer(file)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([now, account_id, username, trans_type, amount, balance_after])

def show_transaction_report(username_filter=None):
    try:
        with open("data/transactions.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if not rows:
                print("\nهیچ تراکنشی یافت نشد.")
                return
            print("\n" + "="*95)
            print(f"{'تاریخ و ساعت':<20} {'شماره حساب':<12} {'کاربر':<12} {'نوع':<10} {'مبلغ':<15} {'موجودی بعد':<15}")
            print("="*95)
            for row in rows:
                if username_filter is None or row[2] == username_filter:
                    try:
                        amount = int(float(row[4]))
                        balance = int(float(row[5]))
                        print(f"{row[0]:<20} {row[1]:<12} {row[2]:<12} {row[3]:<10} {amount:>12,} تومان  {balance:>12,} تومان")
                    except:
                        print(f"{row[0]:<20} {row[1]:<12} {row[2]:<12} {row[3]:<10} {row[4]:>12} {row[5]:>12}")
            print("="*95 + "\n")
    except FileNotFoundError:
        print("\nفایل تراکنش‌ها یافت نشد. هنوز تراکنشی ثبت نشده است.")

def customer_menu(accounts, current_user):
    while True:
        print("\n--- Customer Menu ---")
        print("1. Show my accounts")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_accounts = [acc for acc in accounts if acc.username == current_user.username]
            if not user_accounts:
                print("No accounts found.")
            for acc in user_accounts:
                print(acc)

        elif choice == "2":
            account_id = input("Enter account ID: ")
            amount = float(input("Enter amount to deposit: "))
            for acc in accounts:
                if acc.account_id == account_id and acc.username == current_user.username:
                    if acc.deposit(amount, save_transaction):
                        print(f"Deposited {amount}. New balance: {acc.balance}")
                        save_accounts(accounts)
                    else:
                        print("Deposit failed.")
                    break
            else:
                print("Account not found.")
        elif choice == "3":
            account_id = input("Enter account ID: ")
            amount = float(input("Enter amount to withdraw: "))
            for acc in accounts:
                if acc.account_id == account_id and acc.username == current_user.username:
                    if acc.withdraw(amount, save_transaction):
                        print(f"Withdrew {amount}. New balance: {acc.balance}")
                        save_accounts(accounts)
                    else:
                        print("Withdrawal failed (insufficient balance or account blocked).")
                    break
            else:
                print("Account not found.")

        elif choice == "4":
            from_acc_id = input("Enter your account ID: ")
            to_acc_id = input("Enter target account ID: ")
            amount = float(input("Enter amount to transfer: "))

            from_acc = None
            to_acc = None
            for acc in accounts:
                if acc.account_id == from_acc_id and acc.username == current_user.username:
                    from_acc = acc
                if acc.account_id == to_acc_id:
                    to_acc = acc

            if from_acc and to_acc and from_acc != to_acc:
                if from_acc.withdraw(amount, save_transaction):
                    to_acc.deposit(amount, save_transaction)
                    save_accounts(accounts)
                    print(f"Transferred {amount} from {from_acc_id} to {to_acc_id}.")
                else:
                    print("Transfer failed.")
            else:
                print("Invalid account(s) or same account.")

        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")
def banker_menu(accounts, users):
    while True:
        print("\n--- Banker Menu ---")
        print("1. Open new account for existing user")
        print("2. Show all accounts")
        print("3. Block/unblock account")
        print("4. Show all users")
        print("5. Add new user (customer)")
        print("6. Show transaction report")
        print("7. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            user_exists = any(u.username == username for u in users)
            if not user_exists:
                print("User not found! First add user to system (option 5).")
                continue

            account_type = input("Account type (current/savings): ")
            initial_balance = float(input("Initial balance: "))
            account_id = input("Enter account ID manually (e.g., A1001): ")
            
            existing_ids = [acc.account_id for acc in accounts]
            if account_id in existing_ids:
                print("This account ID already exists! Try again.")
                continue
            
            new_account = Account(account_id, username, account_type, initial_balance, "no")
            accounts.append(new_account)
            save_accounts(accounts)
            print(f"Account {account_id} created for {username}.")

        elif choice == "2":
            if not accounts:
                print("No accounts found.")
            for acc in accounts:
                print(acc)

        elif choice == "3":
            account_id = input("Enter account ID to block/unblock: ")
            for acc in accounts:
                if acc.account_id == account_id:
                    if acc.is_blocked == "no":
                        acc.is_blocked = "yes"
                        print(f"Account {account_id} blocked.")
                    else:
                        acc.is_blocked = "no"
                        print(f"Account {account_id} unblocked.")
                    save_accounts(accounts)
                    break
            else:
                print("Account not found.")

        elif choice == "4":
            if not users:
                print("No users found.")
            for u in users:
                print(f"{u.username} ({u.role}) - {u.status}")

        elif choice == "5":
            new_username = input("Enter new username: ")
            new_password = input("Enter password: ")
            if any(u.username == new_username for u in users):
                print("Username already exists!")
                continue
            new_user = User(new_username, new_password, "customer", "active")
            users.append(new_user)
            save_users(users)
            print(f"User {new_username} added. Now you can open an account for them (option 1).")

        elif choice == "6":
            print("\n1. All transactions")
            print("2. Transactions of a specific user")
            sub = input("Enter choice: ")
            if sub == "1":
                show_transaction_report()
            elif sub == "2":
                username = input("Enter username: ")
                show_transaction_report(username)
            else:
                print("Invalid choice.")

        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")
def main():
    users = load_users()
    accounts = load_accounts()

    print("=== Bank System ===")
    username = input("Username: ")
    password = input("Password: ")

    user = User.login(users, username, password)
    if not user:
        print("Invalid login.")
        return

    print(f"Welcome {user.username} (Role: {user.role})")

    if user.role == "customer":
        customer_menu(accounts, user)
    else:
        banker_menu(accounts, users)

    print("Goodbye!")

if __name__ == "__main__":
    main()
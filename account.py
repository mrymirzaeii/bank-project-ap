class Account:
    def __init__(self, account_id, username, account_type, balance=0, is_blocked="no"):
        self.account_id = account_id
        self.username = username
        self.account_type = account_type
        self.balance = float(balance)
        self.is_blocked = is_blocked

    def deposit(self, amount, save_callback=None):
        if amount > 0 and self.is_blocked == "no":
            self.balance += amount
            if save_callback:
                save_callback(self.account_id, self.username, "deposit", amount, self.balance)
            return True
        return False

    def withdraw(self, amount, save_callback=None):
        if self.is_blocked == "no" and amount > 0 and self.balance >= amount:
            if self.account_type == "savings":
                min_balance = 50000
                max_withdraw_percent = 0.8
                max_withdraw = (self.balance - min_balance) * max_withdraw_percent
                if amount > max_withdraw:
                    print(f"حداکثر قابل برداشت: {max_withdraw:,.0f} تومان")
                    return False
                if self.balance - amount < min_balance:
                    print(f"حداقل موجودی باید {min_balance:,} تومان باشد")
                    return False
            self.balance -= amount
            if save_callback:
                save_callback(self.account_id, self.username, "withdraw", amount, self.balance)
            return True
        return False

    def __str__(self):
        return f"Account ID: {self.account_id} | Type: {self.account_type} | Balance: {self.balance:,.0f} | Blocked: {self.is_blocked}"
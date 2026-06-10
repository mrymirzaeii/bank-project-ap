class User:
    def __init__(self, username, password, role, status="active"):
        self.username = username
        self.password = password
        self.role = role
        self.status = status

    @staticmethod
    def login(users_list, username, password):
        for user in users_list:
            if user.username == username and user.password == password and user.status == "active":
                return user
        return None
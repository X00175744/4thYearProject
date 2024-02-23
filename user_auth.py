class SimpleLoginSystem:
    def __init__(self):
        # Dictionary to store user credentials (username: password)
        self.users = {}

    def register_user(self, username, password):
        """Register a new user."""
        if username in self.users:
            return False  # User already exists
        else:
            self.users[username] = password
            return True  # Registration successful

    def login(self, username, password):
        """Log in a user."""
        return username in self.users and self.users[username] == password

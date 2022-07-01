class UserBlacklisted(Exception):
    def __init__(self, message="User is blacklisted!") -> None:
        self.message = message
        super().__init__(self.message)
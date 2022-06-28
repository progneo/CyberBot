class UserBlacklisted(Exception):
    def __init__(self, message="User is blacklisted!") -> None:
        self.message = message
        super().__init__(self.message)


class UserNotOwner(Exception):
    def __init__(self, message="User is not an owner of the bot!") -> None:
        self.message = message
        super().__init__(self.message)
        
class ChannelNotNsfw(Exception):
    def __init__(self, message="This command only works in NSFW channels!") -> None:
        self.message = message
        super().__init__(self.message)
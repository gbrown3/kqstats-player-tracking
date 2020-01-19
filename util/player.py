import re

class Player:
    """
    A person who has signed in and indicated that
    they are playing a specific character in a match of KQ
    """

    def __init__(self, username):
        """
        Constructor for player object.

        Players are identified by username for now,
        so one must be passed in.
        """

        # For now, usernames must be purely alphanumeric.
        # If people really want it we can broaden the scope later.
        match = re.fullmatch(r'[a-zA-Z0-9]+', username)
        
        if match:
            self.username = username
        else:
            raise ValueError("username must be exclusively alphanumeric")

    def __eq__(self, obj):
        return isinstance(obj, Player) and obj.username == self.username


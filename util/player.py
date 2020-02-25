import re

class Player:
    """
    A person who has signed in and indicated that
    they are playing a specific character in a match of KQ
    on the connected cab.
    """

    def __init__(self, username):
        """
        Constructor for player object.

        Players are identified by username,
        so one must be passed in.
        """
        validated_name = Player.validate_name(username)
        self.username = validated_name

    def __eq__(self, obj):
        return isinstance(obj, Player) and obj.username == self.username

    @staticmethod
    def validate_name(name):
        """
        If the given string is a valid player name, returns that string. 
        Otherwise throws an exception with more detail about 
        what types of names are expected.
        """
        # For now, usernames must be purely alphanumeric.
        # If people really want it we can broaden the scope later.
        match = re.fullmatch(r'[a-zA-Z0-9]+', name)

        if match:
            return name
        else:
            raise ValueError("usernames must be purely alphanumeric")    

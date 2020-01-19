"""
Processes player selections and converts them to the 
format used by KQStream (from kq-stats repo)
"""

TEAM_KEY = "team"
CHARACTER_KEY = "character"
USER_KEY = "user"

CHARACTERS = {
    "gold": {
        "queen": 1,
        "stripes": 3,
        "abs": 5,
        "skull": 7,
        "checkers": 9
    },
    "blue": {
        "queen": 2,
        "stripes": 4,
        "abs": 6,
        "skull": 8,
        "checkers": 10
    }
}

def get_kqstream_character(team, character):
    """
    Returns an int which is the underlying stats
    representation the given character/team

    team -- string representing the team a character is on
    character -- string representing a character (ie queen, stripes, abs, etc)
    """
    return CHARACTERS[team][character]

def get_character_from_json(json):
    """
    Wrapper for get_kqstream_character which pull the character info out of 
    a JSON object.
    """
    team = json[TEAM_KEY]
    character = json[CHARACTER_KEY]

    return get_kqstream_character(team, character)
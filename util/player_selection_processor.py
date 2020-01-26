"""
Processes player selections and converts them to the 
format used by KQStream (from kq-stats repo)
"""

TEAM_KEY = "team"
CHARACTER_KEY = "character"
USER_KEY = "user"

CHARACTERS_BY_TEAM = {
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

CHARACTERs_BY_ID = {
    1: "gold_queen",
    2: "blue_queen",
    3: "gold_stripes",
    4: "blue_stripes",
    5: "gold_abs",
    6: "blue_abs",
    7: "gold_skull",
    8: "blue_skull",
    9: "gold_checkers",
    10: "blue_checkers"
}

def get_kqstream_character(team, character):
    """
    Returns an int which is the underlying stats
    representation the given character/team

    team -- string representing the team a character is on
    character -- string representing a character (ie queen, stripes, abs, etc)
    """
    return CHARACTERS_BY_TEAM[team][character]

def get_character_id_from_json(json):
    """
    Wrapper for get_kqstream_character which pull the character info out of 
    a JSON object.
    """
    team = json[TEAM_KEY]
    character = json[CHARACTER_KEY]

    return get_kqstream_character(team, character)

def update_available_characters(available_characters, taken_character):
    """
    Returns an updated version of availble_characters
    with the newly taken character's status updated.

    available_characters -- dictionary similar to CHARACTERS, but with booleans rather than ints
    taken_character -- int representing a character
    """
    character_and_team = CHARACTERs_BY_ID[taken_character].split("_")

    team = character_and_team[0]
    character = character_and_team[1]

    # This is just to satisfy my functional brain,
    # so we don't have to mutate an existing object
    updated_characters = available_characters.copy()
    updated_characters[team][character] = False

    return updated_characters


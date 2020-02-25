"""
Contains constants with informative error messages
"""

MALFORMED_JSON = 'Malformed JSON sent with request. Make sure you include something' \
                 ' like the following in the request body: {"name": "playernametovalidate"}'

INVALID_NAME = 'This name is invalid. Please pick a name that is exclusively made up of' \
               ' alphanumeric characters (no spaces or special characters).'
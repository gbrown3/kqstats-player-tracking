from flask import Flask, render_template, make_response, request, jsonify
from flask_socketio import SocketIO, emit
import json

from util.player import Player
from util import player_selection_processor
from util import events
from util import errors

app = Flask(__name__)
socketio = SocketIO(app, ping_interval=1, ping_timeout=3, transports=['websocket']) 

# Stores list of stats for each player
# Key = username, Value = list of endgame stats. 
playerstats = {}

# Players that are currently in a game (and will expect stats at the end)
# Key = character being played, Value = username
active_players = {}

# Full stat lists for each game, agnostic of actual players
game_stats = []

available_characters = {
    'gold': {
        'queen': True,
        'stripes': True,
        'abs': True,
        'skull': True,
        'checkers': True
    },
    'blue': {
        'queen': True,
        'stripes': True,
        'abs': True,
        'skull': True,
        'checkers': True
    }
}

@app.route('/')
def index():

    # TODO: Check if a cookie is present with the user's name. 
    # If so, use that. Otherwise pass in an empty string.
    user = ""

    return make_response(
        render_template(
            "index.html", 
            user=user, 
            available_characters=available_characters
        )
    )

@app.route('/players', methods=["GET"])
def players():
    """
    Returns information about players, which can be narrowed down with
    query params.

    Query Params accepted:

    active -- bool, if true then only stats for active players should be sent
    """

    active = request.args.get("active", False)

    if active:
        return make_response(active_players)
    else:
        return make_response(playerstats)

@app.route('/player/<username>', methods=["GET"])
def player(username):
    """
    Returns information about a specific player
    """

    stats = playerstats.get(username, None)

    print(playerstats)

    if stats == None:
        return make_response(render_template("notfound.html", username=username), 404)
    else:
        return make_response({username: stats})

@app.route('/player/validate', methods=["POST"])        
def validate_player_name():
    """
    Parses the request body to determine if a player name is valid.
    Player names are valid if they meet the following conditions:
    1. Fits character constraints defined in the Player class
    2. Name is not already taken.

    Response code will always be 200 OK, so detail error information
    can be included if relevant.

    If name is valid and hasn't already been taken, response will be 
    of the form {"success": true}

    Otherwise, the response will look like the following:
    {"error": "<insert error message here>"}
    """ 

    name = request.json.get("name", None)

    if name == None:
        return make_response({'error': errors.MALFORMED_JSON}, 200)
    else:
        # If name is invalid, return an error
        try:
            Player.validate_name(name)
        except ValueError as e:
            print("Exception caught: " + str(e))
            return make_response({'error': errors.INVALID_NAME}, 200)

        # If name has already been used, return an error
        # TODO: once data is stored in a database, this will need to be a database call
        if name in playerstats:
            return make_response({'error': f"The name '{name}' is already taken. Please choose another one."}, 200)

        # If player name is valid and unused, return 200 OK
        return make_response(jsonify({"success": True}))



@app.route('/playerselection', methods=["POST"])
def player_selection():
    """
    Responsible for handling incoming player character selections
    and connecting user data to the actual game stats.
    """
    global available_characters
    global active_players
    global playerstats

    player_selection = request.json
    print(player_selection)

    if player_selection == None:
        player_selection = {}

    username = player_selection[player_selection_processor.USER_KEY]
    character = player_selection_processor.get_character_id_from_json(player_selection)

    print("User:")
    print(username)
    print("Character: ")
    print(character)

    if username not in playerstats.keys():
        playerstats[username] = []

    active_players[character] = username

    available_characters = player_selection_processor.update_available_characters(
        available_characters, character
    )

    # Asynchronously update FE about character selection,
    # so there's less risk of two players trying to select the
    # same character.
    socketio.emit(
        events.CHARACTER_SELECTED,
        available_characters
    )

    return make_response(player_selection)

@app.route('/stats', methods=["POST"])
def stats():
    """
    Handles incoming stats and events from kqstats 
    (the service that connects directly to the cab)
    """
    global active_players

    # TODO: get json in a normal way once kqstats changes 
    # (see comment below for more deets)

    # Using XMLHttpRequest on kqstats isn't sending the content type
    # correctly for some reason, which is why we need to to add this 
    # force=True. Should be able to do this in a less wonky way once kqstats
    # is updated to use ajax or something like that.
    stats = request.get_json(force=True)
    if stats != None:
        game_stats.append(stats)
    else:
        stats = {}
        print("Empty stats set received")

    print("Stats received: ")
    print(stats)

    print("Request received:")
    print(request)

    # Save the general game stats. Will be useful for doing analysis 
    # on different cabinets/controls for each character (ie blue abs dies a lot)
    game_stats.append(stats)

    # Save the player-specific stats
    for character in stats.keys():

        print("active_players: " + str(active_players))

        # Determine if anyone is currently playing this character
        player = active_players.get(int(character), None)

        # If so, save their specific stats.
        if player != None:
            playerstats[player].append(stats[character])
            print(f"stats saved for player={player}")
        else:
            print(f"No one logged in as character with id={character}, so stats are saved generically")

    # TODO: only reset active_players when we reach a bonus map (end of set)
    active_players = {}

    # TODO: Send playerstats to firebase to store
    # maybe also send a websocket update to /viewstats to get updated info?

    return make_response()

@app.route('/viewstats', methods=['GET'])
def view_stats():

    return render_template("view_stats.html", game_stats=game_stats)


if __name__ == '__main__':
    socketio.run(app, debug=True)
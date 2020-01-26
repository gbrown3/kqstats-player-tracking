from flask import Flask, render_template, make_response, request, jsonify
from flask_socketio import SocketIO, emit
import json

from util import player_selection_processor
from util import events

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

    player = playerstats.get(username, None)

    if player == None:
        return make_response(render_template("notfound.html", username=username), 404)

@app.route('/playerselection', methods=["POST"])
def player_selection():
    """
    Responsible for handling incoming player character selections
    and connecting user data to the actual game stats.
    """
    global available_characters

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

    if username in playerstats.keys():
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

        # Determine if anyone is currently playing this character
        player = active_players.get(character, None)

        # If so, save their specific stats.
        if player != None:
            playerstats[player].append(stats[character])

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
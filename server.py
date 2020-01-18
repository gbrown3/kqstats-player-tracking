from flask import Flask, render_template, make_response, request, jsonify
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app, ping_interval=1, ping_timeout=3, transports=['websocket']) 

players = {}
game_stats = []

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/stats', methods=["POST"])
def stats():
    """
    Handles incoming stats and events from kqstats 
    (the service that connects directly to the cab)
    """
    # TODO: Do some processing to connect player names to game characters
    # TODO: Send processed data to firebase to store

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

    # For now, just echo back what was received
    print("Stats received: ")
    print(stats)

    print("Request received:")
    print(request)

    game_stats.append(stats)

    return make_response(stats)

@app.route('/viewstats', methods=['GET'])
def view_stats():

    return render_template("view_stats.html", game_stats=game_stats)    


if __name__ == '__main__':
    socketio.run(app, debug=True)
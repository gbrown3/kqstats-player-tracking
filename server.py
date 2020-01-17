from flask import Flask, make_response, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, ping_interval=1, ping_timeout=3, transports=['websocket']) 

@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    socketio.run(app, debug=True)
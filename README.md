# kqstats-player-tracking

## Overview
This service is intended to be used in tandem with the `develop` branch of [kqstats](https://github.com/gbrown3/kqstats/tree/develop), with the respective services filling the following roles:

`kqstats` - runs on the same network as the KQ cabinet, captures events and turns them into stats tracked for each character, and sends the stats (and game start/end events) to the player tracking service at the end of each match.

`kqstats-player-tracking` - hosted somewhere that is publicly accessible, provides a dynamic interface for people playing on the KQ cabinet to enter their name, indicate which character they're playing, and have their stats saved and tied to the name they entered.

## Tech Stack

- [Flask](http://flask.palletsprojects.com/en/1.1.x/quickstart/), the simple yet powerful Python server framework
- [Socketio](https://socket.io/docs/client-api/) and [Flask-Socketio](https://flask-socketio.readthedocs.io/en/latest/), for async communication with the frontend
- [Jinja2](https://jinja.palletsprojects.com/en/2.10.x/), for basic webpage templating

## Environment Setup
1. Clone this repository
```
cd yourDirectory
git clone git@github.com:gbrown3/kqstats-player-tracking.git
cd kqstats-player-tracking
```
2. Make sure you have the latest version of Python and pip installed, then set up your virtual environment
```
python3 -m venv venv
. ./venv/bin/activate
```
You should now see `(venv)` before each line of your command line prompt.  

3. With your virtual environment activated, install flask, socketio, and eventlet (which is required for socketio)
```
pip install flask
pip install flask-socketio --user
pip install eventlet --user
```
NOTE: You might not need to use the `--user` flag when installing SocketIO and Eventlet. I needed to in both cases, which is why I'm making it the default.

That's it! Remember to always activate your virtual environment with `. ./venv/bin/activate` in the `kqstats-player-tracking` directory before you start the server.

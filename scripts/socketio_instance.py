#!/home/sacred/myenv/bin/python3





#This file is meant to circumvent the circular log error from importing home.py and snake_handler.py
#at the same time.
from flask_socketio import SocketIO

socketio = SocketIO()

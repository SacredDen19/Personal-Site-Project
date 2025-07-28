#!/home/sacred/myenv/bin/python3
from flask import Flask, render_template, Blueprint, request, session, current_app
from api.datab import load_loggedin
from flask_socketio import emit, join_room #We get rid of socketIO and keep emit for communication
from scripts.snake_game import SnakeGame
from scripts.socketio_instance import socketio #imports socketio from this instance to avoid circular reference

#Basic declarations
user_games = {} #This dict will store individual game sessions in memory (figure out a better solution later)
snake_blueprint = Blueprint('snake_handler', __name__, template_folder='templates')


@snake_blueprint.route("/snake_game_page.html", methods=['POST'])
def show_Snake_Page():
	user = load_loggedin()
	session['current_page'] = 'snake_game_page.html'
	return render_template(session.get('current_page', 'snake_game_page.html'), user=user)

@snake_blueprint.route("/snake_game_redirect", methods=['POST'])
def return_home():
	user = load_loggedin()
	session['current_page'] = 'index.html'
	return render_template(session.get('current_page', 'index.html'), user=user)


#socketio has to be removed and game events have to be manually handled as done so above this comment. For later.
connected_devices = {}
@socketio.on('connect')
def on_connect():
	device_id = session.get('device_id')
	user_games[device_id] = SnakeGame()
	if device_id:
		join_room(device_id)
@socketio.on('move')
def handle_move_snake():
	device_id = session.get('device_id')
	game = user_games.get(device_id)
	game.move()
	socketio.emit('game_state', game.to_dict(), room=device_id)

@socketio.on('game_restart')
def handle_game_restart():
	device_id = session.get('device_id')
	game = user_games.get(device_id)
	game.restartGame()
	socketio.emit('game_state', game.to_dict(), room=device_id, broadcast=True)

@socketio.on('change_direction')
def handle_change_direction(direction):
	device_id = session.get('device_id')
	game = user_games.get(device_id)
	game.change_direction(direction)
	socketio.emit(room=device_id)


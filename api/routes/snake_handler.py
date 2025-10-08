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
	print(f'SNAKE GAME PAGE LOADED. SESSIONS: {session}')
	user = load_loggedin()
	session['current_page'] = 'snake_game_page.html'
	return render_template(session.get('current_page', 'snake_game_page.html'), user=user)

@snake_blueprint.route("/snake_game_redirect", methods=['POST'])
def return_home():
	user = load_loggedin()
	session['current_page'] = 'index.html'
	return render_template(session.get('current_page', 'index.html'), user=user)


#socketio live events
connected_devices = {}
@socketio.on('connect', namespace='/snake_game')
def on_connect():
	print(f'CONNECTION WITH BACK END SOCKET INTIATED BY DEVICE ID: {session.get("device_id")} \nOR {session}')
	device_id = session.get('device_id')
	user_games[device_id] = SnakeGame()
	#print(f'\n on_connect device id value: {device_id}\nclient game values: {user_games}\nclient side game {user_games[device_id]}')
	if device_id:
		print(f'\n\n IF STATEMENT WITHIN IF ON CONNECT RAN \n device ID: {device_id}\n user games: {user_games} \n user ID game: {user_games[device_id].__dict__}\n\n')
		user_games[device_id] = SnakeGame()
		join_room(device_id)
		#socketio.emit('game_started')
@socketio.on('move', namespace='/snake_game')
def handle_move_snake():
	print('SOCKET MOVE FUNCTION EXECUTED')
	device_id = session.get('device_id')
	game = user_games.get(device_id)
	print(f'\n\nToubleshooting game value: {game.__dict__}\n\nGame.move value: {game.move()}\n\n')
	print(f'\nUSER GAMES VALUE: {user_games}\n')
	game.move()
	print(f'\n Game dictionary: {game.to_dict()}')
	socketio.emit('game_state', game.to_dict(), room=device_id, namespace='/snake_game')

@socketio.on('game_restart', namespace='/snake_game')
def handle_game_restart():
	print('GAME RESTART SOCKET EVENT DETECTED')
	device_id = session.get('device_id')
	game = user_games.get(device_id)
	game.restartGame()
	socketio.emit('game_state', game.to_dict(), room=device_id, broadcast=True, namespace='snake_game')

@socketio.on('change_direction', namespace='/snake_game')
def handle_change_direction(direction):
	print('CHANGE DIRECTION EVENT DETECTED IN THE BACK END')
	device_id = session.get('device_id')
	game = user_games.get(device_id)
	game.change_direction(direction)
	socketio.emit(room=device_id, namespace='snake_game')


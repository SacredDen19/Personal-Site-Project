#!/home/sacred/myenv/bin/python3
from flask import Flask, render_template, Blueprint, request, session
from flask_socketio import emit #We get rid of socketIO and keep emit for communication
from scripts.snake_game import SnakeGame
from scripts.socketio_instance import socketio #imports socketio from this instance to avoid circular reference

#Basic declarations
#app = Flask(__name__)
#socketio = SocketIO(app)
game = SnakeGame()

snake_Handler = Blueprint('snake_Handler', __name__, template_folder='templates')


@snake_Handler.route("/snake_game_page.html", methods=['POST'])
def show_Snake_Page():
	session['current_page'] = 'snake_game_page.html'
	return render_template(session.get('current_page', 'snake_game_page.html'))

@snake_Handler.route("/snake_game_redirect", methods=['POST'])
def return_home():
	session['current_page'] = 'index.html'
	return render_template(session.get('current_page', 'index.html'))


#socketio has to be removed and game events have to be manually handled as done so above this comment. For later.
@socketio.on('move')
def handle_move_snake():
	game.move()
	socketio.emit('game_state', game.to_dict())
@socketio.on('game_restart')
def handle_game_restart():
	game.restartGame()
	socketio.emit('game_state', game.to_dict(), broadcast=True)
@socketio.on('change_direction')
def handle_change_direction(direction):
	game.change_direction(direction)

#if __name__ == '__main__':
#	socketio.run(app, debug=True)


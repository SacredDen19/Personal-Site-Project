#!/home/sacred/myenv/bin/python3
from flask import Flask, render_template, Blueprint
#from flask_socketio import SocketIO, emit
from scripts.snake_game import SnakeGame
from home import socketio

#Basic declarations
#app = Flask(__name__)
#socketio = SocketIO(app)
game = SnakeGame()

snake_Handler = Blueprint('snake_Handler', __name__, template_folder='templates')


@snake_Handler.route("/snake_game_page.html")
def show_Snake_Page():
	return render_template('snake_game_page.html')

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

if __name__ == '__main__':
	socketio.run(app, debug=True)


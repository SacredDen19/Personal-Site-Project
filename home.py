#!/home/sacred/myenv/bin/python3
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from snake_handler import  snake_Handler

homeApp = Flask(__name__)

#Registers snake_Handler's blueprint
#This will handle the snake game page
homeApp.register_blueprint(snake_Handler)

socketio = SocketIO(homeApp)

#Defines index (home) page
@homeApp.route("/")
def index():
	return render_template('index.html')


#Listens for the Snake Game Button Press in the home page
#It then emits the move event to the front end to redirect the page
@socketio.on('move_to_snake')
def snake_Page():
	socketio.emit('snakeGame_redirect')

if __name__ == '__main__':
	socketio.run(homeApp, debug=True)

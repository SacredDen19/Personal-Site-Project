#!/home/sacred/myenv/bin/python3
from flask import Flask, render_template, request
from flask_socketio import emit #We get rid of socketIO and keep emit for communication
from dotenv import load_dotenv #This is needed for importing the .env which securely stores sensitive credentials
from snake_handler import  snake_Handler
from scripts.socketio_instance import socketio
import mysql.connector
import os

load_dotenv() #Loads vaeiables from the env file
homeApp = Flask(__name__)
socketio.init_app(homeApp)
#Connects to MySQL using the credentials found in .env using dotenv functions
db = mysql.connector.connect(
	host=os.getenv("DB_HOST"),
	user=os.getenv("DB_USER"),
	password=os.getenv("DB_PASSWORD"),
	database=os.getenv("DB_NAME")
)

cursor = db.cursor()



#Registers snake_Handler's blueprint
#This will handle the snake game page
homeApp.register_blueprint(snake_Handler)

#Defines index (home) page
@homeApp.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		usrName = request.form.get('usr')
		usrPass = request.form.get('secret')
		


#Listens for the Snake Game Button Press in the home page
#It then emits the move event to the front end to redirect the page
@socketio.on('move_to_snake')
def snake_Page():
	socketio.emit('snakeGame_redirect')

if __name__ == '__main__':
	socketio.run(homeApp, debug=True)

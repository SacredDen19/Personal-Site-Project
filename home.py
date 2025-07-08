#!/home/sacred/myenv/bin/python3
from flask import Flask, render_template, request, session, redirect
from flask_socketio import emit #We get rid of socketIO and keep emit for communication
from dotenv import load_dotenv #This is needed for importing the .env which securely stores sensitive credentials
from snake_handler import  snake_Handler
from scripts.socketio_instance import socketio
import mysql.connector
import uuid #Used for creating unique user IDs during sessions
import os

#Debugging
#print("DB_USER:", os.getenv("DB_USER"))
#print("DB_USER:", os.getenv("DB_PASSWORD"))
#print("DB_USER:", os.getenv("DB_NAME"))

load_dotenv() #Loads vaeiables from the env file
homeApp = Flask(__name__)
homeApp.secret_key = os.getenv('SECRET_KEY') #Retrieves and sets the secret key from the .env file. Needed for user specific sessions
socketio.init_app(homeApp, manage_session=False)




#Registers snake_Handler's blueprint
#This will handle the snake game page
homeApp.register_blueprint(snake_Handler)

#Defines index (home) page
@homeApp.route("/", methods=['GET', 'POST'])
def index():
	if 'device_id' not in session:
		session['device_id'] = str(uuid.uuid4())
		session['visits'] = 1
		session['current_page'] = 'index.html'
	else:
		session['visits'] += 1

	if request.method == 'GET':
		session['current page'] = 'index.html'
		return render_template('index.html')
	
	if request.method == 'POST':
		usrName = request.form.get('usr')
		usrPass = request.form.get('secret')

		#Repositioned here for session handling
		#Connects to MySQL using the credentials found in .env using dotenv functions
		db = mysql.connector.connect(
		host=os.getenv("DB_HOST"),
		user=os.getenv("DB_USER"),
		password=os.getenv("DB_PASSWORD"),
		database=os.getenv("DB_NAME"),
		auth_plugin='mysql_native_password' #Forces the native password plugin to circumvent SSL restrictions (NOT SECURE AT ALL WILL CHANGE LATER)
		)
		cursor = db.cursor()
		
		#Cursor allows flask to interact with the database
		cursor.execute("SELECT * FROM users WHERE Username = %s AND Password = %s", (usrName, usrPass))
		user = cursor.fetchone()
			
		#Checks user authentication
		if user:
			return render_template('account.html')
		else:
			return "Invalid credentials", 401

if __name__ == '__main__':
	socketio.run(homeApp, debug=True)

from flask import Flask, render_template, request, Blueprint, session, redirect, current_app
import uuid #Used for creating unique user IDs during sessions
from flask import current_app #This helps prevent circular errors instead of doing the other import (from api import current_app)
import mysql.connector
blueprint_main = Blueprint("main", __name__)


#This route will handle landing page traffic
#Defines index (home) page
@blueprint_main.route("/", methods=['GET', 'POST'])
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
		host=current_app.config["DB_HOST"],
		user=current_app.config["DB_USER"],
		password=current_app.config["DB_PASSWORD"],
		database=current_app.config["DB_NAME"],
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
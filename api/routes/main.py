from flask import Flask, render_template, request, Blueprint, session, redirect
import uuid #Used for creating unique user IDs during sessions
from flask import current_app #This helps prevent circular errors instead of doing the other import (from api import current_app)
from api.datab import db_start_connection, load_loggedin
blueprint_main = Blueprint("main", __name__)

#This route will handle landing page traffic
#Defines index (home) page
@blueprint_main.route("/", methods=['GET', 'POST'])
def index():
	user = None

	#Checks for sessions
	if 'user_id' not in session:
		session['device_id'] = str(uuid.uuid4())
		session['visits'] = 1
		session['current_page'] = 'index.html'
	else:
		user = load_loggedin()
		session['visits'] += 1


	if request.method == 'GET':
		session['current page'] = 'index.html'
		return render_template('index.html', user=user)
	
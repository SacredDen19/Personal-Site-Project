#This will include the login and register routes
from flask import sessions, Flask, render_template, request, session, Blueprint, redirect, url_for, Response
import sys
from api.datab import load_loggedin, db_start_connection, register_user, delete_registered

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register():
		if request.method == 'POST':
			usrName = request.form.get('reg-usr', '').strip() #Defaults to '' if no value; Removes whitespace
			usrPass = request.form.get('reg-secret', '').strip()
			if not usrName or not usrPass:
				register_error = "Username and password cannot be empty or contain white space."
				return render_template('index.html', register_error=register_error, user=None)
			else:
				register_result = register_user(usrName, usrPass)
				if register_result is True:
					user = load_loggedin()
					return render_template('account.html', user=user)
				else:
					register_error = register_result
					return render_template('index.html', register_error=register_error, user=None)
                    
#Login
@auth_blueprint.route('/login', methods=['POST'])
def login():
	if request.method == 'POST':
		usrName = request.form.get('usr')
		usrPass = request.form.get('secret')


		conn = db_start_connection()
		cursor = conn.cursor(dictionary=True)
		
		#Cursor allows flask to interact with the database
		#cursor.execute(f"SELECT * FROM users WHERE Username = '{usrName}' AND Password = '{usrPass}'") DO NOT USE IN REAL PRODUCTION ONLY FOR TESTING AND EDUCATIONAL PURPOSES
		cursor.execute("SELECT * FROM users WHERE Username = %s AND Password = %s", (usrName, usrPass)) #using %s prevents basic MySQL injections
		user = cursor.fetchone()
			
		#Checks user authentication
		if user:
			session["user_id"] = user["Userid"]
			return render_template('account.html', user=user)
		else:
			return render_template('index.html', error="Invalid username or password.", user=None)
		
@auth_blueprint.route('/logout', methods=['POST'])
def logout():
	user = None
	print(f'session: {dict(session)} cleared')
	session.clear()
	return redirect(url_for('main.index', user=user))
	
@auth_blueprint.route('/log-redirect')
def log_redirect():
	user = load_loggedin()
	if user:
		return render_template('account.html', user=user)
	else:
	    return Response(status=204)

@auth_blueprint.route('/account_delete', methods=['POST'])
def account_delete():
	user = load_loggedin()
	if request.method == 'POST':
		if delete_registered():
			user = None
			session.clear()
			return render_template('index.html', user=user)
		else:
			return render_template('account.html', user=user)
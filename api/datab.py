from flask import current_app, session
import mysql.connector
from mysql.connector import IntegrityError

def db_start_connection():
    	#Repositioned here for session handling
		#Connects to MySQL using the credentials found in .env using dotenv functions
		db = mysql.connector.connect(
		host=current_app.config["DB_HOST"],
		user=current_app.config["DB_USER"],
		password=current_app.config["DB_PASSWORD"],
		database=current_app.config["DB_NAME"],
		auth_plugin='mysql_native_password' #Forces the native password plugin to circumvent SSL restrictions (NOT SECURE AT ALL WILL CHANGE LATER)
		)
		return db

#This function handles the creation of new users in the site
def register_user(username, password):
	print('register function debug')
	conn = None
	cursor = None
	try:
		print("try functions debug")
		conn = db_start_connection()
		cursor = conn.cursor(dictionary=True)
		#Creates new user account in MySQL database
		cursor.execute("INSERT INTO users (Username, Password) VALUES (%s, %s)", (username, password))
		conn.commit()
		#Requeries the newly created user for instant session creation
		cursor.execute("SELECT Userid, Username FROM users WHERE Username = %s", (username,))
		user = cursor.fetchone()

		#Session values
		session['user_id'] = user['Userid']
		print("THis is username: ", session['username'])
		return True
	except IntegrityError: #Checks for double entry in database
		error = f'The username {username} is taken'
		return error
	except Exception:
		error = f'There was an error processing the request'
		return error
	finally:
		#checks for these connections, then closes them
		if cursor:
			cursor.close()
		if conn:
			conn.close()
def load_loggedin():
	if 'user_id' in session:	
		conn = db_start_connection()
		cursor = conn.cursor(dictionary=True)
		cursor.execute("SELECT * FROM users WHERE Userid = %s", (session["user_id"],))
		user = cursor.fetchone()

		session['username'] = user['Username']
		print(user)
		return user
	else:
		user=None
		return user
def delete_registered():
	try:
		conn = db_start_connection()
		cursor = conn.cursor(dictionary=True)
		user = load_loggedin()
		if user:
			print(f"{user} entry and session:{dict(session)} cleared.")
			cursor.execute("DELETE FROM users WHERE Userid = %s", (user['Userid'],))
			conn.commit()
			return True
		else:
			return False
	except Exception:
		print("There was an error handling this request")
		return False
	finally:
		if cursor:
			cursor.close()
		if conn:
			conn.close()		


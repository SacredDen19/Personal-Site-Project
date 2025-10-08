from flask import Flask, session
from .config import Config
from .routes import blueprint_main, snake_blueprint, auth_blueprint, conv_blueprint, admin_panel
from dotenv import load_dotenv
#from flask_socketio import SocketIO
from scripts.socketio_instance import socketio
import mysql.connector


load_dotenv()

def main_app():
     
    mainApp = Flask(__name__, static_folder='static', template_folder='../templates')
    mainApp.config.from_object(Config) #Loads everything in config
    #mainApp.secret_key = SECRET_KEY
    
    socketio.init_app(mainApp, manage_session=False)

    #Blueprints of important route handlers
    mainApp.register_blueprint(blueprint_main)
    mainApp.register_blueprint(snake_blueprint)
    mainApp.register_blueprint(auth_blueprint)
    mainApp.register_blueprint(conv_blueprint)
    mainApp.register_blueprint(admin_panel)
    

    return mainApp
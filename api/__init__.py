from flask import Flask, session
from .config import Config
from snake_handler import  snake_Handler
from .routes import blueprint_main
from dotenv import load_dotenv
import mysql.connector


def main_app():
    load_dotenv()
    mainApp = Flask(__name__)
    mainApp.config.from_object(Config) #Loads everything in config

    #Blueprints of important route handlers
    mainApp.register_blueprint(snake_Handler)
    mainApp.register_blueprint(blueprint_main)


    return main_app
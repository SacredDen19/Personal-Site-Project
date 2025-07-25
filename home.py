#!/home/sacred/myenv/bin/python3
from api import main_app
from scripts.socketio_instance import socketio
from flask import Flask, render_template, request, session, redirect
#from flask_socketio import emit #We get rid of socketIO and keep emit for communication
#from dotenv import load_dotenv #This is needed for importing the .env which securely stores sensitive credentials
#from snake_handler import  snake_Handler
#from scripts.socketio_instance import socketio
#import mysql.connector
#import uuid #Used for creating unique user IDs during sessions
#import os

#Debugging
#print("DB_USER:", os.getenv("DB_USER"))
#print("DB_USER:", os.getenv("DB_PASSWORD"))
#print("DB_USER:", os.getenv("DB_NAME"))

#load_dotenv() #Loads vaeiables from the env file
homeApp = main_app()
#homeApp.secret_key = os.getenv('SECRET_KEY') #Retrieves and sets the secret key from the .env file. Needed for user specific sessions


if __name__ == '__main__':
    socketio.init_app(homeApp, manage_session=False)
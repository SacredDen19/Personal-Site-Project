import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Config():

    SECRET_KEY = os.getenv('SECRET_KEY') #Retrieves and sets the secret key from the .env file. Needed for user specific sessions
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    #Repositioned here for session handling
    #Connects to MySQL using the credentials found in .env using dotenv functions
    
    DB_HOST=os.getenv("DB_HOST")
    DB_USER=os.getenv("DB_USER")
    DB_PASSWORD=os.getenv("DB_PASSWORD")
    DB_NAME=os.getenv("DB_NAME")
    auth_plugin='mysql_native_password' #Forces the native password plugin to circumvent SSL restrictions (NOT SECURE AT ALL WILL CHANGE LATER)
    
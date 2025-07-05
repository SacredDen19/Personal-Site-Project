#!/usr/bin/python3
import sys
import os
import site
from dotenv import load_dotenv


#Sets the working directory
sys.path.insert(0, '/var/www/public_html')
#Loads the .env file manually
os.chdir('/var/www/public_html')

load_dotenv('.env') #looks for .env in the working directory

from home import homeApp as application


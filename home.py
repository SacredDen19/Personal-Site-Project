#!/usr/bin/python3
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
#Defines index (home) page
def index():
	return render_template('index.html')

#Defines the hello python page
#@app.route('/Hello')
#def hello():
#	return 'Hello, World'

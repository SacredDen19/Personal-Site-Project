from flask import sessions, Flask, render_template, request, session, Blueprint, redirect, url_for, Response
import sys
from api.datab import load_loggedin, db_start_connection, register_user, delete_registered

conv_blueprint = Blueprint('conv', __name__)


@conv_blueprint.route('/conversations', methods=['GET'])
def main():
    if request.method == 'GET':
        user = load_loggedin()
        messages = [
            {'user': 'user1', 'text':"Hello, user2, how are you?", 'time': "08-06-2025 13:00"},
            {'user': 'user2', 'text':"Hello user1, I am good. How is it?", 'time': "08-06-2025 13:02"},
            {'user': 'user1', 'text':"It is very good. How's the day?", 'time': "08-06-2025 13:10"},
            {'user': 'user2', 'text':"It's a nice day.", 'time': "08-06-2025 17:35"},
            {'user': 'user2', 'text':"Did you get those documents?", 'time': "08-06-2025 17:35"},
            {'user': 'user1', 'text':"I have not got them yet.", 'time': "08-06-2025 17:38"},
            {'user': 'user2', 'text':"Office closes early today. Hurry.", 'time': "08-06-2025 17:41"},
            {'user': 'user1', 'text':"I will now. Thanks.", 'time': "08-06-2025 17:55"},
            {'user': 'user2', 'text':"No problem, don't forget to get your drive", 'time': "08-06-2025 18:01"},
            {'user': 'user1', 'text':"Of course, I won't forget.", 'time': "08-06-2025 18:04"},

        ]
        sorted_messages = sorted(messages, key=lambda x: x['time']) #Sorts the messages dictionary using lambda function x which iterates through each message in messages dictionary and sorts them by time
        return render_template('conversations.html', user=user, messages=sorted_messages)
from flask import sessions, Flask, render_template, request, session, Blueprint, redirect, url_for, Response, jsonify
import sys
from api.datab import load_loggedin, db_start_connection, register_user, delete_registered

conv_blueprint = Blueprint('conv', __name__)


@conv_blueprint.route('/conversations', methods=['GET'])
def main():
    if request.method == 'GET':
        user = load_loggedin()
        conversations = get_conversations()
        #sorted_messages = sorted(messages, key=lambda x: x['time']) Sorts the messages dictionary using lambda function x which iterates through each message in messages dictionary and sorts them by time
        return render_template('conversations.html', user=user, conversations=conversations)
    
@conv_blueprint.route('/conversations/<conversationID>', methods=['GET'])
def show_conversation(conversationID):

    conversation_id = get_conversations().get(conversationID)

    #conversations_json = jsonify(get_conversations())
    return jsonify(conversation_id)
    #return render_template('conversations.html', user=user, messages=conversations, conversations_json=conversations_json)



def get_messages():

    messages = [
        {'conversationID': 0, 'user': 'user2', 'text':"Welcome to the conversation page. More to come.", 'time': "08-06-2025 11:00"},
        {'conversationID': 1, 'user': 'user1', 'text':"Hello, user2, how are you?", 'time': "08-06-2025 13:00"},
        {'conversationID': 1, 'user': 'user2', 'text':"Hello user1, I am good. How is it?", 'time': "08-06-2025 13:02"},
        {'conversationID': 1, 'user': 'user1', 'text':"It is very good. How's the day?", 'time': "08-06-2025 13:10"},
        {'conversationID': 1, 'user': 'user2', 'text':"It's a nice day.", 'time': "08-06-2025 17:35"},
        {'conversationID': 1, 'user': 'user2', 'text':"Did you get those documents?", 'time': "08-06-2025 17:35"},
        {'conversationID': 1, 'user': 'user1', 'text':"I have not got them yet.", 'time': "08-06-2025 17:38"},
        {'conversationID': 1, 'user': 'user2', 'text':"Office closes early today. Hurry.", 'time': "08-06-2025 17:41"},
        {'conversationID': 1, 'user': 'user1', 'text':"I will now. Thanks.", 'time': "08-06-2025 17:55"},
        {'conversationID': 1, 'user': 'user2', 'text':"No problem, don't forget to get your drive", 'time': "08-06-2025 18:01"},
        {'conversationID': 1, 'user': 'user1', 'text':"Of course, I won't forget.", 'time': "08-06-2025 18:04"},
        
    ]
    sorted_messages = sorted(messages, key=lambda x: x['time']) #Sorts the messages dictionary using lambda function x which iterates through each message in messages dictionary and sorts them by time
    return sorted_messages


def get_conversations():
    conversations = {
        '0' : {
            "messages" : [{'user': 'user2', 'text':"Welcome to the conversation page. More to come.", 'time': "08-06-2025 11:00"}
            ]},
        '1' :{ 
            "messages" : [
            {'user': 'user1', 'text':"Hello, user2, how are you?", 'time': "08-06-2025 13:00"},
            {'user': 'user2', 'text':"Hello user1, I am good. How is it?", 'time': "08-06-2025 13:02"},
            {'user': 'user1', 'text':"It is very good. How's the day?", 'time': "08-06-2025 13:10"},
            {'user': 'user2', 'text':"It's a nice day.", 'time': "08-06-2025 17:35"},
            {'user': 'user2', 'text':"Did you get those documents?", 'time': "08-06-2025 17:35"},
            {'user': 'user1', 'text':"I have not got them yet.", 'time': "08-06-2025 17:38"},
            {'user': 'user2', 'text':"Office closes early today. Hurry.", 'time': "08-06-2025 17:41"},
            {'user': 'user1', 'text':"I will now. Thanks.", 'time': "08-06-2025 17:55"},
            {'user': 'user2', 'text':"No problem, don't forget to get your drive", 'time': "08-06-2025 18:01"},
            
            {'user': 'user1', 'text':"New day, new conversation sample.", 'time': "08-10-2025 00:04"},
            {'user': 'user2', 'text':"Right, this sample conversation At one point the scroll bar and text wrapping will be put to the test with this message. Do you think so otherwise?", 'time': "08-10-2025 00:14"},
            {'user': 'user1', 'text':"I try not to be a pessimist about the conversations sample features.", 'time': "08-10-2025 00:18"},
            {'user': 'user1', 'text':"At one point everything will be fixed and things will be better", 'time': "08-10-2025 00:24"},
            {'user': 'user2', 'text':"I guess we will see where time takes us.", 'time': "08-10-2025 01:04"},
        ]},
        '2' :{},
    }
    return conversations
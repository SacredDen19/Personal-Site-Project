from flask import sessions, Flask, render_template, request, session, Blueprint, redirect, url_for, Response, jsonify
import json
from api.datab import load_loggedin, db_start_connection, register_user, delete_registered
from ..models.messages import message
from ..models.conversation_member import conversation_member

conv_blueprint = Blueprint('conv', __name__)


@conv_blueprint.route('/conversations', methods=['GET'])
def main():
    if request.method == 'GET':
        user = load_loggedin()
        #Sets the correct user conversations and their previews
        conversations = conversation_member.caller_id('READ', record_id=session['user_id'])
        #print(f'main class ran! Conversations value: {conversations}')
        #sorted_messages = sorted(messages, key=lambda x: x['time']) Sorts the messages dictionary using lambda function x which iterates through each message in messages dictionary and sorts them by time
        return render_template('conversations.html', user=user, conversations=conversations)
    
#This route is in charge of showing each message posted per preview clicked
@conv_blueprint.route('/conversations/<int:conversationID>', methods=['GET', 'POSt'])
def show_conversation(conversationID):
    user = load_loggedin()
    match request.method:
        case 'GET': 
            conversation_id = conversationID
            messages_posted = message.caller_id('READ', record_id=conversation_id)
            print("Printing users within conversations context: ",user.get("Username"))
            #print("Below will print the messages posted: ")
            #print([message_posted.to_dict() for message_posted in messages_posted])
            return jsonify({
                'messages': [message_posted.to_dict() for message_posted in messages_posted],
                'username' : [user.get("Username")],
                })
        case 'POST':
            data = request.get_json()
            sent_by = session['user_id'] #Sets the sent_id for insertion
            raw_text = data['message_text']
            parent_id = data['parent']

            print("Printing data before crash: ", data)
            user = data['username']
            print(f'Sent by user: {user} with ID: {sent_by} \n Raw message text: {raw_text} \n Conversation parent: {parent_id}')
            
            message.caller_id('WRITE', sent_by=sent_by, raw_text=raw_text, parent_id=parent_id, user=user)
            return jsonify({
                "status": "success",
                "message": "Message was added successfully",
                "data": {
                    "sent_by": sent_by,
                    "message_text": raw_text,
                    "parent_id": parent_id
                }

            })

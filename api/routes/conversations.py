import json
from scripts.socketio_instance import socketio
from flask_socketio import join_room, emit, leave_room
from flask import sessions, Flask, render_template, request, session, Blueprint, redirect, url_for, Response, jsonify
from api.datab import load_loggedin, db_start_connection, register_user, delete_registered
from ..models.messages import message
from ..models.conversation_member import conversation_member
from ..models.conversations import conversation, getConversation
from ..models.user import getUser
import re #needed for string formatting

conv_blueprint = Blueprint('conv', __name__)


@conv_blueprint.route('/conversations', methods=['GET'])
def main():
    if request.method == 'GET':
        user = load_loggedin()
        print(f'{session["user_id"]} has loaded the conversations page')
        #Sets the correct user conversations and their previews
        conversations = conversation_member.caller_id('READ', record_id=session['user_id'])
        print(f'conversations were loaded! {conversations}')
        return render_template('conversations.html', user=user, conversations=conversations)

#This route is in charge of showing each message posted per preview clicked
@conv_blueprint.route('/conversations/<int:conversationID>', methods=['GET', 'POSt'])
def show_conversation(conversationID):
    user = load_loggedin()
    match request.method:
        case 'GET': 
            if request.headers.get('Requested-By') != 'Fetch':
                return redirect(url_for("conv.main"))
            else:
                conversation_id = conversationID
                messages_posted = message.caller_id('READ', record_id=conversation_id) or []
                return jsonify({
                    'messages': [message_posted.to_dict() for message_posted in messages_posted],
                    'username' : [user.get("Username")],
                    })
        case 'POST':
            data = request.get_json()
            sent_by = session['user_id'] #Sets the sent_id for insertion
            raw_text = data['message_text']
            parent_id = data['parent']
            user = data['username']            
            message.caller_id('WRITE', sent_by=sent_by, raw_text=raw_text, parent_id=parent_id, user=user)
            return jsonify({
                "status": "success",
                "message": "Message was added successfully",
                "data": {
                    "username:" : user,
                    "sent_by": sent_by,
                    "message_text": raw_text,
                    "parent_id": parent_id
                }

            })
#Handles conversation creation requests by Fetch API
@conv_blueprint.route('/conversations/create', methods=['POST'])
def create_conversation():
    data = request.json
    match request.method:
        case 'POST':
            try:
                created_by = session['user_id']
                title = data['title']
                input = data['input']

                #BASIC CHECKS AND SANITIZATION

                #INPUT FORMATTING
                #Using re, we set the delimiters to be "" and "," ([ ,] that's what this is)
                #strip and if x clear out any trailing spaces to prevent things like '', or ','
                #This results in a few use and mix of commas and white spaces in the user input
                finput = [x for x in re.split(r"[ ,]+", input.strip()) if x]
                
                usernames = []
                unique_usernames = []
                user_ids = []
                print(f'This is finput = {finput}')

                if not finput:
                    raise Exception('Users field cannot be empty. Try again.')
                #THIS IS LIST COMPREHESION
                #CREATE LISTS BASED ON WHETHER THE USER ENTERED ALPHANUMERIC OR JUST NUMBERS FOR USERNAMES AND/OR USER ID
                for user in finput:
                    if user.isdigit():
                        user_ids.append(int(user))
                    else:
                        usernames.append(user)

                #Gets user ID using username
                usernames_and_ids_toAdd = []
                for username in usernames:
                    if username not in unique_usernames and username != session['username']:
                        unique_usernames.append(username)
                        u = getUser.caller_id('READ', record_id=username)
                        #Checks if the username entered exists in the database or not
                        if not u:
                            raise ValueError(f'Username, {username}, does not exist. Try again.')

                        usernames_and_ids_toAdd.append({
                            'username' : u[0].Username,
                            'user_id' : u[0].Userid
                        })
                    else:
                        raise Exception(f'An error occurred. Were you trying to add your identifier or username to the conversation?')
                print("THIS IS THE QUERY TO THE BACK END FOR GETTING USER IDS FROM USERNAMES: ", usernames_and_ids_toAdd)
                print(session)
                
                #ACTUALLY START WRITING INTO DATABASE HERE AFTER BASIC CHECKS

                #Creates the converastion in MySQL
                conversation.caller_id('WRITE-CONVERSATION', title=title, created_by=created_by)

                #Gets all conversations created by the given user ID
                conversationsCreatedById = getConversation.caller_id('READ', record_id=created_by)
                conversationsList  = []
                for conv in conversationsCreatedById:
                    conversationsList.append(conv)
                print(f'PRINT CONVERSATIONS CREATED BY USER ID {created_by} CONVERSATION: {conversationsList}')
                
                #DISCARD ---> Gets the newly created conversation's ID using it's name and the ID of the user that created it
                #Gets the newest conversation created by the user which should be the one they are requesting to make here
                new_conversation = conversationsList[len(conversationsList)-1]
                print(f'This is userid: {created_by} most newly created conversation ID: {new_conversation.conversation_id}')
                
                #Puts each user using their usernames entered by the conversation creator into the conversation, including the creator's
                usernames_and_ids_toAdd.append({ #Appends creator to the list of usernames and IDs to add
                 'username': session['username'],
                 'user_id' : created_by
                })
                new_conversation_id = new_conversation.conversation_id
                for member in usernames_and_ids_toAdd:
                    print(f'This is each conversation member {member} and the newest conv id: {new_conversation.conversation_id}')
                    conversation_member.caller_id('WRITE_CONVERSATION_MEMBER', conv_id=new_conversation_id, **member) ## **member turns member into function arguments
                    
                    #Checks if the currently cached users are in the conversation
                    print(f'CREATE ROUTE POST DETECTED. RAW DATA: {data}\nFORMATTED DATA: {finput}\nCREATED BY: {created_by}')
                    for cached_user_objects in cached_users:
                        if cached_user_objects['Username'] == member.get('username'):
                            print(f"CACHING CHECK SUCCESS. EMITTING... (SOCKET:{cached_user_objects['Socket_Id']})")
                            socketio.emit('new_conversation_add', {'conv_id':new_conversation_id}, to=cached_user_objects['Socket_Id'])
                return jsonify(data)
            except ValueError as error:
                print(error)
                
                return jsonify({
                    "success" : False, 
                    "Error" : str(error)
                })
            except Exception as error:
                return jsonify({
                    "success" : False, 
                    "Error" : str(error)
                })
            

#Dictionary needed to keep track of users in conversations in memory - Redis solution?
cached_users = []
socket_in_conversation = {}
#Creates socket connection
@socketio.on('connect')
def on_connect():
    print(f"WebSocket Connection Started By {request.sid}")

@socketio.on('cache_user')
def cache_user(username_data):
    cached_users.append({'Username' : username_data,
                        'Socket_Id' : request.sid
                         })
    print(f'Loaded cached username data: {cached_users}')

#Joins clients to live sockets, which run under the conversation IDs, based on clicked conversation preview
@socketio.on('current_conversation')
def current_conversation(data):
    socket_conversation_id = data
    socket_id = request.sid #Requests the ID of the client socket triggering this socket
    
    old_conv_id = socket_in_conversation.get(socket_id) #Creates the old conversation id if socket is in one
    if old_conv_id: #Leaves the socket's previous conversation and joins the new one when they switch conversations 
        print(f"{socket_id} LEFT CONVERSATION {old_conv_id}")
        leave_room(old_conv_id, sid=socket_id)
        old_conv_id = socket_conversation_id
        join_room(socket_conversation_id, sid=socket_id)
        print(f"CONVERSATION SWAPPED BY {socket_id} TO {old_conv_id}")
    #Joins live socket for the converastion the user clicks
    #Also puts in memory the socket ID and the conversation it is in, in the socket in conversation dictionary
    socket_in_conversation[socket_id] = socket_conversation_id
    join_room(socket_conversation_id, sid=socket_id)
    print(f"{socket_id }JOINED LIVE CONVERSATION SOCKET {socket_conversation_id}")

#Creates socket that handles posted messages
#Updates messages across any connected conversation users
@socketio.on('new_message')
def new_message(message_data):
     conversation_id = message_data['data']['parent_id']
     print("New Message posted!", message_data, conversation_id)
     emit('post_message', message_data, to=conversation_id, skip_sid=request.sid)

#Handles socket disconnection when users leave or reload the page
#Checks through all cached users for any matching socket IDs and closes their connection
@socketio.on('disconnect')
def handle_conversation_disconnect():
    for socket in cached_users:
        if socket['Socket_Id'] in request.sid:
            cached_users.remove(socket)
    print(f'DISCONNECT DETECTED. CLEARING USER DATA: \nFlask session: {session}\nCached Users: {cached_users}')
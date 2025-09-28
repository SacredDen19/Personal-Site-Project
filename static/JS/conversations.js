console.log("JS ran")

//Needed declarations and initializations
const socket = io()
const messagesContainer = document.getElementsByClassName('messages-container');
const messageCollection = messagesContainer[0].children; 
const previewsContainer = document.getElementsByClassName('conversations-preview');
const createConversationButton = document.getElementById('create-conversation-preview-button'); //Classes are arrays, so since the button is only item, we access the button at index 0

//Creates the box where users will type their message (used later)
const textBox = document.createElement('textarea'); 
textBox.classList.add('text-box');
textBox.setAttribute('id', 'user-text');
textBox.setAttribute('type', 'text');


/*
        ----------SOCKETS---------
*/
socket.on('connect', function() {
    const username =  usr.Username;
    console.log("Socket Connection Successful. Started by: ", socket.id, " With username: ", username);
    socket.emit('cache_user', username);
;})


if (socket.listeners('post_message').length > 0) {
    console.log('SOCKET OFF')
    socket.off('post_message'); //Meant to turn off any previous sockets
}   
//loads conversation for all users in the conversation
socket.on('post_message', function(data) {
    console.log("THIS IS DATA IN SOCKET POST: ", data);
    const e = 'click' //This is just a quick fix to prevent e is undefine in the function below
    loadConversations(e, data.data.parent_id);
    //renderMessages(data['message_text'], data['username']);
;})

socket.on('new_conversation_add', function (data) {
    console.log('New conversation detected. Have data: ', data);
    const conversation_preview = document.createElement('div');
    conversation_preview.classList.add('conversations-preview');
    conversation_preview.setAttribute('id', data.conv_id)
    conversation_preview.innerHTML = 'Convo id: ' + data.conv_id;
    document.querySelector('.conversations-containter').appendChild(conversation_preview);
    previewEventLoader();
});

/**
 * ------END OF SOCKET DECLARATIONS------
 */


/*-------------FUNCTION DEFINITIONS-------------*/ 
//This sets the scroll bar to the bottom when the conversations page loads
function scrollToBottom() {
    messagesContainer[0].scrollTop = messagesContainer[0].scrollHeight;
}

//This function will load the conversations based on the message tabs/previews in the left column
async function loadConversations(e, conversation_identifier) { //This asynchronous function is needed to work with fetch()
    try {
        let conversationID;
        console.log(conversation_identifier);
        if (conversation_identifier !== undefined) {
            conversationID = conversation_identifier; //gets id from element that fired the event
        } else {
            conversationID = e.target.id;
        } 
        //emits the conversation element ID (which correspond to conversation ID) to current_conversation socket
        socket.emit('current_conversation', conversationID); 
        //headers is used to differentiate when users are navigating by URL or by our defined fetch API event in the backend
        const response = await fetch(`/conversations/${conversationID}`, {
            headers: {
                "Requested-By": "Fetch"
            }
        }) //Creates a request to the backend route
        history.pushState({ conversationID} , '', `/conversations/${conversationID}`); //Changes the url without reloading the page
        const data = await response.json();

        //Interates through messageCollection (messages-container) in order the clear the previous conversation
        for (i=0; i < messageCollection.length;i++) {
            messagesContainer[i].innerHTML = ''; //Clears any messages-container the previous conversation
        }

        let current_user = data.username[0]; //Sets the user making the request/responses
        //Lazy fix --- Sets the current conversation ID for use in other functions
        global_id = conversationID;
        userName = current_user;

        for (i=0; i < data.messages.length; i++) {
            //constant declarations
            const message = data.messages[i]; //Selects individual message object

            renderMessages(message.message_text, message.username);
        }
    //Adds the textbox to the end of messages-container so it doesn't mess with the message box divs
    messagesContainer[0].appendChild(textBox);
    textBoxIndex = messageCollection[messageCollection.length-1];
    textBoxEvent(textBoxIndex);

    //debugging area
        //console.log(data);
    } catch (err) {
        console.error("Error", err);
    }
    scrollToBottom();
} 

//END OF LOADCONVERSATION FUNCTION

async function postMessage(messageText, parent_id, user) {
    console.log("postMessage executed!", userName);
    const conversationID = parent_id;

    const messageData = {
        //Assigns the values we will be sending to the back end
        message_text: messageText,
        parent: parent_id,
        username :  user,
    };

    try {
        //This is a POST request meaning we have to manually set the response's method, header, and body content
        const response = await fetch(`/conversations/${conversationID}`, {
            method : "POST",
            headers : {"Content-Type": "application/json"},
            body : JSON.stringify(messageData) //Serializes messageData as a JSON String
    });
        const data = await response.json();
        console.log("THIS IS RESPONSE DATA: ", data);
        socket.emit('new_message', data);

        //const data = await response.json();
        //console.log("This is data from postMessage: ", data);
    } catch (err) {
        console.error("Error", err);
    }

}

//END OF POSTMESSAGE FUNCTION

function renderMessages(message, username) {
    //Local declarations
    const messageDiv = document.createElement('div');
    const usernameSpan = document.createElement('span');
    const messageTextSpan = document.createElement('span');

    //Class assignment
    messageDiv.classList.add('message');
    usernameSpan.classList.add('username');
    messageTextSpan.classList.add('text');
    
    if (userName != username) { //Checks if the user is the one that is logged in and assigns the correct message box class for styling
        messageDiv.classList.add('them');
    } else {
        messageDiv.classList.add('me');
    }
    //Adds the username and text data to the correct html element
    usernameSpan.innerHTML = username;
    messageTextSpan.innerHTML = message;
    //Adds the actual username and text elements to the message box
    messageDiv.appendChild(usernameSpan);
    messageDiv.appendChild(messageTextSpan);

    //Check if message collection exists or is empty
    if (messageCollection.length == undefined  || messageCollection.length == "0" ) {
        messagesContainer[0].appendChild(messageDiv);
    }   else {
        //console.log("Messages container 0: ", messagesContainer[0])
        messagesContainer[0].appendChild(messageDiv);
    }
}

//END OF RENDERMESSAGES FUNCTION

/**
 * -----START OF EVENT LISTENING FUNCTIONS------
 */

//Loads all available message previews
function previewEventLoader() {
    if (previewsContainer) { //checks if previews exists or loads
        for (let x=0; x < previewsContainer.length; x++) { //iterates through the previewsContainer HTML collection (Array)
            previewsContainer[x].removeEventListener("click", loadConversations); //Removes the event listener if it already exists to prevent duplicates
            previewsContainer[x].addEventListener("click", loadConversations); //adds event listener for click event in each previewsContainer

            console.log("Preview loaded!", previewsContainer[x]);
        }
    } else {
        console.log("previews not loaded");
    }
}

//END OF PREVIEW EVENT LOADER FUNCTION

//Checks to see if textBox has been created by fetchAPI
let boxHandler = null; //Avoids boxHandler not defined error when app first runs
function textBoxEvent(index) {
    let parent = global_id;
    let username = userName;

    if (boxHandler) {
    index.removeEventListener('keydown', boxHandler); //Prevents duplicate messaging by removing any existing eventlisteners
    }
    
    boxHandler = async function textBoxEventHandler(e) {
        if (e.key == 'Enter') {
            e.preventDefault(); //prevents cursor from going to next line when pressing enter (textarea quirk)
            console.log("Textbox generated! Index:", index);

            await postMessage(index.value, parent, username);

            //These need to be executed last
            index.value = ''; //Clears the value in text area

            //Loads all conversations this time by passing the actual parent_id, not based on element clicked
            await loadConversations(e, parent); 

            console.log("Enter event triggered!!!", index);
        } else {
        console.log("Textbox not loaded")
        }
    };

    index.addEventListener('keydown', boxHandler);
}

//END OF TEXT BOX EVENT FUNCTION
function closeElement(parent_element) {
    const closeButton = document.createElement('div');
    closeButton.classList.add('close-button');
    closeButton.innerHTML = 'CLOSE';
    parent_element.appendChild(closeButton);
    closeButton.addEventListener('click', function() {
        parent_element.remove()
    });
}
createConversationButton.addEventListener('click', function(){
    //Checks document for any existing dialogue boxes and does nothing if they exist to prevent duplicates
    //querySelector is used to check the document for any create conversation dialogue boxes with the class
    //conversation-create-box
    if (document.querySelector('.conversation-create-box')) {

    } else {
        const conversationCreateBox = document.createElement('div');
        conversationCreateBox.classList.add('conversation-create-box');

        const appendedConversationBox = document.getElementsByClassName('main-content')[0].appendChild(conversationCreateBox)
        
        const conversationTitle = document.createElement('label');
        const addUserLabel = document.createElement('label');
        const startConversation = document.createElement('div');
        const createConverationBoxElements = [conversationTitle, addUserLabel, startConversation];
        //Checks if the appended create box to the main content container has been created
        if (appendedConversationBox) {
            //Adds the close button to the create conversation box
            closeElement(appendedConversationBox);
            const conversationBoxContentContainer = appendedConversationBox.appendChild(document.createElement('div'));
            conversationBoxContentContainer.classList.add('conversation-box-content-container');
            //Appends the elements going on the create conversation box
            for (let x=0; x < createConverationBoxElements.length; x++) {
                conversationBoxContentContainer.appendChild(createConverationBoxElements[x]);
            }
            //Adds the information to its specific object within the container
            for (let x = 0; x < conversationBoxContentContainer.children.length; x++) {
                switch (x) {
                    case 0:
                        conversationBoxContentContainer.children[x].innerHTML = 'Enter conversation name: ';
                        conversationTitleInput = conversationBoxContentContainer.children[x].appendChild(document.createElement('input'));
                        conversationBoxContentContainer.children[x].classList.add('tybe-bar');
                        conversationTitleInput.setAttribute('placeholder', 'Conversation Title');
                        break;
                    case 1:
                        conversationBoxContentContainer.children[x].innerHTML = 'Add users to the conversation: ';
                        usernameOrIdInput = conversationBoxContentContainer.children[x].appendChild(document.createElement('input'));
                        conversationBoxContentContainer.children[x].classList.add('tybe-bar')
                        usernameOrIdInput.setAttribute('placeholder', 'Enter username or user ID');
                        break;
                    case 2:
                        conversationBoxContentContainer.children[x].innerHTML = 'Create Conversation';
                        conversationBoxContentContainer.children[x].classList.add('create-conversation-button');
                        break;
                    }
                }
            //Creates constants for the inner create conversation button
            const innerCreateConversationButton = document.getElementsByClassName('create-conversation-button')[0];
            innerCreateConversationButton.addEventListener('click', async function () {
                let title = conversationTitleInput.value;
                let userOrId = usernameOrIdInput.value;
                console.log(title, userOrId);
                //Checks if the error message exists already, and if it does, deletes it
                if (document.querySelector('.error-box')) {
                    document.querySelector('.error-box').remove();
                }
                try {
                    //This is a POST request meaning we have to manually set the response's method, header, and body content
                    const response = await fetch(`/conversations/create`, {
                        method : "POST",
                        headers : {"Content-Type": "application/json"},
                        body : JSON.stringify({'title': title, 'input': userOrId}) //Serializes both variables as a JSON String
                    });
                    conversationTitleInput.value = '';
                    usernameOrIdInput.value = '';
                    const data = await response.json();
                    console.log('create conversation data: ', data);
                    if (data.success == false) {
                        const conversationBoxContentContainer = document.querySelector('.conversation-box-content-container');
                        const ErrorBox = document.createElement('div');
                        ErrorBox.classList.add('error-box');
                        ErrorBox.innerText = data.Error;
                        conversationBoxContentContainer.insertBefore(ErrorBox, conversationBoxContentContainer.lastElementChild);
                    }
                } catch (err) {
                    console.error("Error", err);
                }

            });

        }
    }
});

//Listens for a page reload, navigation, or close in order to close the live
//conversation socket connection the client is using
window.addEventListener('pagehide', function() {
    const username =  usr.Username;
    console.log('Page unloaded!');
    socket.disconnect();
})


/*-----END OF EVENT LISTENING FUNCTIONS------*/

previewEventLoader();

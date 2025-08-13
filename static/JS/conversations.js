console.log("JS ran")

const messagesContainer = document.getElementsByClassName('messages-container');
const messageCollection = messagesContainer[0].children;
const previewsContainer = document.getElementsByClassName('conversations-preview');
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

        const response = await fetch(`/conversations/${conversationID}`) //Creates a request to the backend route
        history.pushState({ conversationID} , '', `/conversations/${conversationID}`); //Changes the url without reloading the page
        const data = await response.json();
        console.log("THIS IS DATA: ", data);
        //Interates through messageCollection (messages-container) in order the clear the previous conversation
        for (i=0; i < messageCollection.length;i++) {
            messagesContainer[i].innerHTML = ''; //Clears any messages-container the previous conversation
            //console.log("cleared Container: with ID of ",i,messagesContainer[i]);
        }

        //Creates the box where users will type their message
        let current_user = data.username[0];
        const textBox = document.createElement('textarea'); 
        textBox.classList.add('text-box');
        textBox.setAttribute('id', 'user-text');
        textBox.setAttribute('type', 'text');

        //For every message received, this creates a message box for it and dynamically changes the page to show it/them.
        for (i=0; i < data.messages.length; i++) {
            //constant declarations
            const message = data.messages[i];
            //console.log("data response message: ", message) prints the message text data objects
            const messageDiv = document.createElement('div');
            const usernameSpan = document.createElement('span');
            const messageTextSpan = document.createElement('span');

            //Class assignment
            messageDiv.classList.add('message');
            usernameSpan.classList.add('username');
            messageTextSpan.classList.add('text');
            console.log("Print current_user:", current_user, " and message.username: ", message.username);
            if (current_user != message.username) { //Checks if the user is the one that is logged in and assings the correct message box class for styling
                messageDiv.classList.add('them');
            } else {
                messageDiv.classList.add('me');
            }
            //Adds the username and text data to the correct html element
            usernameSpan.innerHTML = `${message.username}`;
            messageTextSpan.innerHTML = `${message.message_text}`;
            //Adds the actual username and text elements to the message box
            messageDiv.appendChild(usernameSpan);
            messageDiv.appendChild(messageTextSpan);

            //Lazy fix --- Sets the current conversation ID for use in other functions
            global_id = conversationID;
            userName = current_user;
            //Check if message collection exists or is empty
            if (messageCollection.length == undefined  || messageCollection.length == "0" ) {
                messagesContainer[0].appendChild(messageDiv);
            }   else {
                messagesContainer[0].appendChild(messageDiv);
            }
        }
    //Adds the textbox to the end of messages-container so it doesn't mess with the message box divs
    messagesContainer[0].appendChild(textBox);
    console.log("This is messagesContainer[lastIndex]: ", messageCollection[messageCollection.length-1]);
    textBoxIndex = messageCollection[messageCollection.length-1];
    textBoxEvent(textBoxIndex);



    //debugging area
        console.log(data);
    } catch (err) {
        console.error("Error", err);
    }
    scrollToBottom();
} //END OF loadconversation FUNCTION


async function postMessage(messageText, parent_id, usern) {
    console.log("postMessage executed!", userName);
    const conversationID = parent_id;

    const messageData = {
        //Assigns the values we will be sending to the back end
        message_text: messageText,
        parent: parent_id,
        username :  usern,
    };

    try {
        //This is a POST request meaning we have to manually set the response's method, header, and body content
        const response = await fetch(`/conversations/${conversationID}`, {
            method : "POST",
            headers : {"Content-Type": "application/json"},
            body : JSON.stringify(messageData) //Serializes messageData as a JSON String
    });

        //const data = await response.json();
        //console.log("This is data from postMessage: ", data);
    } catch (err) {
        console.error("Error", err);
    }
}



//Loads all available message previews
function previewEventLoader() {
    if (previewsContainer) { //checks if previews exists or loads
        for (let x=0; x < previewsContainer.length; x++) { //iterates through the previewsContainer HTML collection (Array)
            previewsContainer[x].addEventListener("click", function (e) { //adds event listener for click event in each previewsContainer

                loadConversations(e);
            });
            console.log("Preview loaded!", previewsContainer[x]);
        }
    } else {
        console.log("previews not loaded")
    }
}

//Checks to see if textBox has been created by fetchAPI
function textBoxEvent(index) {
    let parent = global_id;
    let usrN = userName;
    if (index) {
    
    index.addEventListener('keydown', async function(e) {
        if (e.key == 'Enter') {
            e.preventDefault(); //prevents cursor from going to next line when pressing enter (textarea quirk)
            console.log("Textbox generated! Index:", index);

            await postMessage(index.value, parent, usrN);

            //These need to be executed last
            index.value = ''; //Clears the value in text area

            await loadConversations(e, parent);

            previewEventLoader(); //Dynamically loads all conversation previews on the left and messages on the right
            console.log("Enter event triggered!!!", index);
        }
    });

    } else {
    console.log("Textbox not loaded")
    }
}



previewEventLoader();
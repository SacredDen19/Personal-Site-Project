console.log("JS ran")

const messagesContainer = document.getElementsByClassName('messages-container');
const messageCollection = messagesContainer[0].children;
const previewsContainer = document.getElementsByClassName('conversations-preview');
//This sets the scroll bar to the bottom when the conversations page loads
function scrollToBottom(index) {
    messagesContainer[index].scrollTop = messagesContainer[index].scrollHeight;
}


//This function will load the conversations based on the message tabs/previews in the left column
async function loadConversations(e) { //This asynchronous function is needed to work with fetch()
    try {
        //console.log("async worked")
        const conversationID = e.target.id; //gets id from element that fired the event
        console.log("Messages container: ", messagesContainer, "Message Container Children Collection: ",messageCollection);
        console.log("Target preview:", conversationID);
        
        const response = await fetch(`/conversations/${conversationID}`) //Creates a request to the backend route
        history.pushState({ conversationID} , '', `/conversations/${conversationID}`); //Changes the url without reloading the page
        const data = await response.json();

        //Interates through messageCollection (messages-container) in order the clear the previous conversation
        for (i=0; i < messageCollection.length;i++) {
            messagesContainer[i].innerHTML = ''; //Clears any messages-container the previous conversation
            console.log("cleared Container: with ID of ",i,messagesContainer[i]);
        }
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

            if (message.user == "user1") { //Checks if the user is the one that is logged in and assings the correct message box class for styling
                messageDiv.classList.add('them');
            } else {
                messageDiv.classList.add('me');
            }
            //Adds the username and text data to the correct html element
            usernameSpan.innerHTML = `${message.user}`;
            messageTextSpan.innerHTML = `${message.text}`;
            //Adds the actual username and text elements to the message box
            messageDiv.appendChild(usernameSpan);
            messageDiv.appendChild(messageTextSpan);
            //Adds the message text data to message box divs 
            console.log("conversation: ", conversationID);
            //Check if message collection exists or is empty
            if (messageCollection.length == undefined  || messageCollection.length == "0" ) {
                messagesContainer[0].appendChild(messageDiv);
            }   else {
                messagesContainer[0].appendChild(messageDiv);
            }
        }


        console.log(data);
    } catch (err) {
        console.error("Error", err);
    }
}

//window.onload = scrollToBottom;

if (previewsContainer) { //checks if previews exists or loads
    for (let x=0; x <= previewsContainer.length; x++) { //iterates through the previewsContainer HTML collection (Array)
        previewsContainer[x].addEventListener("click", function (e) { //listens for click event in previewsContainer

            loadConversations(e);
        });
        console.log("Preview loaded!", previewsContainer[x]);
    }
} else {
    console.log("previews not loaded")
}

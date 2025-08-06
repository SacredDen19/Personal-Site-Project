
//This sets the scroll bar to the bottom when the conversations page loads

function scrollToBottom() {
    const messagesContainer = document.getElementsByClassName('messages-container')[0];
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
window.onload = scrollToBottom;


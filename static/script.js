function setMessage(message) {

    const input = document.getElementById("message");

    if (input) {

        input.value = message;

        input.focus();

    }
}


const messages = document.getElementById("messages");

if (messages) {

    messages.scrollTop = messages.scrollHeight;

}
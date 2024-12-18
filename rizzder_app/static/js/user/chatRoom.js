$(document).ready(function() {
    const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/" + roomName + "/");
        chatSocket.onopen = function (e) {
            console.log("The connection was set up successfully!");
        };
        chatSocket.onclose = function (e) {
            console.log("Something unexpected happened!");
        };
        document.querySelector("#sendMessage").onclick = function (e) {
            chatSocket.send(JSON.stringify({
                message: document.getElementById("textMessage").value,
                userId: userId,
                time: Date.now()
            }));
        };
        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            console.log(data)
        };
});
$(document).ready(function() {
    const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/" + roomName + "/");
        chatSocket.onopen = function (e) {
            console.log("The connection was set up successfully!");
        };
        chatSocket.onclose = function (e) {
            console.log(e);
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
            // Check if the page is scrolled to the bottom
            const isScrolledToBottom = document.querySelector('.message-content').scrollHeight - document.querySelector('.message-content').clientHeight <= document.querySelector('.message-content').scrollTop + 1;

            fetch(window.location.href) // Request the current page
                    .then(response => response.text())  // Get the response as text (HTML)
                    .then(html => {
                        // Create a temporary container to hold the fetched content
                        const tempContainer = document.createElement('div');
                        tempContainer.innerHTML = html;

                        // Extract the new messages from the response
                        const newMessages = tempContainer.querySelector('.message-content');

                        // Only update the message container with new messages
                        if (newMessages) {
                            // Update the message content
                            document.querySelector('.message-content').innerHTML = newMessages.innerHTML;

                            // Scroll to the bottom if the page was already scrolled to the bottom
                            if (isScrolledToBottom) {
                                document.querySelector('.message-content').scrollTo(0, document.querySelector('.message-content').scrollHeight);
                            }
                        }
                    })
                    .catch(error => console.error('Error fetching new messages:', error));

            const data = JSON.parse(e.data);
            console.log(data)
        };
});

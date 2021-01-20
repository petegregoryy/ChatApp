# ChatApp
Simple Chat application between clients through a server

This is the python client and server repository, with releases of the server corresponding to the supported client versions.

Feel free to develop your own clients for this.  Currently the server supports 3 commands:

-USER: 
This should be the first command sent on connection, including the username for the client.

-DATA: 
Anything sent following a data command will be sent to all connected clients, including the client it was sent from.

-LIST: 
This lists the usernames of currently connected users.

A GUI client for Windows is available here: https://github.com/petegregoryy/ChatAppGUI

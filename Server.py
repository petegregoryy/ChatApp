import select, socket, sys
try:
    import Queue
except ImportError:
    import queue as Queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('', 65432))
server.listen(5)
print(f"listening")
inputs = [server]
clients = []
outputs = []
usernames = {}
message_queues = {}

usernames["server"] = "Server"

# Function to disconnect a client from the server and notify the other clients of their disconnection
def Disconnect(s):
    print("Peer disconnected")
    # Remove them from the client list
    clients.remove(s)
    # Close the socket connection
    s.close()
    # Remove them from inputs
    inputs.remove(s)
    # send the disconnect message to every client
    for client in clients:
        # Add the message to the output queue for the client
        message_queues[client].put(str.encode(usernames[s] + " left the chat."))
        # This bit is what actually sends it, adding them to the output queue starts the message sending
        if client not in outputs:
            outputs.append(client)
    print(f"Removing {usernames[s]} from usernames")
    # Remove the username and socket from the usernames dictionary
    usernames.pop(s)
    # Delete the assosiated queue
    del message_queues[s]

while inputs: # if there are inputs, run
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs) # set readable, writable and exceptional sockets with select
    for s in readable: # for every socket that is readable
        if s is server: # if the socket is a client
            connection, client_address = s.accept() # accept the connection, call it connection and set client_address as the address
            print(f"Accepted connection from {client_address}") 
            connection.setblocking(0) # Set blocking of the socket to off (I think)
            inputs.append(connection) # add the connection to the input list
            clients.append(connection) # Add it to the list of clients
            message_queues[connection] = Queue.Queue() # add the connection to the queue of messages
        else:
            try:
                data = s.recv(1024)  # Get client info
            except Exception: # If an exception, run the disconnection
                Disconnect(s)
            else:
                data_decoded = data.decode("utf-8") # Decode data
                print(f"recieved {data_decoded}") 
                print(data)
                if data_decoded != "":
                    if data_decoded[0:4] == "USER":
                        usernames[s] = data_decoded[4:] # add the username to the dictionary with the socket as a key
                        combinedlist = []
                        # create usernawmes list
                        for users in usernames:
                            combinedlist.append(usernames[users])
                        combined = '|'.join(combinedlist)
                        
                        # send the connection message and the usernames list to every client
                        for client in clients:

                            try:
                                if client != s:
                                    message_queues[client].put(str.encode(usernames[s] + " joined the chat!"))
                                message_queues[client].put(str.encode(f"250 LIST|{combined}"))
                                if client not in outputs:
                                    outputs.append(client)
                            except KeyError:
                                Disconnect(s)


                        print(usernames)
                        if s not in outputs:
                            outputs.append(s)

                    #If the command recieved is DATA echo the recieved message to every client
                    elif data_decoded[0:4] == "DATA":
                        print(clients)
                        for client in clients:
                            message_queues[client].put(str.encode(usernames[s] + ": " + data_decoded[4:]))
                            if client not in outputs:
                                outputs.append(client)
                        # message_queues[s].put(str.encode(data_decoded[4:]))
                        if s not in outputs:
                            outputs.append(s)
                    # If command is LIST send the list to the client that requested it
                    elif data_decoded[0:4] == "LIST":
                        combinedlist = []
                        for users in usernames:
                            combinedlist.append(usernames[users])
                        combined = '|'.join(combinedlist)
                        message_queues[s].put(str.encode(f"250 LIST|{combined}"))
                        if s not in outputs:
                            outputs.append(s)
                # Run the disconnect if nothing is recievec
                else:
                    Disconnect(s)
                    #if s in outputs:
                    #    outputs.remove(s)
                    #inputs.remove(s)
                    #for client in clients:
                    #    message_queues[client].put(str.encode(usernames[s] + " left the chat."))
                    #clients.remove(s)
                    #usernames.pop(s)

                    #s.close()
                    #del message_queues[s]
    # For every socket in writable try to send the messages in the sockets queue
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
            print(f"sending {next_msg}")
        # If the queue is empty remove the socket from the output list
        except Queue.Empty:
            outputs.remove(s)
        # otherwise send the next message
        else:
            s.send(next_msg)

    # Not sure what this does, but it needs to be there (I think its to do with error'd sockets)
    for s in exceptional:
        inputs.remove(s)
        clients.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]
import socket
from threading import Thread

_HOST = '0.0.0.0'
_PORT = 65432

global users
users = [""]
global clients
clients = []






def process_message(data, conn):
    string = data.decode("utf-8") # Decode reply
    command = string[0:4] # Get first 4 letters for command
    msg = string[4:] # Get rest of string
    # Print them
    print ("CMD: " + command) 
    print("MSG: " + msg)


    if command == "USER": # Check if the command was a USER command
        unique = True # Create Unique
        for user in users: # For each user in the users list check if it matches the message, if it does, the name isnt unique
            if user == msg:
                unique = False
                break
            else:
                unique = True
                
        if unique: # If the name is unique, append the username to the users list, print that and send an OK response
            users.append(msg)
            print(f"Adding {msg} to users list")
            print(users)
            conn.sendall(b"250 OK")
            print ("Sending 250 OK")
        else: # Otherwise, send a 550 to show an error
            conn.sendall(b'550 User duplicate')
            print ("Sending 550")
    elif command == "DATA": # If the command is DATA, send the message back to the user
        conn.sendall(str.encode(msg))
        print(clients)
        for client in clients:
            if client != conn:
                print(f"Sending {msg} to {client}")
                client.sendall(str.encode(msg))
        print (f"Sending {msg}")

def ProcessThread(s, socket, addr): # Function for controlling the connection with the socket
        print('Connection from ', addr)
        while True:
            print("Running Process")
            data = socket.recv(1024) # Receive data
            process_message(data,socket) # send the data and the socket to be processed

            if not data: # Quit if it doesn't receive data
                break
                # sock.sendall(data)
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((_HOST,_PORT)) # Bind socket and start listening
        s.listen()
        conn,address = s.accept() # When connection occurs, set conn and adress to the information of the connection
        clients.append(conn)
        thread1 = Thread(target=ProcessThread,args=(s,conn,address)) # create a thread using the conn and address information
        thread1.start()



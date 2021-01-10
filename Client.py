import socket
import threading

# _HOST = input("What server would you like to connect to: ")
# _PORT = input("What port is that server on: ")
_HOST = "127.0.0.1"
_PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   
    s.connect((_HOST,_PORT))                                      #Opens socket

    #Username 
    ValidInput=False
    while ValidInput==False:
        print("What username would you like to use?")
        USERNAME = input(">> ")
        sendline = "USER"+USERNAME
        s.send(str.encode(sendline))
        rData = s.recv(1024)

        reply = rData.decode("utf-8")
        cmd = reply[0:3]            #Formatting
        msg = reply[4:]
        print ("CMD: " + cmd)
        print("MSG: " + msg)
        if cmd == "250":            # checks if username is taken
            ValidInput=True
        elif cmd == "550":
            print("That username is already taken")


    #Message send/recieve
    while True:                 
        usr = input("> ") 
        sendString = "DATA" + usr           
        s.send(sendString.encode('utf-8'))      #Send
        data = s.recv(1024)

        print('Recieved' , repr(data))   #Recieve

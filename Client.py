import socket
import threading

# _HOST = input("What server would you like to connect to: ")
_HOST = "127.0.0.1"
_PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((_HOST,_PORT))
    while True:
        usr = input("> ")
        s.send(usr.encode('utf-8'))
        data = s.recv(1024)

        print('Recieved' , repr(data))
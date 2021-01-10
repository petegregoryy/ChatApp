import socket
import threading

_HOST = input("What server would you like to connect to: ")
_PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((_HOST,_PORT))
    s.sendall(b'Hello World')
    data = s.recv(1024)

print('Recieved' , repr(data))
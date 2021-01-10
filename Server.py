import socket
import threading

_HOST = '127.0.0.1'
_PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((_HOST,_PORT))
    s.listen()
    conn,addr = s.accept()
    with conn:
        print('Connection from ', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
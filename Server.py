import socket
import threading

_HOST = '127.0.0.1'
_PORT = 65432

users = []

def process_message(data):
    string = data.decode("utf-8")
    command = string[0:4]
    msg = string[4:]
    print ("CMD: " + command)
    print("MSG: " + msg)


    if command == "USER":
        unique = True
        for user in users:
            if user == msg:
                unique = False
            else:
                unique = True
                users.append(msg)
        if unique:
            conn.sendall(b"250 OK")
            print ("Sending 250 OK")
        else:
            conn.sendall(b'550 User duplicate')
            print ("Sending 550")
    elif command == "DATA":
        conn.sendall(str.encode(msg))
        print (f"Sending {msg}")

def ProcessThread(s, conn, addr):
        with conn:
            print('Connection from ', addr)
            while True:
                data = conn.recv(1024)
                process_message(data)

                if not data:
                    break
                # conn.sendall(data)
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((_HOST,_PORT))
        s.listen()
        conn,addr = s.accept()
        process = threading.Thread(target=ProcessThread, args=(s,conn,addr))
        process.start()



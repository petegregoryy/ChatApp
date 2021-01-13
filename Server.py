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

while inputs:
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs)
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            print(f"Accepted connection from {client_address}")
            connection.setblocking(0)
            inputs.append(connection)
            clients.append(connection)
            message_queues[connection] = Queue.Queue()
        else:
            try:
                data = s.recv(1024)
            except ConnectionResetError:
                print("Peer disconnected")
                clients.remove(s)
                s.close()
                inputs.remove(s)
                for client in clients:
                    message_queues[client].put(str.encode(usernames[s] + " left the chat."))
                    if client not in outputs:
                        outputs.append(client)
                del message_queues[s]
            else:
                data_decoded = data.decode("utf-8")
                print(f"recieved {data_decoded}")

                if data:
                    if data_decoded[0:4] == "USER":
                        message_queues[s].put(b"250 OK")
                        usernames[s] = data_decoded[4:]# message_queues[s].put(data)
                        for client in clients:
                            message_queues[client].put(str.encode(usernames[s] + " joined the chat!"))
                            if client not in outputs:
                                outputs.append(client)
                        print(usernames)
                        if s not in outputs:
                            outputs.append(s)

                    elif data_decoded[0:4] == "DATA":
                        print(clients)
                        for client in clients:
                            message_queues[client].put(str.encode(usernames[s] + ": " + data_decoded[4:]))
                            if client not in outputs:
                                outputs.append(client)
                        # message_queues[s].put(str.encode(data_decoded[4:]))
                        if s not in outputs:
                            outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
            print(f"sending {next_msg}")
        except Queue.Empty:
            outputs.remove(s)
        else:
            s.send(next_msg)

    for s in exceptional:
        inputs.remove(s)
        clients.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]
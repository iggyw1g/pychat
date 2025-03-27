import socket
import threading

def client_handle(client_socket, address):
    connected = True
    while connected:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[{address}] {message}")
            broadcast(message, client_socket)
        except:
            connected = False
        
    print(f"[DISCONNECTED] {address} disconnected")
    client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)

def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        client_socket, address = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=client_handle, args = (client_socket, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


SERVER = "127.0.0.1"
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

clients = []

print("[STARTING] Server is starting ...")
start_server()


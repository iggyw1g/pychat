import socket
import threading 

clients = {}  

def handle_client(client_socket, address):
    try:
        name = client_socket.recv(1024).decode('utf-8').strip()
        if not name:
            raise ValueError("Client didn't provide a name")
        clients[name] = client_socket
        broadcast(f"{name} joined the chat", exclude=client_socket)
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(f"{name}: {message}", exclude=client_socket)
            
    except Exception as e:
        print(f"Error with {name}: {e}")
    finally:
        if name in clients:
            del clients[name]
            broadcast(f"{name} left the chat")
        client_socket.close()

def broadcast(message, exclude=None):
    for name, sock in clients.items():
        if sock != exclude:
            try:
                sock.send(message.encode('utf-8'))
            except:
                del clients[name]  

def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


SERVER = "127.0.0.1"
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

print("[STARTING] Server is starting...")
start_server()
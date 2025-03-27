import socket
import threading

def recieve_messages():
    while True:
        try: 
            message = client.recv(1024).decode('utf-8')
            print(message)

        except:
            print("An error occured!")
            client.close()
            break

def send_message():
    while True:
        message = input("")
        client.send(message.encode('utf-8'))

SERVER = "127.0.0.1"
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

recieve_thread = threading.Thread(target = recieve_messages)
recieve_thread.start()

send_thread = threading.Thread(target = send_message)
send_thread.start()
import socket
import threading
import tkinter as tk
import random
from tkinter import scrolledtext, simpledialog, messagebox

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        
        
        self.server_ip = "127.0.0.1"
        self.server_port = 5050
        self.client_socket = None
        self.username = ""
        
       
        self.setup_gui()
        
       
        self.get_username()
    
    def setup_gui(self):
        self.chat_display = scrolledtext.ScrolledText(
            self.root, 
            state='disabled',
            wrap=tk.WORD,
            height=20,
            width=60
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
      
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(padx=10, pady=5, fill=tk.X)
        
        self.message_entry = tk.Entry(
            entry_frame,
            font=('Arial', 12)
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(
            entry_frame,
            text="Send",
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT, padx=5)
        
        # # Status bar
        # self.status_var = tk.StringVar()
        # self.status_var.set("Disconnected")
        # status_bar = tk.Label(
        #     self.root,
        #     textvariable=self.status_var,
        #     bd=1,
        #     relief=tk.SUNKEN,
        #     anchor=tk.W
        # )
        # status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def get_username(self):
        self.username = simpledialog.askstring(
            "Username",
            "Enter your username:",
            parent=self.root
        )
        
        if not self.username:
            #messagebox.showerror("Error", "Username is required")
            self.username = "unknown"
            #return
        
        self.connect_to_server()
    
    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            
            
            self.client_socket.send(self.username.encode('utf-8'))
            
            
            receive_thread = threading.Thread(
                target=self.receive_messages,
                daemon=True
            )
            receive_thread.start()
            
            #self.status_var.set(f"Connected as {self.username}")
            self.display_message("System", f"You have joined as {self.username}")
        
        except Exception as e:
            messagebox.showerror(
                "Connection Error",
                f"Cannot connect to server: {str(e)}"
            )
            self.root.destroy()
    
    def display_message(self, sender, message):
        self.chat_display.config(state='normal')
        
        if sender == "System":
            self.chat_display.tag_config('system', foreground='blue')
            self.chat_display.insert(tk.END, f"{sender}: ", 'system')
        elif sender == self.username:
            self.chat_display.tag_config('you', foreground='green')
            self.chat_display.insert(tk.END, f"You: ", 'you')
        else:
            self.chat_display.tag_config('others', foreground='black')
            self.chat_display.insert(tk.END, f"{sender}: ", 'others')
        
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.display_message(self.username, message)
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.display_message("System", f"Failed to send message: {str(e)}")
    
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                if ": " in message:
                    sender, msg = message.split(": ", 1)
                    self.display_message(sender, msg)
                else:
                    self.display_message("System", message)
            
            except ConnectionAbortedError:
                self.display_message("System", "Disconnected from server")
                break
            except Exception as e:
                self.display_message("System", f"Error: {str(e)}")
                break
        
        self.client_socket.close()
        #self.status_var.set("Disconnected")
        self.send_button.config(state='disabled')
        self.message_entry.config(state='disabled')
    
    def on_closing(self):
        if self.client_socket:
            self.client_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClientGUI(root)
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.mainloop()
# File: core/client.py

import socket
import threading

class Client:
    def __init__(self, username, room_id, on_receive):
        self.username = username
        self.room_id = room_id
        self.on_receive = on_receive
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 5000))
        self.send_message(f"{username} has joined the room {room_id}.")
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, msg):
        self.socket.sendall(msg.encode('utf-8'))

    def send_alert(self, alert_msg):
        self.send_message(f"[ALERT] {alert_msg}")

    def send_file(self, path, file_type):
        self.send_message(f"[FILE:{file_type}] {self.username}: {path}")

    def receive_messages(self):
        while True:
            try:
                msg = self.socket.recv(1024).decode('utf-8')
                self.on_receive(msg)
            except:
                break

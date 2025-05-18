# File: core/server.py

import socket
import threading

clients = []

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg, client)
        except:
            clients.remove(client)
            break

def broadcast(msg, current_client):
    for client in clients:
        if client != current_client:
            try:
                client.send(msg)
            except:
                clients.remove(client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen()
    print("[SERVER STARTED] Listening on port 5000...")

    while True:
        client, addr = server.accept()
        print(f"[NEW CONNECTION] {addr}")
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

if __name__ == '__main__':
    start_server()

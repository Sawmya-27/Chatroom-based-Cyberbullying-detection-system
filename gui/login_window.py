# File: gui/login_window.py

# File: gui/login_window.py

import tkinter as tk
from tkinter import messagebox
from gui.chatroom import Chatroom

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - SAFE CHAT")
        self.root.configure(bg="#f2f2f2")
        self.root.geometry("300x200")

        tk.Label(root, text="Username:", bg="#f2f2f2", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(root, font=("Arial", 11))
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Room ID:", bg="#f2f2f2", font=("Arial", 12)).pack(pady=5)
        self.room_entry = tk.Entry(root, font=("Arial", 11))
        self.room_entry.pack(pady=5)

        tk.Button(root, text="Join Room", command=self.join_room, font=("Arial", 11), bg="#4CAF50", fg="white").pack(pady=10)

    def join_room(self):
        username = self.username_entry.get()
        room_id = self.room_entry.get()
        if not username or not room_id:
            messagebox.showerror("Error", "Please enter both username and room ID")
            return

        self.root.destroy()
        new_root = tk.Tk()
        Chatroom(new_root, username, room_id)
        new_root.mainloop()

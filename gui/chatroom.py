# File: gui/chatroom.py

# File: gui/chatroom.py

# File: gui/chatroom.py

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import speech_recognition as sr
import pyttsx3

from core.client import Client
from utils.file_utils import is_bullying_content, is_bullying_text

class Chatroom:
    def __init__(self, root, username, room_id):
        self.root = root
        self.root.title(f"Room: {room_id} | User: {username}")

        self.engine = pyttsx3.init()
        self.client = Client(username, room_id, self.display_message)

        self.chat_log = tk.Text(root, state='disabled', height=20, width=60, bg="#ffffff", font=("Helvetica", 11))
        self.chat_log.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(root, width=50, font=("Helvetica", 11))
        self.message_entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        tk.Button(root, text="Send", command=self.send_text, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(root, text="Speak", command=self.voice_to_text, bg="#2196F3", fg="white", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(root, text="Send Image", command=self.send_image, bg="#FF9800", fg="white", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(root, text="Send Text File", command=self.send_text_file, bg="#9C27B0", fg="white", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)

        self.last_image = None
        self.image_cache = {}

    def display_message(self, msg):
        self.chat_log.configure(state='normal')

        if msg.startswith("[FILE:image] "):
            parts = msg.split(" ", 2)
            if len(parts) == 3:
                username, path = parts[1][:-1], parts[2]
                try:
                    img = Image.open(path).resize((100, 100))
                    img_tk = ImageTk.PhotoImage(img)
                    self.chat_log.image_create(tk.END, image=img_tk)
                    self.chat_log.insert(tk.END, f"\n{username} sent an image.\n\n")
                    self.image_cache[path] = img_tk
                except Exception as e:
                    messagebox.showerror("Image Error", f"Failed to display image: {e}")
        else:
            self.chat_log.insert(tk.END, msg + '  ')
            if ':' in msg:
                speaker_button = tk.Button(self.chat_log, text="🔊", command=lambda m=msg: self.speak_message(m))
                self.chat_log.window_create(tk.END, window=speaker_button)
            self.chat_log.insert(tk.END, '\n\n')

        self.chat_log.configure(state='disabled')

    def speak_message(self, msg):
        self.engine.say(msg)
        self.engine.runAndWait()

    def send_text(self):
        msg = self.message_entry.get()
        if msg:
            if is_bullying_text(msg):
                messagebox.showwarning("Warning", "Behave properly.. Don't chat abusively!!")
                self.chat_log.configure(state='normal')
                self.chat_log.insert(tk.END, f"⚠️ A bullying message was blocked from {self.client.username}.\n\n")
                self.chat_log.configure(state='disabled')
                self.client.send_alert(f"A bullying message was blocked from {self.client.username}.")
            else:
                formatted = f"{self.client.username}: {msg}"
                self.client.send_message(formatted)
                self.display_message(formatted)
                self.message_entry.delete(0, tk.END)


    def send_text_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if is_bullying_text(content):
                        messagebox.showwarning("Warning", "Behave properly.. Don't chat abusively!!")
                        self.chat_log.configure(state='normal')
                        self.chat_log.insert(tk.END, f"⚠️ A bullying message was blocked from {self.client.username}.\n\n")
                        self.chat_log.configure(state='disabled')
                        self.client.send_alert(f"A bullying message was blocked from {self.client.username}.")
                    else:
                        formatted = f"{self.client.username}: {content}"
                        self.client.send_message(formatted)
                        self.display_message(formatted)
            except Exception as e:
                messagebox.showerror("File Error", f"Failed to read file: {e}")

    def voice_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                messagebox.showinfo("Listening", "Please speak now...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language='en-IN')
                self.message_entry.insert(tk.END, text)
                self.send_text()  # Automatically send after recognition
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Sorry, could not understand your voice.")
            except sr.RequestError:
                messagebox.showerror("Error", "Speech recognition service error.")
            except Exception as e:
                messagebox.showerror("Error", str(e))


    def send_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
        if path:
            bullying = is_bullying_content(path, 'image')
            if bullying:
                self.chat_log.configure(state='normal')
                self.chat_log.insert(tk.END, f"⚠️ A bullying image was detected and blocked from {self.client.username}.\n\n")
                self.chat_log.configure(state='disabled')
                self.client.send_alert(f"A bullying image was blocked from {self.client.username}.")
            else:
                self.client.send_file(path, 'image')
                try:
                    img = Image.open(path).resize((100, 100))
                    img_tk = ImageTk.PhotoImage(img)
                    self.chat_log.configure(state='normal')
                    self.chat_log.image_create(tk.END, image=img_tk)
                    self.chat_log.insert(tk.END, f"\n{self.client.username} sent an image.\n\n")
                    self.chat_log.configure(state='disabled')
                    self.image_cache[path] = img_tk
                except Exception as e:
                    messagebox.showerror("Image Error", f"Failed to display image: {e}")

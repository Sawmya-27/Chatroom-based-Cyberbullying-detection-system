# File: main.py
# Entry point to start the application

from gui.login_window import LoginWindow

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

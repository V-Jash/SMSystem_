import tkinter as tk
import json
from tkinter import messagebox, simpledialog
import os
import hashlib

CRED_FILE = "credentials.json"


def hashPassword(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def ensure_default_credentials():
    if not os.path.exists(CRED_FILE):
        creds = {"admin": hashPassword("admin")}
        with open(CRED_FILE, "w") as f:  # lowercase "w"
            json.dump(creds, f)


def load_credentials():
    with open(CRED_FILE, "r") as f:
        return json.load(f)


def save_credentials(creds):
    with open(CRED_FILE, "w") as f:
        json.dump(creds, f)


def add_user(username, password) -> bool:
    username = username.strip()
    if not username or not password:
        return False
    creds = load_credentials()

    if username in creds:
        return False
    creds[username] = hashPassword(password)   # FIXED: wrong assignment
    save_credentials(creds)
    return True


class LoginPage:

    def __init__(self, master):
        self.master = master
        master.title('LoginPage')
        master.geometry('300x200')
        master.resizable(False, False)

        tk.Label(master, text='Username:').grid(
            row=0, column=0, padx=8, pady=8, sticky='e')
        self.username = tk.StringVar()
        tk.Entry(master, textvariable=self.username).grid(
            row=0, column=1, padx=8, pady=8)

        tk.Label(master, text='Password:').grid(
            row=1, column=0, padx=8, pady=8, sticky='e')
        self.password = tk.StringVar()
        tk.Entry(master, textvariable=self.password,
                 show='*').grid(row=1, column=1, padx=8, pady=8)

        tk.Button(master, text='Login', command=self.login).grid(
            row=2, column=0, pady=10)
        tk.Button(master, text='Register', command=self.register).grid(
            row=2, column=1, pady=10)
        tk.Button(master, text='Exit', command=master.quit).grid(
            row=3, column=0, columnspan=2, pady=10)

    def login(self):
        user = self.username.get().strip()
        pwd = self.password.get()

        creds = load_credentials()
        if user and user in creds and creds[user] == hashPassword(pwd):
            messagebox.showinfo(
                "Code 1", f"{user} logged in Successfully !!!")
            self.reset()
        else:
            messagebox.showerror(
                "Code 0", "Incorrect Username or Password")
            self.reset()

    def register(self):
        new_usr = simpledialog.askstring(
            'Registration', "Enter the username :", parent=self.master)
        if not new_usr:
            return
        new_pwd = simpledialog.askstring(
            'Registration', "Enter the password :", parent=self.master, show="*")

        if add_user(new_usr, new_pwd):
            messagebox.showinfo(
                "R Code 1", f'{new_usr} registered successfully !!!')
        else:
            messagebox.showerror(
                "R Code 0", "Username exists or Invalid input")

    def reset(self):
        self.username.set("")
        self.password.set("")   # FIXED (was repeating username)


if __name__ == "__main__":
    ensure_default_credentials()
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()

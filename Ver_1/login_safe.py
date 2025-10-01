# login_safe.py
"""
Improved login example for beginners.

Features:
- credentials.json file with username -> sha256(password) mapping
- create default admin/admin if file missing
- Login window (Tkinter) with Login, Reset, Exit, Register buttons
- Register opens small dialog to add new users
- On successful login: hides login window and opens Toplevel Menu
- When Menu closes, login window is restored
- Lockout after 3 failed attempts (disables Login button for 10s)
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import hashlib
import os

CRED_FILE = "credentials.json"
LOCKOUT_SECONDS = 10
MAX_ATTEMPTS = 3


def hash_password(password: str) -> str:
    """Return SHA-256 hex digest of a password string."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def ensure_default_credentials():
    """Create credentials.json with default admin/admin if missing."""
    if not os.path.exists(CRED_FILE):
        creds = {"admin": hash_password("admin")}
        with open(CRED_FILE, "w") as f:
            json.dump(creds, f)


def load_creds() -> dict:
    """Load and return credentials dict. Returns empty dict on failure."""
    try:
        with open(CRED_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_creds(creds: dict):
    """Save credentials dict to file."""
    with open(CRED_FILE, "w") as f:
        json.dump(creds, f)


def add_user(username: str, password: str) -> bool:
    """
    Add a new user to credentials file.
    Returns True on success, False if user exists or input invalid.
    """
    username = username.strip()
    if not username or not password:
        return False
    creds = load_creds()
    if username in creds:
        return False
    creds[username] = hash_password(password)
    save_creds(creds)
    return True


class LoginApp:
    def __init__(self, master):
        ensure_default_credentials()
        self.master = master
        self.master.title("Login")
        self.master.resizable(False, False)

        # Track failed attempts
        self.failed_attempts = 0

        # UI widgets
        tk.Label(master, text="Username:").grid(
            row=0, column=0, padx=8, pady=8, sticky="e")
        tk.Label(master, text="Password:").grid(
            row=1, column=0, padx=8, pady=8, sticky="e")

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        tk.Entry(master, textvariable=self.username).grid(
            row=0, column=1, padx=8, pady=8)
        tk.Entry(master, textvariable=self.password,
                 show="*").grid(row=1, column=1, padx=8, pady=8)

        # Buttons row
        self.login_btn = tk.Button(
            master, text="Login", width=10, command=self.login)
        self.login_btn.grid(row=2, column=0, pady=10, padx=6)

        tk.Button(master, text="Reset", width=10, command=self.reset).grid(
            row=2, column=1, pady=10, padx=6)
        tk.Button(master, text="Exit", width=10, command=master.quit).grid(
            row=2, column=2, pady=10, padx=6)

        # Extra: Register button to add new user
        tk.Button(master, text="Register", width=10, command=self.open_register_dialog).grid(
            row=3, column=0, columnspan=3, pady=(0, 10)
        )

        # Status label
        self.status = tk.Label(master, text="", fg="red")
        self.status.grid(row=4, column=0, columnspan=3)

    def login(self):
        user = self.username.get().strip()
        pwd = self.password.get()
        creds = load_creds()

        if user and user in creds and creds[user] == hash_password(pwd):
            self.failed_attempts = 0
            self.status.config(text="")
            messagebox.showinfo("Welcome", f"Hello {user} — logging you in.")
            self.open_menu()
        else:
            self.failed_attempts += 1
            remaining = max(0, MAX_ATTEMPTS - self.failed_attempts)
            self.status.config(
                text=f"Login failed. Attempts left: {remaining}")
            messagebox.showerror("Error", "Invalid username or password")
            if self.failed_attempts >= MAX_ATTEMPTS:
                self.lockout()

    def lockout(self):
        """Disable login button for LOCKOUT_SECONDS then re-enable."""
        self.login_btn.config(state="disabled")
        self.status.config(
            text=f"Too many attempts. Try again in {LOCKOUT_SECONDS} seconds.")
        # Schedule re-enable
        self.master.after(LOCKOUT_SECONDS * 1000, self.end_lockout)

    def end_lockout(self):
        self.reset()
        self.failed_attempts = 0
        self.login_btn.config(state="normal")

        self.status.config(text="")

    def reset(self):
        self.username.set("")
        self.password.set("")
        self.status.config(text="")

    def open_register_dialog(self):
        """Open small dialogs to register a new user."""
        dialog = RegisterDialog(self.master)
        # RegisterDialog handles actual creation and shows results.

    def open_menu(self):

        # Hide login
        self.master.withdraw()

        # Create menu window
        menu = tk.Toplevel(self.master)
        menu.title("Menu")
        menu.geometry("320x180")
        menu.resizable(False, False)

        tk.Label(
            menu, text="This is the Menu.\nReplace this with your Menu module.", pady=10).pack()

        # Define what should happen when menu closes
        def on_close():
            menu.destroy()
            self.master.deiconify()   # ✅ show login again
            self.reset()              # clear login fields

        # Buttons that properly restore login
        tk.Button(menu, text="Close Menu", command=on_close).pack(pady=10)
        tk.Button(menu, text="Logout (return to login)",
                  command=on_close).pack(pady=4)

        # Handle window close (X button)
        menu.protocol("WM_DELETE_WINDOW", on_close)


class RegisterDialog:
    """Simple registration dialog using Toplevel + simpledialog for input validation."""

    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Register New User")
        self.dialog.resizable(False, False)
        tk.Label(self.dialog, text="Enter new username:").grid(
            row=0, column=0, padx=8, pady=8)
        tk.Label(self.dialog, text="Enter password:").grid(
            row=1, column=0, padx=8, pady=8)
        tk.Label(self.dialog, text="Confirm password:").grid(
            row=2, column=0, padx=8, pady=8)

        self.u_var = tk.StringVar()
        self.p_var = tk.StringVar()
        self.c_var = tk.StringVar()

        tk.Entry(self.dialog, textvariable=self.u_var).grid(
            row=0, column=1, padx=8, pady=8)
        tk.Entry(self.dialog, textvariable=self.p_var,
                 show="*").grid(row=1, column=1, padx=8, pady=8)
        tk.Entry(self.dialog, textvariable=self.c_var,
                 show="*").grid(row=2, column=1, padx=8, pady=8)

        tk.Button(self.dialog, text="Create", command=self.create_user).grid(
            row=3, column=0, pady=10, padx=8)
        tk.Button(self.dialog, text="Cancel", command=self.dialog.destroy).grid(
            row=3, column=1, pady=10, padx=8)

    def create_user(self):
        username = self.u_var.get().strip()
        pwd = self.p_var.get()
        confirm = self.c_var.get()

        if not username:
            messagebox.showwarning("Input error", "Username cannot be empty.")
            return
        if not pwd:
            messagebox.showwarning("Input error", "Password cannot be empty.")
            return
        if pwd != confirm:
            messagebox.showwarning("Input error", "Passwords do not match.")
            return

        if add_user(username, pwd):
            messagebox.showinfo(
                "Success", f"User '{username}' created. You can now log in.")
            self.dialog.destroy()
        else:
            messagebox.showerror(
                "Error", f"User '{username}' already exists or invalid input.")


if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()

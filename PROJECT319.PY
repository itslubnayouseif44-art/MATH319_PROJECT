import tkinter
from tkinter import messagebox
from tkinter import filedialog
import hashlib
import os

USERS_FILE = "user.txt"

def registration(username, password):
    if not username or not password:
        messagebox.showerror("Error", "You Must Complete All Required Information")
        return
    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    with open(USERS_FILE, "a") as user:
        user.write(username + "," + hashed_pass + "\n")
    messagebox.showinfo("Success", "Registration Completed!")

def authentication(username, password):
    if not os.path.exists(USERS_FILE):
        messagebox.showerror("Error", "No Users Registered Yet!")
        return False

    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    with open(USERS_FILE, "r") as user:
        for line in user:
            stored_username, stored_hashed_pass = line.strip().split(",")
            if username == stored_username and hashed_pass == stored_hashed_pass:
                return True
    return False

# ----------------- نافذة تسجيل الدخول -----------------
def login_window():

    def login_action():
        username = entry_user.get()
        password = entry_pass.get()
        if authentication(username, password):
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            login.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def open_register():
        register_window()

    login = tkinter.Tk()
    login.title("Secure File Storage - Login")
    login.geometry("300x200")

    tkinter.Label(login, text="Username:").pack(pady=5)
    entry_user = tkinter.Entry(login)
    entry_user.pack()

    tkinter.Label(login, text="Password:").pack(pady=5)
    entry_pass = tkinter.Entry(login, show="*")
    entry_pass.pack()

    tkinter.Button(login, text="Login", command=login_action).pack(pady=10)
    tkinter.Button(login, text="Register", command=open_register).pack(pady=5)

    login.mainloop()

def register_window():
    def register_action():
        username = entry_user.get()
        password = entry_pass.get()
        registration(username, password)

    register_win = tkinter.Toplevel()

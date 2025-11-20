import tkinter 
from tkinter import filedialog, messagebox
import hashlib
#________________________FUNCTIONS______________________________

USERS_FILE="user.text"
def registration(username,password):
    if not username or not password:
     messagebox.showerror("Error","You Must Complete All Required Information")
    return
    hashed_pass=hashlib.sha256(password.encode()).hexdigest()
    with open(USERS_FILE,"a")as user
    user.write(username+","+hashed_pass+"\n")
    messagebox.showinfo("Success","Registration Completed!")
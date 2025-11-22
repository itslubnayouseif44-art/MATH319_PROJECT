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

def Authentication(usename,password):
   if not os.path.exists(USERS_FILE):
      messagebox.showerror("Error","No Users Registered Yet!")
      return False
   
    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    with open(USERS_FILE,"r") as user:
        for line in user:
            stored_username,stored_hashed_pass=line.strip().split(",")
            hashed_pass=hashlib.sha256(password.encode()).hexdigest()
            if usename==stored_username and hashed_pass==stored_hashed_pass:
                messagebox.showinfo("Success","Login Successful!")
                return true 
    return         

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

def Authentication(username, password):
    if not os.path.exists(USERS_FILE):
        messagebox.showerror("Error", "No Users Registered Yet!")
        return False

    hashed_pass = hashlib.sha256(password.encode()).hexdigest()

    with open(USERS_FILE, "r") as user:
        for line in user:
            stored_username, stored_hashed_pass = line.strip().split(",")

            if username == stored_username and hashed_pass == stored_hashed_pass:
                messagebox.showinfo("Success", "Login Successful!")
                return True
    messagebox.showerror("Error", "Invalid username or password!")
    return False
 

def login_window():

    def login_action():
        username = entry_user.get()
        password = entry_pass.get()

        if Authentication(username, password):
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
         # WE HAVE TO CALL FUNCTION THT HAS MAIN PROGRAM
            login.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def open_register();
     register_window()

    login = tkinter.Tk()
    login.title("Secure File Storage - Login")

    tkinter.Label(login, text="Username:").pack(pady=5)
    entry_user = tkinter.Entry(login)
    entry_user.pack()

    tkinter.Label(login, text="Password:").pack(pady=5)
    entry_pass = tkinter.Entry(login, show="*")
    entry_pass.pack()
   
    tkinter.Button(login, text="Login", command=login_action).pack(pady=10)
    tk.Button(login, text="Register", command=open_register).pack(pady=5)
    login.mainloop()    

def Register_window():
   def Register_action():
      username=entry_yser.get()
      password=entry_pass.get()
      registration(username,password)

    register_win=tkinter.Toplevel()
    register_win.title("Secure File Storage - Register")
    register_win.geometry("300x200")
   
   tkinter.lable(register_win,text="Username:").pack(pady=5)
   entry_user=tkinter.Entry(register_win)
    entry_user.pack()
   
   tkinter.label(register_win,title="password:").pack(pady=5)
    entry_pass=tkinter.Entry(register_win,show="*")    
   enter_pass.pack()

tkinter.button(register_win,text="Register",command=Register_action).pack(pady=5)
    register_win.mainloop()


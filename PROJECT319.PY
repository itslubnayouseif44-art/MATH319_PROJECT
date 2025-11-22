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
         # HERE REGISTER FUNCTION  HAS TO BE CALLING HERE 
    login = tk.Tk()
    login.title("Secure File Storage - Login")
    login.geometry("300x200")

    tk.Label(login, text="Username:").pack(pady=5)
    entry_user = tk.Entry(login)
    entry_user.pack()

    tk.Label(login, text="Password:").pack(pady=5)
    entry_pass = tk.Entry(login, show="*")
    entry_pass.pack()

    tk.Button(login, text="Login", command=login_action).pack(pady=10)
    tk.Button(login, text="Register", command=open_register).pack(pady=5)
    login.mainloop()    


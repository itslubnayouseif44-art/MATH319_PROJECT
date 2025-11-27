import tkinter
from tkinter import messagebox, filedialog, simpledialog
import hashlib
import os
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

USERS_FILE = "user.text"

# _____________________________________ User Interface_______________________________________

# DASHBOARD WINDOW 
def dashboard_window(username, parent_root):
    
    dash = tkinter.Toplevel(parent_root)
    dash.title(f"Secure File Storage - {username}")
    dash.geometry("350x250")
    dash.resizable(False, False)
    dash.configure(bg="#FFF8EF")

    tkinter.Label(dash, text=f"Welcome, {username}", font=("Arial", 14, "bold"), bg="#FFF8EF").pack(pady=15)

    button_frame = tkinter.Frame(dash, bg="#FFF8EF")
    button_frame.pack(pady=20)

    tkinter.Button(button_frame, text="Encrypt File 🔒", width=20,
                   command=encrypt_file, bg="#F4165C", fg="white",
                   font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)

    tkinter.Button(button_frame, text="Decrypt File 🔓", width=20,
                   command=decrypt_file, bg="#F4165C", fg="white",
                   font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)

    def logout_action():
       
        parent_root.deiconify()

    tkinter.Button(dash, text="Logout", width=12, command=logout_action,
                   bg="#96d4af", fg="white", font=("Arial", 11)).pack(pady=5)

    def on_close():
        dash.destroy()
        parent_root.deiconify()

    dash.protocol("WM_DELETE_WINDOW", on_close)

# LOGIN WINDOW 
def login_window():
    def login_action():
        username = entry_user.get()
        password = entry_pass.get()
        if authentication(username, password):
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
           
            login.withdraw()
            
            dashboard_window(username, login)
        else:
            messagebox.showwarning("Login Failed", "Incorrect username or password.")

    def open_register():
        register_window(login)

    login = tkinter.Tk()
    login.title("Secure File Storage - Login")
    login.geometry("350x250")
    login.configure(bg="#FFF8EF")

    tkinter.Label(login, text="Login", font=("Arial", 16, "bold"), bg="#FFF8EF").pack(pady=10)

    form_frame = tkinter.Frame(login, bg="#FFF8EF")
    form_frame.pack(pady=10)

    tkinter.Label(form_frame, text="Username:", font=("Arial", 12), bg="#FFF8EF").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_user = tkinter.Entry(form_frame, font=("Arial", 12))
    entry_user.grid(row=0, column=1, padx=5, pady=5)

    tkinter.Label(form_frame, text="Password:", font=("Arial", 12), bg="#FFF8EF").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_pass = tkinter.Entry(form_frame, show="*", font=("Arial", 12))
    entry_pass.grid(row=1, column=1, padx=5, pady=5)

    button_frame = tkinter.Frame(login, bg="#FFF8EF")
    button_frame.pack(pady=15)

    tkinter.Button(button_frame, text="Login", width=12, command=login_action,
                   bg="#F4165C", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10)

    tkinter.Button(button_frame, text="Register", width=12, command=open_register,
                   bg="#F4165C", fg="white", font=("Arial", 12)).grid(row=0, column=1, padx=10)

      
    def on_root_close():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            login.destroy()

    login.protocol("WM_DELETE_WINDOW", on_root_close)
    login.mainloop()

# REGISTRATION WINDOW 
def register_window(parent_root):
    def register_action():
        username = entry_user.get()
        password = entry_pass.get()
        registration(username, password)
        if username and password:
          register_win.destroy()
          parent_root.withdraw()       
          dashboard_window(username, parent_root)



    register_win = tkinter.Toplevel()
    register_win.title("Secure File Storage - Register")
    register_win.geometry("350x250")
    register_win.resizable(False, False)
    register_win.configure(bg="#FFF8EF")

    tkinter.Label(register_win, text="Register", font=("Arial", 16, "bold"), bg="#FFF8EF").pack(pady=10)

    form_frame = tkinter.Frame(register_win, bg="#FFF8EF")
    form_frame.pack(pady=10)

    tkinter.Label(form_frame, text="Username:", font=("Arial", 12), bg="#FFF8EF").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_user = tkinter.Entry(form_frame, font=("Arial", 12))
    entry_user.grid(row=0, column=1, padx=5, pady=5)

    tkinter.Label(form_frame, text="Password:", font=("Arial", 12), bg="#FFF8EF").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_pass = tkinter.Entry(form_frame, show="*", font=("Arial", 12))
    entry_pass.grid(row=1, column=1, padx=5, pady=5)

    tkinter.Button(register_win, text="Register", width=15, command=register_action,
                   bg="#F4165C", fg="white", font=("Arial", 12)).pack(pady=15)

 
# _____________________________________ User Authentication _______________________________________


#  USER REGISTRATION
def registration(username, password):
    if not username or not password:
        messagebox.showerror("Error", "You must complete all required information!")
        return

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as user_file:
            for line in user_file:
                stored_username, _ = line.strip().split(",")
                if username == stored_username:
                    messagebox.showerror("Error", "Username already exists!")
                    return

    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    with open(USERS_FILE, "a") as user:
        user.write(username + "," + hashed_pass + "\n")
    messagebox.showinfo("Success", "Registration Successful!")

#  USER AUTHENTICATION 
def authentication(username, password):
    if not os.path.exists(USERS_FILE):
        messagebox.showerror("Error", "No users registered yet!")
        return False

    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    with open(USERS_FILE, "r") as user:
        for line in user:
            stored_username, stored_hashed_pass = line.strip().split(",")
            if username == stored_username and hashed_pass == stored_hashed_pass:
                return True
    return False

# _____________________________________ File Upload _______________________________________

# ENCRYPT FILE 
def encrypt_file():
    input_File = filedialog.askopenfilename(title="Select File to Encrypt")
    if input_File:
        password = simpledialog.askstring("Password", "Enter password for encryption:", show='*')
        if password:
            output_File = input_File + ".enc"
            encryption(input_File, output_File, password)
            messagebox.showinfo("Success", f"File encrypted successfully!\n{output_File}")
        else:
            messagebox.showerror("Error", "Password is required for encryption!")
    else:
        messagebox.showerror("Error", "No file selected for encryption!")

# DECRYPT FILE 
def decrypt_file():
    input_File = filedialog.askopenfilename(title="Select File to Decrypt")
    if input_File:
        password = simpledialog.askstring("Password", "Enter password for decryption:", show='*')
        if password:
            if input_File.endswith(".enc"):
                output_File = input_File[:-4] + ".dec"
            else:
                output_File = input_File + ".dec"
            decryption(input_File, output_File, password)
            messagebox.showinfo("Success", f"File decrypted successfully!\n{output_File}")
        else:
            messagebox.showerror("Error", "Password is required for decryption!")
    else:
        messagebox.showerror("Error", "No file selected for decryption!")

# _____________________________________  AES Encryption _______________________________________

# FILE ENCRYPTION 
def encryption(input_file, output_file, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password.encode('utf-8'), salt, dkLen=32, count=100000)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        with open(input_file, 'rb') as inputFile, open(output_file, 'wb') as outputFile:
            outputFile.write(salt)
            outputFile.write(iv)

            while True:
                chunk = inputFile.read(4096)
                if len(chunk) == 0:
                    break
                if len(chunk) % 16 != 0:
                    chunk = pad(chunk, 16)
                cipherText = cipher.encrypt(chunk)
                outputFile.write(cipherText)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")

# _____________________________________  Retrieval and Decryption  _______________________________________

# FILE DECRYPTION 
def decryption(input_file, output_file, password):
    try:
        with open(input_file,'rb') as inputFile:
            salt = inputFile.read(16)
            iv = inputFile.read(16)

            if len(salt) != 16 or len(iv) != 16:
                raise ValueError("Invalid encrypted file format!")

            key = PBKDF2(password.encode('utf-8'), salt, dkLen=32, count=100000)
            cipher = AES.new(key, AES.MODE_CBC, iv)

            with open(output_file, 'wb') as outputFile:
                while True:
                    chunk = inputFile.read(4096)
                    if len(chunk) == 0:
                        break
                    decrypted_chunk = cipher.decrypt(chunk)
                    if inputFile.tell() == os.path.getsize(input_file):
                        decrypted_chunk = unpad(decrypted_chunk, 16)
                    outputFile.write(decrypted_chunk)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")
    except ValueError as e:
        messagebox.showerror("Error", f"Decryption failed: {e}")

# _____________________________________ RUN LOGIN   _______________________________________

login_window()


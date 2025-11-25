import tkinter
from tkinter import messagebox
import hashlib
import os
from Crypto.Protocol.KDF import PBKDF2
from Crypto.cipher import AES
from Crypto.Random imprt get_random_bytes
from Crypto.Util.Padding import pad, unpad

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
    register_win.title("Secure File Storage - Register")
    register_win.geometry("300x200")

    tkinter.Label(register_win, text="Username:").pack(pady=5)
    entry_user = tkinter.Entry(register_win)
    entry_user.pack()

    tkinter.Label(register_win, text="Password:").pack(pady=5)
    entry_pass = tkinter.Entry(register_win, show="*")
    entry_pass.pack()

    tkinter.Button(register_win, text="Register", command=register_action).pack(pady=5)

#Encrypt files
def encryption(input_file, output_file, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password.encode('utf-8'), salt, dkLen=32, count=100000)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        with open(input_file, 'rb') as inputFile, open(output_file, 'wb') as outputFile:
            
            # Write salt + IV to encrypted file
            outputFile.write(salt)
            outputFile.write(iv)
            
            while True:
                chunk = inputFile.read(4096)

                if len(chunk) == 0:
                    break

                if len(chunk) < 4096:
                    chunk = pad(chunk, 16)

                cipherText = cipher.encrypt(chunk)
                outputFile.write(cipherText)

    except FileNotFoundError:
        print("File not found!")


#Decrypt files
def decryption(input_file, output_file, password):
    try:
        with open(input_file,'rb') as inputFile:
            # Read salt and IV
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

                    # Check if this is the last chunk
                    if inputFile.tell() == os.path.getsize(input_file):
                        decrypted_chunk = unpad(decrypted_chunk, 16)

                    outputFile.write(decrypted_chunk)

    except FileNotFoundError:
        print("File not found!")
    except ValueError as e:
        print("Decryption error:", e)
    
    

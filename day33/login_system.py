import tkinter as tk
from tkinter import messagebox
import json

PATH = "users.json"

root = tk.Tk()
root.title("Login")
root.geometry("300x450")


def get_users():
    with open(PATH, "r") as file:
        return json.load(file)

def access():
    user_username = username.get().strip()
    user_password = password.get().strip()
    users = get_users()
    
    for user in users:
        if user["username"] == user_username and user["password"] == user_password:
            messagebox.showinfo("Login success", f"Welcome {user_username}")
            break
    else:
        messagebox.showerror("Login Failed", "Invalid user or password")
    
tk.Label(root, text="Username", font=("Arial", 8)).pack(pady=10)
username = tk.Entry(root)
username.pack()
tk.Label(root, text="Password", font=("Arial", 8)).pack()
password = tk.Entry(root, show="*")
password.pack()
access_btn = tk.Button(root, text="Login", command=access)
access_btn.pack(pady=10)

root.mainloop()
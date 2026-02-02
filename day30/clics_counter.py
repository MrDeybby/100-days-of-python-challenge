import tkinter as tk


root = tk.Tk()
root.title("Clics Counter")
root.geometry("600x400")


def increase_clics():
    global counter 
    global label
    global button2
    
    counter += 1
    label.config(text=f"Clic Counter: {counter}")
    
    if button2["state"] == "disabled":
        button2.config(state="normal")

def reset_counter():
    global counter 
    global label
    global button2
    
    counter = 0
    label.config(text=f"Clic Counter: {counter}")
    
    button2.config(state="disabled")
    
counter = 0
label = tk.Label(root, text=f"Clic Counter: {counter}")
label.pack(pady=10)

button = tk.Button(root, text="Clic me", command=increase_clics)
button.pack(pady=10)

button2 = tk.Button(root, text="Reset", command=reset_counter, state="disabled")
button2.pack(pady=10)

root.mainloop()

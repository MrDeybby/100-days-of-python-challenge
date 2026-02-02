import tkinter as tk

root = tk.Tk()
root.title("Event Handling")
root.geometry("300x200")

label = tk.Label(root, text="Enter your name")
label.pack()

entry = tk.Entry(root)
entry.pack()

def greet():
    name = entry.get()
    if name:
        label.config(text=f"Hello {name}")
def reset():
    global label
    global entry
    
    label.config(text="Enter your name")
    entry.delete(0, tk.END)
    
button = tk.Button(root, text="Greet", command=greet)
button.pack()

button2 = tk.Button(root, text="Reset", command=reset)
button2.pack()


root.mainloop()

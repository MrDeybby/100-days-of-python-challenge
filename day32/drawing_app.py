import tkinter as tk
from tkinter import colorchooser

root = tk.Tk()
root.title("Drawing App")
root.geometry("400x550")

thickness = 1
color = "black"


def change_thickness(value):
    global thickness
    thickness = int(value)


def draw(event):
    x, y = event.x, event.y
    canvas.create_oval(x, y, x + thickness, y + thickness, fill=color, outline=color)


def change_color():
    global color
    new_color = colorchooser.askcolor()[1]
    if new_color:
        color = new_color


def reset_canvas():
    canvas.delete("all")


title_label = tk.Label(root, text="Drawing APP", font=("Arial", 15))
title_label.pack()

canvas = tk.Canvas(root, width=350, height=350, bg="white")
canvas.pack()

thickness_label = tk.Label(root, text=f"Thickness:", font=("Arial", 10))
thickness_label.pack()

thickness_level = tk.Scale(
    root, from_=1, to=10, orient="horizontal", command=change_thickness
)
thickness_level.pack()

change_color_btn = tk.Button(root, text="Change color", command=change_color)
change_color_btn.pack()

clear_canvas_btn = tk.Button(root, text="Reset canvas", command=reset_canvas)
clear_canvas_btn.pack()

canvas.bind("<B1-Motion>", draw)
root.mainloop()

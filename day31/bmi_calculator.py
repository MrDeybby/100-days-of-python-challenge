import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("250x400")

title_label = tk.Label(root, text="BMI Calculator", font=("Arial", 15))
title_label.pack(pady=10)

label_weight= tk.Label(root, text="Enter Your weight (kg)")
label_weight.pack(pady=10)
entry_weight = tk.Entry(root)
entry_weight.pack()

label_height = tk.Label(root, text="Enter Your height (m)")
label_height.pack(pady=10)
entry_height = tk.Entry(root)
entry_height.pack()

label_result = tk.Label(root)
label_result.pack()

def calculate_bmi(height:int, weight:int) -> (float | int):
    bmi = weight / (height * height)
    status = None
    if bmi < 18.5:
        status = "Underweight" 
    elif bmi <  24.9:
        status = "Normal weight"
    elif bmi < 29.9:
        status = "Overweight"
    else:
        status = "Obesity"
    
    return bmi, status

def display_bmi():
    try:
        height = float(entry_height.get())
        weight = float(entry_weight.get())
        if weight <= 0 or height <=0:
            raise ValueError("Height and weight must be greater than 0")
        bmi, status = calculate_bmi(height=height, weight=weight)
        label_result.config(text=f"The BMI is: {bmi:.2f} \n Status is: {status}", font=("Arial", 10))
        label_result.pack(pady=10)
        
    except ValueError:
        messagebox.showerror("Invalid input","Height and weight must be numbers")

def reset():
    entry_height.delete(0, tk.END)
    entry_weight.delete(0, tk.END)
    label_result.config(text="", font=("Arial", 0))

button = tk.Button(root, text="Calculate BMI", command=display_bmi)
button.pack()
reset_button = tk.Button(root, text="Clear", command=reset)
reset_button.pack()
root.mainloop()
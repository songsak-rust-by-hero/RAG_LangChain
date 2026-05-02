import tkinter as tk

def say_hello():
    label.config(text="Hello!")

root = tk.Tk()
root.title("My App")

label = tk.Label(root, text="กดปุ่มสิ")
label.pack()

button = tk.Button(root, text="Click me", command=say_hello)
button.pack()

root.mainloop()
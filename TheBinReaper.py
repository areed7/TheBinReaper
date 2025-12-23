import tkinter as tk

def clicked():
    print("Button pressed")

root = tk.Tk()
root.title("Simple Button")

btn = tk.Button(root, text="Click me", command=clicked)
btn.pack(padx=20, pady=20)

root.mainloop()
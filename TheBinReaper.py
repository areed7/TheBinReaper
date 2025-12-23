import tkinter as tk
from tkinter import ttk

from TestGrimoire import TestGrimoire

#initialize the test grimoire
tg=TestGrimoire()

root = tk.Tk()
root.title("Bin Reaper")

projectNameVar = tk.StringVar(value="Test Name")
projectVersionVar = tk.StringVar(value="Test Version")
projectCreationDateVar = tk.StringVar(value="Creation Date")
projectModificationDateVar = tk.StringVar(value="Modification Date")

def open_project():
    tg.open_project()
    projectNameVar.set("Project Name: " + tg.projectName)
    projectVersionVar.set("Project Version: " + tg.projectVersion)
    projectCreationDateVar.set("Creation Date: " + tg.creationDate)
    projectModificationDateVar.set("Modification Date: " + tg.modificationDate)

def close_project():
    tg.close_project()
    projectNameVar.set("Project Name: " + tg.projectName)
    projectVersionVar.set("Project Version: " + tg.projectVersion)
    projectCreationDateVar.set("Creation Date: " + tg.creationDate)
    projectModificationDateVar.set("Modification Date: " + tg.modificationDate)

def start_new_lot():


def save_datalogs():



# layout config
root.columnconfigure((0,1,2), weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)
menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open Project", command=open_project)
filemenu.add_command(label="Close Project", command=close_project)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

datalogMenu = tk.Menu(menubar, tearoff=0)
datalogMenu.add_command(label="Start New Lot", command=open_project)
datalogMenu.add_command(label="Save Datalogs", command=close_project)
menubar.add_cascade(label="Datalog", menu=datalogMenu)

root.config(menu=menubar)

# LEFT – info
left_container = ttk.Frame(root)
left_container.grid(row=0, column=0, sticky="ns")
canvas = tk.Canvas(left_container, width=220)
scroll = ttk.Scrollbar(left_container, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll.set)
left = ttk.Frame(canvas, padding=8)
canvas.create_window((0, 0), window=left, anchor="nw")
left.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.pack(side="left", fill="y")
scroll.pack(side="right", fill="y")
ttk.Label(left, textvariable=projectNameVar).pack(anchor="w")
ttk.Label(left, textvariable=projectVersionVar).pack(anchor="w")
ttk.Label(left, textvariable=projectCreationDateVar).pack(anchor="w")
ttk.Label(left, textvariable=projectModificationDateVar).pack(anchor="w")

# CENTER – log / results
center = ttk.Frame(root, padding=8)
center.grid(row=0, column=1, sticky="nsew")
center.rowconfigure(0, weight=1)
center.columnconfigure(0, weight=1)

log = tk.Text(center, wrap="word")
log.grid(row=0, column=0, sticky="nsew")
log.configure(state="disabled")

# RIGHT – buttons
right = ttk.Frame(root, padding=8)
right.grid(row=0, column=2, sticky="nse")
ttk.Button(right, text="Start").pack(fill="x")
ttk.Button(right, text="Stop").pack(fill="x")
ttk.Button(right, text="Load").pack(fill="x")

# BOTTOM – bins / yield
bottom = ttk.Frame(root, padding=8)
bottom.grid(row=1, column=0, columnspan=3, sticky="ew")
ttk.Label(bottom, text="Bin 1: 95%   Yield: 92%").pack(anchor="w")

root.mainloop()

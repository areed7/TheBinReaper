import tkinter as tk
from tkinter import ttk

from DUTGrimoire import DUTGrimoire
from TestGrimoire import TestGrimoire
from TestExecutioner import TestExecutioner

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"

class TheBinReaper:
    def __init__(self):
        self.tg = TestGrimoire()
        self.te = TestExecutioner()
        self.dg = None
        self.currentSN = "1"
        self.currentFlow = "None"
        self.currentLot = "None"

    def open_program(self):
        self.tg.open_project()
        self.currentSN = "1"
    
    def close_program(self):
        self.tg.close_project()
        self.dg = None
        self.currentSN = "1"
        self.currentFlow = "None"
        self.currentLot = "None"

    def select_flow(self, flowName: str):
        available_flows = self.tg.grab_available_flows()
        if flowName not in available_flows:
            print("Error: Flow selected does not exist in list of available flows!")
            print("Available Flows: " + ", ".join(map(str, available_flows)))
            return
        self.currentFlow = flowName
        self.dg = DUTGrimoire(self.tg, self.currentLot, self.currentFlow)
    
    def set_lot(self, lotName: str):
        self.currentLot = lotName
    
    def set_sn(self, sn:str):
        self.currentSN = sn

    def execute(self):
        self.te.execute(self.tg, self.dg, self.currentFlow, self.currentSN)
        self.dg.autolog_write(self.tg.programDirectory)

    def setflow_prompt(self):
        if self.tg.projectName == "":
            print("")
            print("======================================================")
            print("                    Select Flow                       ")
            print("======================================================")
            print("")
            print("No Program Loaded...")
            print("")
        else:
            print("")
            print("======================================================")
            print("                    Select Flow                       ")
            print("======================================================")
            print("")
            
            line = ""

            print("Warning: Loading a new flow will reset data.")
            while line.lower() not in ['y', 'n']:
                    line = input("Are you sure you want to change flows? y/n  ")
                    if line.lower() == "y":
                        break
                    if line.lower() == "n":
                        line = ""
                        return
            
            print(f"[c]\t-- Cancel")

            available_flows = self.tg.grab_available_flows()
            indexNum = 0
            for flow in available_flows:
                print(f"[{indexNum}]\t-- "+flow)
                indexNum = indexNum + 1
            
            flowIndex = -1
            while flowIndex == -1 or flowIndex >= len(available_flows):
                if line.lower() == "c":
                    break
                line = input("Please Select a Flow: ")
                try:
                    flowIndex = int(line)
                    self.currentFlow = available_flows[flowIndex]
                except Exception as e:
                    continue
            #tg: TestGrimoire, lotName: str, selectedTestFlow: str):
            self.dg = DUTGrimoire(self.tg, self.currentLot, self.currentFlow)
            print("")


    def print_info(self):
        if self.tg.projectName == "":
            print("")
            print("======================================================")
            print("                        INFO                          ")
            print("======================================================")
            print("")
            print("No Program Loaded...")
            print("")
        else:
            print("")
            print("======================================================")
            print("                        INFO                          ")
            print("======================================================")
            print("")
            print("Program Name:\t\t" + self.tg.projectName)
            print("Program Ver:\t\t" + self.tg.projectVersion)
            print("Creation Date:\t\t" + self.tg.creationDate)
            print("Modify Date:\t\t" + self.tg.modificationDate)
            print("Selected Flow:\t\t"+ self.currentFlow)
            print("Current SN:\t\t"+ self.currentSN)
            print("Current Lot:\t\t"+ self.currentLot)
            print("")
    
    def print_help(self):
        print("")
        print("======================================================")
        print("                      HELP MENU                       ")
        print("======================================================")
        print("clear\t\t\t\t--\tClears the screen of all current info.")
        print("info\t\t\t\t--\tPrints out the current lot and program information.")
        print("openprogram\t\t\t--\tPops up a dialog that will allow the user to select the bprg program file.")
        print("closeprogram\t\t\t--\tCloses the currently open program.")
        print("setflow\t\t\t\t--\tLists all available flows for the current program and promps the user to set it. This will reset data.")
        print("lot [lot name]\t\t\t--\tSets the lot name that will be applied to the datalog.")
        print("sn [serial number]\t\t--\tSets the current serial number.")
        print("execute\t\t--\tRuns the program on the current dut.")
        print("savedata\t\t\t--\tOpens a dialog to save data.")
        print("")

    #Handle user input.
    def run(self):
        
        while True:
            line = input("> ")
            match True:
                case _ if line.lower() == "exit":
                    while line.lower() not in ['y', 'n']:
                        line = input("> Are you sure you want to exit? y/n  ")
                        if line.lower() == "y":
                            exit()
                        if line.lower() == "n":
                            line = ""
                            break
                    pass

                case _ if line.lower() == "openprogram":
                    self.open_program()
                    pass

                case _ if line.lower() == "closeprogram":
                    self.close_program()
                    pass

                case _ if line.lower().startswith("lot"):
                    try:
                        self.set_lot(line.split(" ")[1])
                    except Exception as e:
                        print("Failed to set lot. Please ensure you're using the command correctly.")
                    pass

                case _ if line.lower().startswith("sn"):
                    try:
                        self.set_sn(line.split(" ")[1])
                    except Exception as e:
                        print("Failed to set lot. Please ensure you're using the command correctly.")
                    pass

                case _ if line.lower() == "execute":
                    self.execute()
                    pass

                case _ if line.lower() == "info":
                    self.print_info()
                    pass
                
                case _ if line.lower() == "setflow":
                    self.setflow_prompt()
                    pass

                case _ if line.lower() == "help":
                    self.print_help()
                    pass
                
                case _ if line.lower() == "savedata":
                    self.dg.write_datalog()
                    pass

                case _ if line.lower() == "clear":
                    print("\033c", end="")
                    pass

                case _ if line == "":
                    pass

                case _:
                    print("Unrecognized Command")
                    pass
                
                    
                    

if __name__ == "__main__":

    br = TheBinReaper()
    br.run()
    


'''

#initialize the test grimoire
tg=TestGrimoire()
te=TestExecutioner()
dg=None

currSN = "1"
currFlow = "None"

root = tk.Tk()
root.title("Bin Reaper")


projectNameVar = tk.StringVar(value="Test Name: ")
projectVersionVar = tk.StringVar(value="Test Version: ")
projectCreationDateVar = tk.StringVar(value="Creation Date: ")
projectModificationDateVar = tk.StringVar(value="Modification Date: ")
lotNameVar = tk.StringVar(value="LOT: ")
flowVar = tk.StringVar(value="Flow: ")
currSNVar = tk.StringVar(value="SN: ")

def open_project():
    tg.open_project()
    currSN = "1"
    projectNameVar.set("Project Name: " + tg.projectName)
    projectVersionVar.set("Project Version: " + tg.projectVersion)
    projectCreationDateVar.set("Creation Date: " + tg.creationDate)
    projectModificationDateVar.set("Modification Date: " + tg.modificationDate)
    
    dg = DUTGrimoire("LotName", tg, tg.flows.keys()[0])
    
    lotNameVar = tk.StringVar(value="LOT: " + dg.lotName)
    flowVar = tk.StringVar(value="Flow: " + currFlow)
    currSNVar = tk.StringVar(value="SN: " + currSN)


def close_project():
    tg.close_project()
    projectNameVar.set("Project Name: " + tg.projectName)
    projectVersionVar.set("Project Version: " + tg.projectVersion)
    projectCreationDateVar.set("Creation Date: " + tg.creationDate)
    projectModificationDateVar.set("Modification Date: " + tg.modificationDate)

if __name__ == "__main__":
    open_project()


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
ttk.Label(left, textvariable=lotNameVar).pack(anchor="w")
ttk.Label(left, textvariable=flowVar).pack(anchor="w")
ttk.Label(left, textvariable=currSNVar).pack(anchor="w")

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
'''
from TestGrimoire import TestGrimoire
from datetime import datetime
from tkinter import filedialog
import socket
import os
class DUTGrimoire:
    def __init__(self, tg: TestGrimoire, lotName: str, selectedTestFlow: str):

        datetimenow = datetime.now()

        self.computerName   = socket.gethostname()
        self.lotName        = lotName
        self.dateStart      = datetimenow.strftime("%d%b%Y %H:%M").upper()
        self.dateStartFile  = datetimenow.strftime("%m%d%Y_%H_%M").upper()
        self.isA            = False
        self.testHeaders    = []
        self.maxLimits      = []
        self.minLimits      = []
        self.testUnits      = []
        self.testIds        = []
        self.testResults    = []

        if selectedTestFlow == "None":
            print("Error: No flow selected in DUTGrimoire. Please select a flow before trying again.")
            return

        
        self.testHeaders.append("")
        self.testHeaders.append("")

        self.testUnits.append("SN")
        self.testUnits.append("BIN")

        self.testIds.append("")
        self.testIds.append("")
        
        self.maxLimits.append("Max Limits")
        self.maxLimits.append("")

        self.minLimits.append("Min Limits")
        self.minLimits.append("")

        #Parse out the current test flow, and assemble the test headers
        testList = tg.flows[selectedTestFlow].split(",")

        testIndex = 0
        for test in testList:
            testIndex = testIndex + 1
            #Grab the subtests and number of sub tests for this program.
            subtests    =   tg.grab_subtests(test)
            numSubtests = len(subtests)
            for stIndex in range(0, numSubtests):
                testIDStr = str(testIndex) + "_" + str(stIndex)
                self.testIds.append(testIDStr)
                first = next(j for j in subtests if j["sub_test_index"] == stIndex)
                self.testHeaders.append( test + "_" + first["sub_test_name"])
                self.minLimits.append(first["min_limit"])
                self.maxLimits.append(first["max_limit"])
                self.testUnits.append(first["units"])
                
    
    def set_lot(self, lotName: str):
        self.lotName = lotName

    def add_result(self, results):
        self.testResults.append(results)

    def autolog_write(self, path: str):
        self.isA = not self.isA
        file = path + "/autolog/"
        if not os.path.exists(file):
            os.makedirs(file)
        if self.isA:
            file = file + self.lotName + "_" + self.dateStartFile + "_A.csv"
        else:
            file = file + self.lotName + "_" + self.dateStartFile + "_B.csv"
        print(file)
        self.write_datalog(file)

    def write_datalog(self, path = ""):
        if(path == ""):
            path = filedialog.asksaveasfilename(defaultextension=".csv")
        if( path == "" ):
            print("No path selected to save datalogs.")
            return
        with open(path, "w") as f:
            f.write("Date,"+ self.dateStart + "\n")
            f.write("Computer Name," + self.computerName + "\n")
            f.write("Lot,"+ self.lotName + "\n")
            f.write(",".join(map(str, self.testIds)) + "\n")
            
            f.write(",".join(map(str, self.testHeaders)) + "\n")
            f.write(",".join(map(str, self.maxLimits)) + "\n")
            f.write(",".join(map(str, self.minLimits)) + "\n")
            f.write(",".join(map(str, self.testUnits)) + "\n")
            
            
            for result in self.testResults:
                f.write(",".join(map(str, result)) + "\n")

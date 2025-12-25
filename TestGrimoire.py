from tkinter import filedialog
from tkinter import messagebox
from collections import namedtuple
import json
import os
#Used for the following:
    #Create new projects
    #Add or remove tests for those projects
    #Add or remove parameters and results for those tests
#Basic ATE software to help rapidly develop test programs with data logging.

#Programs will be denoted with .bprg
#.bprg file should have the following format:
#10,Version,CreationDate,LastModifiedDate
#20,TestName,TestVersion
#50,BinID,Name
#90,FlowSet,TestName,SubTestName,Bin,Units,MinLimit,MaxLimit
#100,FlowSet,TestName,SubTestName,Bin,Units,MinLimit,MaxLimit
#100,FlowSet,TestName,SubTestName,Bin,Units,MinLimit,MaxLimit

#10 denotes the version, creation date, and last modification date
#20 denotes the test name and test version
#50 denotes the bin ID and the string name it implies

#90 Denotes the headers for #100
#100 denotes the test list info
#TestName: Name of Python Module
#FlowSet: Name of the limit set and test list that's currently selected to run
#SubTestName: Name of the value sent to the datalog
#SubTestNames should be in the order by which they are datalogged
#Bin: The Bin that the test will fail to.
#Units: The Units for the datalog such as kOhms or uVolts
#MinLimit and MaxLimit: The minimium and maximum values by which the test will fail.

#This file does not run programs. It should only parse data in and out, and provide the ""

class TestGrimoire:
    def __init__(self):
        self.programPath = ""
        self.programDirectory = ""
        self.projectName = ""
        self.projectVersion = ""
        self.creationDate = ""
        self.modificationDate = ""
        self.bins = {} #Simple lookup table for the bins.
        self.tests = [] #Tests are simply a list of jsons.
        self.flows = {}

    #Open a project file and attempt to parse the file.
    #Should throw errors.
    def open_project(self):
        
        self.programPath = filedialog.askopenfilename(filetypes=[("Bin Reaper Program", "*.bprg")])
        self.programDirectory = os.path.dirname(self.programPath)
        #Parse the project. First grab the name and version.
        data=[]
        with open(self.programPath, "r") as file:
            data = file.read()
        
        #Parse conditions for each line type.
        line_id10Counter = 0
        line_id20Counter = 0
        for line in data.splitlines():
            #Try to parse the line as Json. Throw error if fails.
            jLine={}
            try:
                jLine = json.loads(line)
            except Exception as e:
                #Close the project throw an error and leave the open project function.
                messagebox.showerror("Error", "Failed to parse line as json: " + line)
                self.close_project()
                return
            match True:
                
                ######################################
                ##          Parse Version 10,       ##
                ######################################
                case _ if jLine["line_id"] == 10:
                    line_id10Counter = line_id10Counter + 1
                    if(line_id10Counter >= 2):
                        messagebox.showerror("Error", "More than one line id 10 spotted.")
                        self.close_project()
                        return
                    self.creationDate       = jLine["creation_date"]
                    self.modificationDate   = jLine["modification_date"]
                    pass
                ##################################
                ##      Parse Test Name 20,     ##
                ##################################
                case _ if jLine["line_id"] == 20:
                    line_id20Counter = line_id20Counter + 1
                    if(line_id20Counter >= 2):
                        messagebox.showerror("Error", "More than one line id 20 spotted.")
                        self.close_project()
                        return
                    self.projectName        = jLine["program_name"]
                    self.projectVersion     = jLine["program_version"]
                    pass
                ##############################
                ##      Prase Bins 50,      ##
                ##############################
                case _ if jLine["line_id"] == 50:
                    self.bins[ jLine["bin_num"] ]   =   jLine["bin_name"]
                    pass

                ##############################
                ##      Parse Flows 90      ##
                ##############################
                case _ if jLine["line_id"] == 90:
                    self.flows[jLine["flow_set"]] = jLine["test_order"]
                    pass
                ##################################
                ##      Parse Test Info 100,    ##
                ##################################
                case _ if jLine["line_id"] == 100:
                    self.tests.append( jLine )
                    pass
    
    #Combines all the parameters for each of the sub tests into one lookup table.
    def grabParams(self, testName):
        subtests    = [j for j in self.tests if j["test_name"] == testName]
        params = {}
        for subtest in subtests:
            params = {**params, **subtest["params"]}
        return params

    def grabSubtests(self, testName):
        subtests    = [j for j in self.tests if j["test_name"] == testName]
        return subtests

    #Clear out all info that was previously loaded.
    def close_project(self):
        self.programPath = ""
        self.programDirectory = ""
        self.projectName = ""
        self.projectVersion = ""
        self.creationDate = ""
        self.modificationDate = ""
        self.bins = {} #Simple lookup table for the bins.
        self.tests = [] #Tests are simply a list of jsons.
        self.flows = {}
    

if __name__ == "__main__":
    tg = TestGrimoire()
    tg.open_project()
    
    print(tg.grabParams("ResistanceB"))
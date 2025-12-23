from tkinter import filedialog; 
from tkinter import messagebox;
from collections import namedtuple
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


#testdef named tuple for the tests
TestDef = namedtuple(
    "TestDef",
    ["flow_set", "test_name", "sub_test_name", "bin", "units", "min_limit", "max_limit"]
)

class TestGrimoire:
    def __init__(self):
        self.programPath = ""
        self.projectName = ""
        self.projectVersion = ""
        self.bins = {} #Simple lookup table for the bins.
        self.tests = [] #Tests are stored as a set of tuples Each Tuple is the same order as above. FlowSet,TestName,SubTestName,Bin,Units,MinLimit,MaxLimit

    #Open a project file and attempt to parse the file.
    #Should throw errors.
    def open_project(self):
        
        self.programPath = filedialog.askopenfilename(filetypes=[("Bin Reaper Program", "*.bprg")])
        #Parse the project. First grab the name and version.
        data=[]
        with open(self.programPath, "r") as file:
            data = file.read()
        
        #Parse conditions for each line type.
        versionLine10Counter = 0
        testnameLine20Counter = 0
        for line in data.splitlines():
            
            match True:
                
                ######################################
                ##          Parse Version 10,       ##
                ######################################
                case _ if line.startswith("10,"):
                    print("Version Line: " + line)
                    versionLine10Counter = versionLine10Counter + 1
                    if( versionLine10Counter >= 2):
                         messagebox.showerror("Error", "More than one version lines detected in the .bprg file. Please ensure only one version \"10,\" line exists.")
                         self.close_project()
                         break
                    pass
                ##################################
                ##      Parse Test Name 20,     ##
                ##################################
                case _ if line.startswith("20,"):
                    print("Test Name Line:" + line)
                    testnameLine20Counter = testnameLine20Counter + 1
                    if( testnameLine20Counter >= 2):
                         messagebox.showerror("Error", "More than one test name lines detected in the .bprg file. Please ensure only one version \"20,\" line exists.")
                         self.close_project()
                         break
                    pass
                ##############################
                ##      Prase Bins 50,      ##
                ##############################
                case _ if line.startswith("50,"):
                    try:
                        sLine=line.split(",")
                        self.bins[sLine[1]] = sLine[2]
                    except Exception as e:
                        print("Failed to parse line: " + line)
                        messagebox.showerror("Error", "Failed to load bins. Please verify the .bprg file. Lines that have the following format: \"50,BinNumber,BinName\"")
                        self.close_project()
                        break
                    pass
                ##################################
                ##      Parse Test Info 100,    ##
                ##################################
                case _ if line.startswith("100,"):
                    try:
                        sLine=line.split(",")
                        self.tests.append(TestDef(sLine[1],sLine[2],sLine[3],sLine[4],sLine[5],sLine[6],sLine[7]))

                        #Limit Sanity Check
                        if(float(sLine[6]) > float(sLine[7])):
                            messagebox.showerror("Error", "Limit sanity check failed.")
                            raise ValueError("Limit Sanity Check")
                    except Exception as e:
                        print("Failed to parse line: " + line)
                        messagebox.showerror("Error", "Failed to parse a test for line: " + line)
                        self.close_project()
                        break
                    pass

    #Clear out all info that was previously loaded.
    def close_project(self):
        self.programPath = ""
        self.projectName = ""
        self.projectVersion = ""
        self.bins = {}
        self.tests = []
    
fc = TestGrimoire()
fc.open_project()
print(fc.tests)
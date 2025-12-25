from TestGrimoire import TestGrimoire
from DUTGrimoire import DUTGrimoire
import importlib.util

class TestExecutioner:
    def __init__(self):
        self.selectedTestFlow = ""


    def run_test(self, script_path, params):
        spec = importlib.util.spec_from_file_location("test_module", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Resistor.invoke(params)

    #Simply select the tests based on the flow. 
    def selectFlow(self, selectedTestFlow: str):
        self.selectedTestFlow = selectedTestFlow
    

    #When the test executes we first loop through and attempt to import all the .py files.
    #After importing them we try to run "Testname.invoke(params)" with the parameters passed into the test. The parameters are a simple lookup table.
    def execute(self, tg: TestGrimoire, dg: DUTGrimoire, sn: str):
        #Loop through the selected flow and execute each test.
        tests = tg.flows[self.selectedTestFlow].split(",")

        #Initalize with a bin 1. Change index 2 if the dut fails.
        snBin = [sn, 1]
        hasBinBeenSet = False
        totalRes = []
        #Loop through each test. Execute the test.
        for test in tests:
            subtests    = tg.grabSubtests(test)
            numSubtests = len(subtests)
            program_file = tg.programDirectory + "/" + str(subtests[0]["program_file"])
            results = self.run_test(program_file, tg.grabParams(test) )
            totalRes = totalRes + results
            #Check to see if any of the results are a fail condition of each subtest.
            for subtestIndex in range(0, numSubtests):
                first = next(j for j in subtests if j["sub_test_index"] == subtestIndex)
                for result in results:
                    if result > first["max_limit"] or result < first["min_limit"]:
                        print("Max Limit: " + str(first["max_limit"]) + "\tMin Limit: " + str(first["min_limit"]))
                        if hasBinBeenSet == False:
                            hasBinBeenSet = True
                            snBin[1] = first["bin"]

        dg.addResult(snBin + totalRes)
            
       
        
if __name__ == "__main__":

    te = TestExecutioner()
    te.selectFlow("25C")


    tg = TestGrimoire()
    tg.open_project()

    dg = DUTGrimoire("180520_14", tg, "25C")

    te.execute(tg, dg, "SN1")
    te.execute(tg, dg, "SN2")
    te.execute(tg, dg, "SN3")
    print(dg.testResults)
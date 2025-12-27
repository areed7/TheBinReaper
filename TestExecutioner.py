from TestGrimoire import TestGrimoire
from DUTGrimoire import DUTGrimoire
import importlib.util


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"

class TestExecutioner:
    def __init__(self):
        self.selectedTestFlow = ""


    def run_test(self, script_path, params):
        spec = importlib.util.spec_from_file_location("test_module", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Resistor.invoke(params)

    #When the test executes we first loop through and attempt to import all the .py files.
    #After importing them we try to run "Testname.invoke(params)" with the parameters passed into the test. The parameters are a simple lookup table.
    def execute(self, tg: TestGrimoire, dg: DUTGrimoire, selectedFlow: str, sn: str, continueOnFail = False):
        
        if selectedFlow == "None":
            print("No flow Selected. Test will not execute.")
            return

        #Loop through the selected flow and execute each test.
        tests = tg.flows[selectedFlow].split(",")

        #Initalize with a bin 1. Change index 2 if the dut fails.
        snBin = [sn, 1]
        hasBinBeenSet = False
        totalRes = []
        #Loop through each test. Execute the test.
        for test in tests:
            print(test)
            subtests    = tg.grab_subtests(test)
            numSubtests = len(subtests)
            program_file = tg.programDirectory + "/" + str(subtests[0]["program_file"])
            results = self.run_test(program_file, tg.grab_params(test) )
            totalRes = totalRes + results
            #Check to see if any of the results are a fail condition of each subtest.
            for subtestIndex in range(0, numSubtests):
                first = next(j for j in subtests if j["sub_test_index"] == subtestIndex)
                for result in results:
                    if result > first["max_limit"] or result < first["min_limit"]:
                        #print("Max Limit: " + str(first["max_limit"]) + "\tMin Limit: " + str(first["min_limit"]))
                        if hasBinBeenSet == False:
                            hasBinBeenSet = True
                            snBin[1] = first["bin"]
                        if continueOnFail == False:
                            break
        if snBin[1] == 1:
            print("SN: " + sn + GREEN + "\t\tPASS" + RESET)
        else:
            print("SN: " + sn + RED + "\t\tFAIL BIN " + str(snBin[1]) + RESET)
        
        dg.add_result(snBin + totalRes)
            
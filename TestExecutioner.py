from TestGrimoire import TestGrimoire
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
    def execute(self, tg: TestGrimoire):
        #Loop through the selected flow an execute each test.
        tests = tg.flows[self.selectedTestFlow].split(",")

        for test in tests:
            subtests    = tg.grabSubtests(test)
            program_file = tg.programDirectory + "/" + str(subtests[0]["program_file"])
            print(self.run_test(program_file, tg.grabParams(test) ))
            
       
        
if __name__ == "__main__":

    te = TestExecutioner()
    te.selectFlow("25C")


    tg = TestGrimoire()
    tg.open_project()

    te.execute(tg)
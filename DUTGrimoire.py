from TestGrimoire import TestGrimoire
import socket
class DUTGrimoire:
    def __init__(self, lotName: str, tg: TestGrimoire, selectedTestFlow: str):
        self.computerName   = socket.gethostname()
        self.lotName        = lotName
        self.testHeaders    = []
        self.testIds        = []
        self.testResults    = []

        #First column for test headers is the sn
        #Second is the bin number
        #Followed by all the test names
        self.testHeaders.append("SN")
        self.testHeaders.append("BIN")

        #Append nothing for the first two test ids list.
        self.testIds.append("")
        self.testIds.append("")

        #Parse out the current test flow, and assemble the test headers
        testList = tg.flows[selectedTestFlow].split(",")

        testIndex = 0
        for test in testList:
            testIndex = testIndex + 1
            #Grab the subtests and number of sub tests for this program.
            subtests    =   tg.grabSubtests(test)
            numSubtests = len(subtests)
            for stIndex in range(0, numSubtests):
                testIDStr = str(testIndex) + "_" + str(stIndex)
                self.testIds.append(testIDStr)
                first = next(j for j in subtests if j["sub_test_index"] == stIndex)
                self.testHeaders.append( test + "_" + first["sub_test_name"])

        print(self.testIds)
        print(self.testHeaders)


    def addResult(self, results):
        self.testResults.append(results)

    def writeDatalog(self):
        return


if __name__ == "__main__":
    tg = TestGrimoire()
    tg.open_project()

    dg = DUTGrimoire("180520_14", tg, "25C")
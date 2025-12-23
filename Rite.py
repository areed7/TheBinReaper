#Base class for tests. 
#Just an on-theme name for a test. A DUT must pass all rites to achieve Ascension (Bin 1, or any passing bin).
#A dut that does not achieve bin 1 is reaped. (Play a little animation or something)

#program is simply self invoke and self banish.
#Invoke() should run the program as normal. 
#If anything happens while the program is running, then call your own return self.banish().
#banish() should set up results with invalid data such that it can trace what problem may be happening from the data alone.
class Rite:
    def __init__(self):
        self.results = []

    def invoke(self, params=[]):
        return self.results

    def banish(self):
        #Invalid data detected in your invoke() call your banish()
        #Shutdown safely
        #Append results with invalid data
        #Return the invalid data with a return self.banish()
        #self.results.append(9999.0)
        return self.results
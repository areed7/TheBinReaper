import random
class Resistor:
    def __init__(self):
        self.results = []

    def invoke(self, params={}):
        try:

            #Force current, measure voltage
            forcedCurrent = params["source_i_ma"]
            measuredVoltage = random.gauss(1.0, 0.01)
            self.results.append(measuredVoltage/forcedCurrent) #Append the results

            #Shutdown
            forcedCurrent=0.0
        except Exception as e:
            print(e)
            return self.banish()
        return self.results

    def banish(self):
        #Invalid data detected in your invoke() call your banish()
        #Shutdown safely
        #Append results with invalid data
        #Return the invalid data with a return self.banish()
        #self.results.append(9999.0)
        return self.results